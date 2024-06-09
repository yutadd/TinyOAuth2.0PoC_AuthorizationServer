use chrono::{NaiveDateTime, Utc};

pub struct User {
    pub id: String,
    pub authorization_code: Option<String>,
    pub authorization_code_expires_at: Option<i64>,
    pub access_token: Option<String>,
    pub access_token_expires_at: Option<i64>,
    pub refresh_token: Option<String>,
    pub refresh_token_expires_at: Option<i64>,
    pub username: String,
    pub password: String,
    pub session_id: Option<String>,
    pub session_expires_at: Option<i64>,
}

impl User {
    pub fn new(id: String, username: String, password: String) -> Self {
        User {
            id,
            authorization_code: None,
            authorization_code_expires_at: None,
            access_token: None,
            access_token_expires_at: None,
            refresh_token: None,
            refresh_token_expires_at: None,
            username,
            password,
            session_id: None,
            session_expires_at: None,
        }
    }
}
pub struct Client {
    pub client_id: String,
    pub client_secret: String,
    pub redirect_prefix: String,
    pub allowed_scope: String,
}