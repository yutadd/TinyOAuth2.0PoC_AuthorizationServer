use crate::mods::config::config::CONFIG;
use crate::mods::db::models::{Client, User};
use crate::mods::db::repository::Repository;
use mysql::*;

pub fn data_seeding() -> Result<(), mysql::Error> {
    // リポジトリを作成
    println!("initializing db");
    println!("{:?}",CONFIG.self_server_port);
    println!("↑database url");
    let repository = Repository::new(CONFIG.db.database_url.as_str())?;
    println!("repository initialized");
    // テーブルを作成
    repository.create_tables()?;

    // ユーザーを挿入
    let user = User::new(
        CONFIG.example_user.user_id.clone(),
        CONFIG.example_user.user_name.clone(),
        CONFIG.example_user.user_password.clone(),
    );
    repository.insert_user(&user)?;

    // クライアントを挿入
    let client = Client {
        client_id: CONFIG.example_client.client_id.clone(),
        client_secret: CONFIG.example_client.client_secret.clone(),
        redirect_prefix: CONFIG.example_client.redirect_prefix.clone(),
        allowed_scope: CONFIG.example_client.allowed_scope.join(" "),
    };
    repository.insert_client(&client)?;

    // データを取得して表示
    let selected_users = repository.get_users()?;
    for user in selected_users {
        println!("ID: {}, Name: {}", user.id, user.username);
    }

    Ok(())
}
