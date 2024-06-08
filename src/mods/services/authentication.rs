
use crate::mods::config::config::CONFIG;
use http_body_util::Full;
use crate::mods::util::request::authentication::is_loggedin;
use hyper::body::Bytes;
use hyper::{Request, Response};
pub fn redirect_by_login_state(request: Request<hyper::body::Incoming>)->Response<Full<Bytes>>{
    if is_loggedin(request){
        let mut response = Response::new(Full::new(Bytes::from("")));
        *response.status_mut() = hyper::StatusCode::FOUND;
        response.headers_mut().insert("Location", format!("http://{}:{}{}",CONFIG.server_address,CONFIG.self_server_port,CONFIG.endpoints.ask_authorization).parse().unwrap());
        response
    }else{
        let mut response = Response::new(Full::new(Bytes::from("")));
        *response.status_mut() = hyper::StatusCode::FOUND;
        response.headers_mut().insert("Location", format!("http://{}:{}{}",CONFIG.server_address,CONFIG.self_server_port,CONFIG.endpoints.ask_login).parse().unwrap());
        response
    }
}