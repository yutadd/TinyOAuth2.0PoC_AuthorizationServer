use once_cell::sync::Lazy;
pub struct Endpoints {
    pub check_loggedin: String,
    pub ask_login: String,
    pub ask_authorization: String,
    pub act_authorization: String,
    pub act_login: String,
    pub exchange_token:String,
}
pub struct Db {
    pub username: String,
    pub password: String,
    pub database: String,
    pub server_domain: String,
    pub server_port: u16,
    pub database_url:String
}
pub struct ExampleClient {
    // clientの設定と一致さすべし
    pub client_id: String,
    pub client_secret: String,
    pub redirect_prefix: String,
    pub allowed_scope: Vec<String>,
}
pub struct ExampleUser {
    pub user_name:String,
    pub user_id: String,
    pub user_password: String,
}
pub fn create_database_url(username: &str, password: &str, domain: &str, port: u16, database: &str) -> String {
    format!("mysql://{}:{}@{}:{}/{}", username, password, domain, port, database)
}
pub struct Config {
    pub server_address: String,
    pub self_server_port: u16,
    pub session_id_name:String,
    pub endpoints: Endpoints,
    pub db: Db,
    pub example_client: ExampleClient,
    pub example_user: ExampleUser,
}

pub static CONFIG: Lazy<Config> = Lazy::new(|| {
    let username = "root".to_string();
    let password = "P@ssw0rd".to_string();
    let database = "authorization_server".to_string();
    let server_domain = "mariadb".to_string();
    let server_port = 3306;
    print!("initializing config");
    Config {
    server_address: "localhost".to_string(),
    self_server_port: 8081,
    session_id_name:"authorization_server_session_id".to_string(),
    endpoints: Endpoints {
        check_loggedin: "/chk/loggedin".to_string(),
        ask_login: "/ask/login".to_string(),
        ask_authorization: "/ask/authorization".to_string(),
        act_authorization: "/act/authorization".to_string(),
        act_login: "/act/login".to_string(),
        exchange_token:"/act/exchangeToken".to_string(),
    },
    db: Db {
        username: username.clone(),
        password: password.clone(),
        database: database.clone(),
        server_domain: server_domain.clone(),
        server_port: 3306,
        database_url: create_database_url(&username, &password, &server_domain, server_port, &database),
    },
    example_client: ExampleClient {
        client_id: "123abcABC".to_string(),
        client_secret: "client_P@ssw0rd".to_string(),
        redirect_prefix: "http://localhost/".to_string(),
        allowed_scope: vec!["read".to_string()],
    },
    example_user: ExampleUser {
        user_name:"DotPiano".to_string(),
        user_id: "user01".to_string(),
        user_password: "P@ssw0rd".to_string(),
    },
}});
