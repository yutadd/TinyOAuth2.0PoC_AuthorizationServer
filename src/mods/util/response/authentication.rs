
use http_body_util::Full;
use hyper::body::Bytes;
use hyper::Response;
use hyper::Request;
use crate::mods::config::config::CONFIG;
use crate::mods::util::file::file::read_file;
use crate::mods::util::request::versatale::get_query_params;
use hyper::header::{HeaderValue, SET_COOKIE};
use std::time::Duration;
// Start Generation Here
pub fn return_login_page(request:&Request<hyper::body::Incoming>) -> Response<Full<Bytes>> {
    let query_params = get_query_params(request.uri());
    let client_id = query_params.get("client_id").map_or("", String::as_str);
    let response_type = query_params.get("response_type").map_or("", String::as_str);
    let state = query_params.get("state").map_or("", String::as_str);
    let success_redirect_uri = query_params.get("success_redirect_uri").map_or("", String::as_str);
    let fail_redirect_uri = query_params.get("fail_redirect_uri").map_or("", String::as_str);
    let scope = query_params.get("scope").map_or("", String::as_str);
    let contents = read_file("templates/login_page.html".to_string())
        .unwrap_or("# there is error reading templates/login_page.html".to_string())
        .replace("{{client_id}}", client_id)
        .replace("{{response_type}}", response_type)
        .replace("{{state}}", state)
        .replace("{{success_redirect_uri}}", success_redirect_uri)
        .replace("{{fail_redirect_uri}}", fail_redirect_uri)
        .replace("{{scope}}", scope);
    let response = Response::new(Full::new(Bytes::from(contents)));
    response
}
pub fn return_session_and_redirect_authorization(session_id:String,query:String)->Response<Full<Bytes>>{
    let mut response = Response::new(Full::new(Bytes::from("")));
    *response.status_mut() = hyper::StatusCode::FOUND;
    let cookie_value = format!("{}={}; Path=/; HttpOnly; Max-Age={}", CONFIG.session_id_name.as_str(),session_id, Duration::from_secs(3600).as_secs());
    response.headers_mut().insert(SET_COOKIE, HeaderValue::from_str(&cookie_value).unwrap());
    response.headers_mut().insert("Location", format!("{}?{}",CONFIG.endpoints.ask_authorization.clone(),query).parse().unwrap());
    response
}