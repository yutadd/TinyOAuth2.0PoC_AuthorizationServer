use crate::mods::config::config::CONFIG;
use crate::mods::db::repository;
use crate::mods::util::request::authentication::is_user_loggedin;
use crate::mods::util::{
    response::authentication::return_login_page, response::versatale::return_redirect_request,
};
use std::collections::HashMap;
use http_body_util::{BodyExt, Full};
use hyper::body::{Body, Bytes, Frame};
use hyper::{Request, Response};

pub fn redirect_by_login_state(request: &Request<hyper::body::Incoming>) -> Response<Full<Bytes>> {
    let uri = request.uri();
    let query = uri.query().unwrap_or("");
    if is_user_loggedin(request) {
        return_redirect_request(format!(
            "http://{}:{}{}?{}",
            CONFIG.server_address,
            CONFIG.self_server_port,
            CONFIG.endpoints.ask_authorization,
            query
        ))
    } else {
        return_redirect_request(format!(
            "http://{}:{}{}?{}",
            CONFIG.server_address, CONFIG.self_server_port, CONFIG.endpoints.ask_login, query
        ))
    }
}
pub fn ask_login(request: &Request<hyper::body::Incoming>) -> Response<Full<Bytes>> {
    if !is_user_loggedin(request) {
        return_login_page()
    } else {
        return_redirect_request(CONFIG.endpoints.ask_authorization.clone())
    }
}
async fn get_params_from_body(req: Request<hyper::body::Incoming>) -> HashMap<String, String> {
    let collected_data = req.collect().await.expect("not analyzable");
    let body_bytes = collected_data.to_bytes();
    let body_str = String::from_utf8(body_bytes.to_vec()).expect("Failed to convert body to string");
    body_str.split('&')
        .filter_map(|s| {
            let mut split = s.splitn(2, '=');
            match (split.next(), split.next()) {
                (Some(key), Some(value)) => Some((key.to_string(), value.to_string())),
                _ => None,
            }
        })
        .collect()
}

pub async fn act_login(request: Request<hyper::body::Incoming>) -> Response<Full<Bytes>> {
    let params = get_params_from_body(request).await;
    let username = params.get("username").unwrap_or(&"".to_string()).clone();
    let password = params.get("password").unwrap_or(&"".to_string()).clone();
    let mut new_params = params.clone();
    new_params.remove("username");
    new_params.remove("password");
    let query_string: String = new_params.iter()
        .map(|(key, value)| format!("{}={}", key, value))
        .collect::<Vec<String>>()
        .join("&");
    if let Ok(repo) = repository::Repository::new(&CONFIG.db.database_url) {
        
        if repo.check_credential(username,password).is_ok(){
            // TODOセッション生成
            return_redirect_request(format!("{}?{}",CONFIG.endpoints.ask_authorization.clone(),query_string))
        }else{
            return_redirect_request(format!(
                "http://{}:{}{}?{}",
                CONFIG.server_address, CONFIG.self_server_port, CONFIG.endpoints.ask_login, query_string
            ))
        }
    } else {
        return_redirect_request(format!(
            "http://{}:{}{}?{}",
            CONFIG.server_address, CONFIG.self_server_port, CONFIG.endpoints.ask_login, query_string
        ))
    }
}
