use once_cell::sync::Lazy;
pub struct Endpoints {
    pub check_loggedin: String,
    pub ask_login: String,
    pub ask_authorization: String,
    pub act_authorization: String,
    pub act_login: String,
}
pub struct Db {
    pub username: String,
    pub password: String,
    pub database: String,
    pub server_domain: String,
    pub server_port: u16,
}
pub struct ExampleClient {
    // clientの設定と一致さすべし
    pub client_id: String,
    pub client_secret: String,
    pub redirect_prefix: String,
    pub allowed_scope: Vec<String>,
}
pub struct ExampleUser {
    pub user_id: String,
    pub user_password: String,
}
pub struct Config {
    pub server_address: String,
    pub self_server_port: u16,
    pub endpoints: Endpoints,
    pub db: Db,
    pub example_client: ExampleClient,
    pub example_user: ExampleUser,
}

pub static CONFIG: Lazy<Config> = Lazy::new(|| Config {
    server_address: "localhost".to_string(),
    self_server_port: 8081,

    endpoints: Endpoints {
        check_loggedin: "/chk/loggedin".to_string(),
        ask_login: "/ask/login".to_string(),
        ask_authorization: "/ask/authorization".to_string(),
        act_authorization: "/act/authorization".to_string(),
        act_login: "/act/login".to_string(),
    },
    db: Db {
        username: "myuser".to_string(),
        password: "P@ssw0rd".to_string(),
        database: "authorization_server".to_string(),
        server_domain: "mariadb".to_string(),
        server_port: 3306,
    },
    example_client: ExampleClient {
        client_id: "123abcABC".to_string(),
        client_secret: "client_P@ssw0rd".to_string(),
        redirect_prefix: "http://localhost/".to_string(),
        allowed_scope: vec!["read".to_string()],
    },
    example_user: ExampleUser {
        user_id: "user01".to_string(),
        user_password: "P@ssw0rd".to_string(),
    },
});
