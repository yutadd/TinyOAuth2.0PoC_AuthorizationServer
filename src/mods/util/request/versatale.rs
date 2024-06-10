use hyper::Request;
use http_body_util::BodyExt;
use std::collections::HashMap;
pub async fn get_params_from_body(req: Request<hyper::body::Incoming>) -> HashMap<String, String> {
    let collected_data = req.collect().await.expect("not analyzable");
    let body_bytes = collected_data.to_bytes();
    let body_str = String::from_utf8(body_bytes.to_vec()).expect("Failed to convert body to string");
    body_str.split('&')
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
    percent_encoding::percent_decode_str(encoded).decode_utf8_lossy().into_owned()
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
