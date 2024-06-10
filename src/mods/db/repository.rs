use crate::mods::db::models::{Client, User};
use chrono::Utc;
use mysql::prelude::*;
use mysql::*;
use rand::Rng;
use rand::distributions::Alphanumeric;
use std::io::{Error, ErrorKind};
use bcrypt::{hash, verify, DEFAULT_COST};
pub struct Repository {
    pool: Pool,
}
impl Repository {
    pub fn new(database_url: &str) -> Result<Self, mysql::Error> {
        let pool = Pool::new(Opts::from_url(database_url).expect("Invalid DB URL"))?;
        Ok(Repository { pool })
    }

    pub fn create_tables(&self) -> Result<(), mysql::Error> {
        let mut conn = self.pool.get_conn()?;
        conn.query_drop(
            r"CREATE TABLE if not exists users (
                id TEXT NOT NULL UNIQUE,
                authorization_code TEXT,
                authorization_code_expires_at BIGINT,
                access_token TEXT,
                access_token_expires_at BIGINT,
                refresh_token TEXT,
                refresh_token_expires_at BIGINT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                session_id TEXT,
                session_expires_at BIGINT
            )",
        )?;
        conn.query_drop(
            r"CREATE TABLE if not exists clients (
                client_id TEXT NOT NULL UNIQUE,
                client_secret TEXT NOT NULL,
                redirect_prefix TEXT NOT NULL,
                allowed_scope TEXT NOT NULL
            )",
        )?;
        Ok(())
    }

    pub fn insert_user(&self, user: &User) -> Result<(), mysql::Error> {
        let mut conn = self.pool.get_conn()?;
        let hashed_password = hash(&user.password, DEFAULT_COST).expect("Failed to hash password");
        conn.exec_drop(
            r"INSERT INTO users (id, username, password)
              SELECT :id, :username, :password
              WHERE NOT EXISTS (SELECT 1 FROM users WHERE id = :id)",
            params! {
                "id" => &user.id,
                "username" => &user.username,
                "password" => &hashed_password,
            },
        )?;
        Ok(())
    }

    pub fn insert_client(&self, client: &Client) -> Result<(), mysql::Error> {
        let mut conn = self.pool.get_conn()?;
        conn.exec_drop(
            r"INSERT INTO clients (client_id, client_secret, redirect_prefix, allowed_scope)
              SELECT :client_id, :client_secret, :redirect_prefix, :allowed_scope
              WHERE NOT EXISTS (SELECT 1 FROM clients WHERE client_id = :client_id)",
            params! {
                "client_id" => &client.client_id,
                "client_secret" => &client.client_secret,
                "redirect_prefix" => &client.redirect_prefix,
                "allowed_scope" => &client.allowed_scope,
            },
        )?;
        Ok(())
    }

    pub fn get_users(&self) -> Result<Vec<User>, mysql::Error> {
        let mut conn = self.pool.get_conn()?;
        let users = conn.query_map(
            "SELECT id, authorization_code, authorization_code_expires_at, access_token, access_token_expires_at, refresh_token, refresh_token_expires_at, username, password, session_id, session_expires_at FROM users",
            |(id, authorization_code, authorization_code_expires_at, access_token, access_token_expires_at, refresh_token, refresh_token_expires_at, username, password, session_id, session_expires_at): (String, Option<String>, Option<i64>, Option<String>, Option<i64>, Option<String>, Option<i64>, String, String, Option<String>, Option<i64>)| {
                User {
                    id,
                    authorization_code,
                    authorization_code_expires_at: authorization_code_expires_at,
                    access_token,
                    access_token_expires_at: access_token_expires_at,
                    refresh_token,
                    refresh_token_expires_at: refresh_token_expires_at,
                    username,
                    password,
                    session_id,
                    session_expires_at: session_expires_at,
                }
            },
        )?;
        Ok(users)
    }

    pub fn get_clients(&self) -> Result<Vec<Client>, mysql::Error> {
        let mut conn = self.pool.get_conn()?;
        let clients = conn.query_map(
            "SELECT client_id, client_secret, redirect_prefix, allowed_scope FROM clients",
            |(client_id, client_secret, redirect_prefix, allowed_scope)| Client {
                client_id,
                client_secret,
                redirect_prefix,
                allowed_scope,
            },
        )?;
        Ok(clients)
    }
    pub fn is_session_valid(&self, session_id: &str) -> Result<bool, mysql::Error> {
        let mut conn = self.pool.get_conn()?;
        let result: Option<String> = conn.exec_first(
            "SELECT id FROM users WHERE session_id = :session_id AND session_expires_at > :current_time",
            params! {
                "session_id" => session_id,
                "current_time" => Utc::now().timestamp(),
            },
        )?;
        Ok(result.is_some())
    }

    pub fn issue_session_id(&self, userid: String) -> Result<String,mysql::Error> {

        let mut conn = self.pool.get_conn()?;
        let session_id: String = rand::thread_rng()
            .sample_iter(&Alphanumeric)
            .take(30)
            .map(char::from)
            .collect();
        let expire_time = Utc::now().timestamp() + 3600; // 1 hour expiration time
        conn.exec_drop(
            "UPDATE users SET session_id = :session_id, session_expires_at = :expire_time WHERE id = :userid",
            params! {
                "session_id" => &session_id,
                "expire_time" => expire_time,
                "userid" => &userid,
            },
        )?;
        Ok(session_id)
    }
    pub fn check_credential(&self, username: String, password: String) -> Result<String, mysql::Error> {
        let mut conn = self.pool.get_conn()?;
        let stored_password: Option<(String, String)> = conn.exec_first(
            "SELECT id, password FROM users WHERE username = :username",
            params! {
                "username" => &username,
            },
        )?;
        match stored_password {
            Some((user_id, stored_password)) => {
                if verify(&password, &stored_password).expect("Failed to verify password") {
                    Ok(user_id)
                } else {
                    Err(mysql::Error::from(Error::new(ErrorKind::NotFound, "Invalid credentials")))
                }
            },
            None => Err(mysql::Error::from(Error::new(ErrorKind::NotFound, "Invalid credentials"))),
        }
    }
}