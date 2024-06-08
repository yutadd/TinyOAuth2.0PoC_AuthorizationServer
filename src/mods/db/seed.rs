use mysql::*;
use mysql::prelude::*;
use crate::mods::config::config::CONFIG;

pub fn data_seeding()->Result<(),mysql::Error>{
    // 接続文字列を設定
    let url = format!("mysql://{}:{}@{}:{}/{}",CONFIG.db.username,CONFIG.db.password,CONFIG.db.server_domain,CONFIG.db.server_port,CONFIG.db.database);

    // プールを作成
    let pool = Pool::new(Opts::from_url(url.as_str()).expect("Invalid DB URL. Check config->db params"))?;

    // コネクションを取得
    let mut conn = pool.get_conn()?;

    // クエリを実行
    conn.query_drop(
        r"CREATE TABLE if not exists users (
            id TEXT NOT NULL UNIQUE,
            authorization_code TEXT,
            authorization_code_expires_at DATETIME,
            access_token TEXT,
            access_token_expires_at DATETIME,
            refresh_token TEXT,
            refresh_token_expires_at DATETIME,
            username TEXT NOT NULL UNIQUE,
            password BLOB NOT NULL,
            session_id TEXT,
            session_expires_at DATETIME
        )"
    )?;
    conn.query_drop(r"CREATE TABLE if not exists clients (
        client_id TEXT NOT NULL UNIQUE,
        client_secret TEXT NOT NULL,
        redirect_prefix TEXT NOT NULL,
        allowed_scope TEXT NOT NULL
    )");

    // データを挿入
    conn.exec_drop(
        r"INSERT INTO users (id, username, password)
          SELECT :id, :username, :password
          WHERE NOT EXISTS (SELECT 1 FROM users WHERE id = :id)",
        params! {
            "username" => &CONFIG.example_user.user_name,
            "id"=>&CONFIG.example_user.user_id,
            "password"=>&CONFIG.example_user.user_password
        },
    )?;

    conn.exec_drop(
        r"INSERT INTO clients (client_id, client_secret, redirect_prefix, allowed_scope)
          SELECT :client_id, :client_secret, :redirect_prefix, :allowed_scope
          WHERE NOT EXISTS (SELECT 1 FROM clients WHERE client_id = :client_id)",
        params! {
            "client_id"=>&CONFIG.example_client.client_id,
            "client_secret" => &CONFIG.example_client.client_secret,
            "redirect_prefix"=>&CONFIG.example_client.redirect_prefix,
            "allowed_scope"=>&CONFIG.example_client.allowed_scope.join(" ")
        },
    )?;
    // データを取得
    let selected_users: Vec<(String, String)> = conn.query("SELECT id, username FROM users")?;

    for user in selected_users {
        println!("ID: {}, Name: {}", user.0, user.1);
    }
    Ok(())
}