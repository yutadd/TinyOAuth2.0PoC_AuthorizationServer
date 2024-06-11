use crate::mods::config::config::CONFIG;
use crate::mods::db::repository::Repository;
use crate::mods::util::request::versatale::{basic_authentication, get_params_from_body};
use http_body_util::Full;
use hyper::body::Bytes;
use hyper::{Request, Response};

use crate::mods::util::response::token::{return_error_object, return_token_object};
pub async fn exchange_token(request: Request<hyper::body::Incoming>) -> Response<Full<Bytes>> {
    println!("exchanging token");
    if basic_authentication(&request).is_some() {
        let query_params = get_params_from_body(request).await;
        let grant_type = query_params.get("grant_type").map_or("", String::as_str);
        let code = query_params.get("code").map_or("", String::as_str);
        if let Ok(repo) = Repository::new(&CONFIG.db.database_url) {
            if grant_type == "code" {
                let (token,refresh_token) = repo
                    .issue_token(code.to_string())
                    .expect("Error issueing token");
                return return_token_object(token,refresh_token);
            } else {
                return_error_object(
                    "we only support code as grant type".to_string(),
                    "check your grant type".to_string(),
                )
            }
        } else {
            return_error_object(
                "Couldn't connect to DB repo.".to_string(),
                "check if the database is up.".to_string(),
            )
        }
    } else {
        return_error_object(
            "Invalid_authorization_header".to_string(),
            "check yourauthorization header".to_string(),
        )
    }
}
