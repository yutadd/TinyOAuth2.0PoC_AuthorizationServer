use once_cell::sync::Lazy;
pub struct Endpoints {
    pub check_loggedin:String,
    pub ask_login:String,
    pub ask_authorization: String,
    pub act_authorization:String,
    pub act_login:String
}

pub struct Config {
    pub server_address: String,
    pub server_port: u16,
    pub endpoints: Endpoints,
}

pub static CONFIG: Lazy<Config> = Lazy::new(|| Config {
    server_address: "localhost".to_string(),
    server_port: 8081,
    endpoints: Endpoints {
        check_loggedin:"/chk/loggedin".to_string(),
        ask_login:"/ask/login".to_string(),
        ask_authorization: "/ask/authorization".to_string(),
        act_authorization:"/act/authorization".to_string(),
        act_login:"/act/login".to_string()
    },
});