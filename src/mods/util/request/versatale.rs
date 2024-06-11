use http_body_util::BodyExt;
use hyper::Request;
use std::collections::HashMap;
pub async fn get_params_from_body(
    mut req: Request<hyper::body::Incoming>,
) -> HashMap<String, String> {
    let collected_data = req.body_mut().collect().await.expect("not analyzable");
    let body_bytes = collected_data.to_bytes();
    let body_str =
        String::from_utf8(body_bytes.to_vec()).expect("Failed to convert body to string");
    body_str
        .split('&')
        .filter_map(|s| {
            let mut split = s.splitn(2, '=');
            match (split.next(), split.next()) {
                (Some(key), Some(value)) => Some((url_decode(key), url_decode((value)))),
                _ => None,
            }
        })
        .collect()
}
fn url_decode(encoded: &str) -> String {
    percent_encoding::percent_decode_str(encoded)
        .decode_utf8_lossy()
        .into_owned()
}
use hyper::Uri;

use crate::mods::config::config::CONFIG;
pub fn get_query_params(uri: &Uri) -> HashMap<String, String> {
    uri.query()
        .unwrap_or("")
        .split('&')
        .filter_map(|s| {
            let mut split = s.splitn(2, '=');
            match (split.next(), split.next()) {
                (Some(key), Some(value)) => Some((url_decode(key), url_decode(value))),
                _ => None,
            }
        })
        .collect()
}
pub fn get_session_id_from_request(request: &Request<hyper::body::Incoming>) -> Option<String> {
    let headers = request.headers().clone();
    if let Some(cookie) = headers.get("Cookie") {
        let cookie_str = cookie.to_str().unwrap_or("");
        if cookie_str.contains(CONFIG.session_id_name.as_str()) {
            let splited = cookie_str.split(';');
            for part in splited {
                let trimmed = part.trim();
                if trimmed.starts_with(CONFIG.session_id_name.as_str()) {
                    return trimmed.split('=').nth(1).map(|s| s.to_string());
                }
            }
        }
    }
    None
}
use crate::mods::db::repository::Repository;
use base64::{
    engine::general_purpose,
    Engine as _,
};
use hyper::header::AUTHORIZATION;
pub fn basic_authentication(request: &Request<hyper::body::Incoming>) -> Option<String> {
    println!("[util/req/vers] authenticating client");
    let repo = Repository::new(CONFIG.db.database_url.as_str()).expect("failed initialize repo");

    if let Some(auth_header) = request.headers().get(AUTHORIZATION) {
        if let Ok(auth_str) = auth_header.to_str() {
            if auth_str.starts_with("Basic ") {
                let base64_credentials = &auth_str[6..];
                println!("{}",base64_credentials);
                let decoded_credentials = general_purpose::STANDARD.decode(base64_credentials).expect("error at decoding authentication payload");
                    if let Ok(credentials) = String::from_utf8(decoded_credentials) {
                        let mut split = credentials.splitn(2, ':');
                        if let (Some(client_id), Some(client_secret)) = (split.next(), split.next())
                        {
                            if repo
                                .client_authentication(
                                    &client_id.to_string(),
                                    &client_secret.to_string(),
                                )
                                .expect("error verifying ")
                            {
                                return Some(client_id.to_string());
                            }else{
                                println!("[util/req/vers]failed client authentication")
                            }
                        }else{
                            println!("[util/req/vers]error spliting credentials")
                        }
                    }else{
                        println!("[util/req/vers]error couldn't convert str vec<u8 into String")
                    }
            }else{
                println!("[util/req/vers]error authentication method is not basic")
            }
        }else{
            println!("[util/req/vers]error converting to string.")
        }
    }else{
        println!("[util/req/vers]no authorization header found.")
    }
    None
}
