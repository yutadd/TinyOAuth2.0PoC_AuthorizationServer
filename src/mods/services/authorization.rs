use crate::mods::config::config::CONFIG;
use crate::mods::util::request::authentication::is_user_loggedin;
use crate::mods::util::request::versatale::get_session_id_from_request;
use crate::mods::util::response::authorization::return_authorization_page;
use crate::mods::util::response::versatale::return_error_page;
use crate::mods::util::response::versatale::return_redirect_request;
use http_body_util::Full;
use hyper::body::Bytes;
use hyper::{Request, Response};
use crate::mods::db::repository::Repository;
use crate::mods::util::request::versatale::get_query_params;
use uuid::Uuid;
pub fn ask_authorization(request: &Request<hyper::body::Incoming>) -> Response<Full<Bytes>> {
    let uri = request.uri();
    let query = uri.query().unwrap_or("");
    if is_user_loggedin(request) {
        return_authorization_page(request)
    } else {
        return_redirect_request(format!(
            "http://{}:{}{}?{}",
            CONFIG.server_address, CONFIG.self_server_port, CONFIG.endpoints.ask_login, query
        ))
    }
}
pub fn act_authorization(request: &Request<hyper::body::Incoming>) -> Response<Full<Bytes>> {
    let uri = request.uri();
    let query = uri.query().unwrap_or("");
    let query_params = get_query_params(request.uri());
    let client_id = query_params.get("client_id").map_or("", String::as_str);
    let response_type = query_params.get("response_type").map_or("", String::as_str);
    let state = query_params.get("state").map_or("", String::as_str);
    let success_redirect_uri = query_params
        .get("success_redirect_uri")
        .map_or("", String::as_str);
    let fail_redirect_uri = query_params
        .get("fail_redirect_uri")
        .map_or("", String::as_str);
    let scope = query_params.get("scope").map_or("", String::as_str);
    let repo = Repository::new(&CONFIG.db.database_url).expect("couldn't reached to DB.");
    if is_user_loggedin(request) {
        if repo
            .is_redirect_url_valid(&client_id.to_string(), &success_redirect_uri.to_string())
            .expect("couldn't check redirect uri by DB error.")
        {
            if repo
                .is_redirect_url_valid(&client_id.to_string(), &fail_redirect_uri.to_string())
                .expect("couldn't check redirect uri by DB error.")
            {
                if repo.is_scope_valid(&client_id.to_string(), &scope.to_string()).expect("Couldn't check scope due to DB error.") {
                    if response_type == "code" {
                        println!("authorization success. returning code to client.");
                        let authorization_code = Uuid::new_v4().to_string();
                        let session_id=get_session_id_from_request(request).expect("failed to parse session_id");
                        repo.save_authorization_code(&session_id.to_string(), &authorization_code)
                            .expect("saving authorization code failed");
                        println!("returned code to client.");
                        return return_redirect_request(format!(
                            "{}?code={}&state={}",
                            success_redirect_uri, authorization_code, state
                        ));
                    } else {
                        println!("returning error because the authorization type is invalid.");
                        return return_redirect_request(format!(
                            "{}?error=unsupported_response_type&state={}",
                            fail_redirect_uri, state
                        ));
                    }
                } else {
                    println!("returning error because scope that the user requested is invalid.");
                    return return_redirect_request(format!(
                        "{}?error=invalid_scope&state={}",
                        fail_redirect_uri, state
                    ));
                }
            } else {
                println!("returning error because failed redirect uri the user requested is invalid");
                return_error_page(
                    hyper::StatusCode::BAD_REQUEST,
                    "The success_redirecturi you contained to your request is invalid",
                )
            }
        } else {
            println!("showing error because successfulredirect the user provided is something wrong.");
            return_error_page(
                hyper::StatusCode::BAD_REQUEST,
                "The success_redirecturi you contained to your request is invalid",
            )
        }
    } else {
        println!("redirecting to authorization endpoint because the user is not logged in.");
        return_redirect_request(format!(
            "http://{}:{}{}?{}",
            CONFIG.server_address, CONFIG.self_server_port, CONFIG.endpoints.ask_login, query
        ))
    }
}
