use crate::mods::config::config::CONFIG;
use crate::mods::db::repository;
use crate::mods::util::request::authentication::is_user_loggedin;
use crate::mods::util::response::authentication::return_session_and_redirect_authorization;
use crate::mods::util::{
    response::authentication::return_login_page, response::versatale::return_redirect_request,
};
use http_body_util::Full;
use hyper::body:: Bytes;
use hyper::{Request, Response};
use crate::mods::util::request::versatale::get_params_from_body;

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
        return_login_page(request)
    } else {
        return_redirect_request(CONFIG.endpoints.ask_authorization.clone())
    }
}

pub async fn act_login(request: Request<hyper::body::Incoming>) -> Response<Full<Bytes>> {
    let params =get_params_from_body(request).await;
    let username = params.get("username").unwrap_or(&"".to_string()).clone();
    let password = params.get("password").unwrap_or(&"".to_string()).clone();
    println!("{:?}",params);
    let mut new_params = params.clone();
    new_params.remove("username");
    new_params.remove("password");
    let query_string: String = new_params.iter()
        .map(|(key, value)| format!("{}={}", key, value))
        .collect::<Vec<String>>()
        .join("&");
    if let Ok(repo) = repository::Repository::new(&CONFIG.db.database_url) {
        if let Ok(userid)=repo.check_credential(username,password){
            // TODOセッション生成
            if let Ok(session_id)=repo.issue_session_id(userid){
                return_session_and_redirect_authorization(session_id, query_string)
            }else{
                return_redirect_request(format!(
                    "http://{}:{}{}?{}",
                    CONFIG.server_address, CONFIG.self_server_port, CONFIG.endpoints.ask_login, query_string
                ))
            }
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
