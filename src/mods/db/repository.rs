use mysql::*;
use mysql::prelude::*;
use crate::mods::db::models::{User, Client};
use chrono::{NaiveDateTime, Utc};
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
            )"
        )?;
        conn.query_drop(
            r"CREATE TABLE if not exists clients (
                client_id TEXT NOT NULL UNIQUE,
                client_secret TEXT NOT NULL,
                redirect_prefix TEXT NOT NULL,
                allowed_scope TEXT NOT NULL
            )"
        )?;
        Ok(())
    }

    pub fn insert_user(&self, user: &User) -> Result<(), mysql::Error> {
        let mut conn = self.pool.get_conn()?;
        conn.exec_drop(
            r"INSERT INTO users (id, username, password)
              SELECT :id, :username, :password
              WHERE NOT EXISTS (SELECT 1 FROM users WHERE id = :id)",
            params! {
                "id" => &user.id,
                "username" => &user.username,
                "password" => &user.password,
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
            |(client_id, client_secret, redirect_prefix, allowed_scope)| {
                Client {
                    client_id,
                    client_secret,
                    redirect_prefix,
                    allowed_scope,
                }
            },
        )?;
        Ok(clients)
    }
}