use crate::mods::config::config::CONFIG;
use crate::mods::services::authentication::{act_login, ask_login, redirect_by_login_state};
use crate::mods::services::authorization::act_authorization;
use crate::mods::services::authorization::ask_authorization;
use crate::mods::util::response::versatale::return_error_page;
use http_body_util::Full;
use hyper::body::Bytes;
use hyper::{Request, Response, StatusCode};
use std::convert::Infallible;
use crate::mods::services::token::exchange_token;
pub async fn hello(
    request: Request<hyper::body::Incoming>,
) -> Result<Response<Full<Bytes>>, Infallible> {
    let path = request.uri().path().to_string();
    let method = request.method().clone();
    if method.as_str() == "GET" {
        if path == CONFIG.endpoints.check_loggedin {
            return Ok(redirect_by_login_state(&request));
        } else if path == CONFIG.endpoints.ask_login {
            return Ok(ask_login(&request));
        } else if path == CONFIG.endpoints.ask_authorization {
            return Ok(ask_authorization(&request));
        } else if path == CONFIG.endpoints.act_authorization {
            return Ok(act_authorization(&request));
        }
    } else if method.as_str() == "POST" {
        if path == CONFIG.endpoints.act_login {
            return Ok(act_login(request).await);
        } else if path==CONFIG.endpoints.exchange_token{
            return Ok(exchange_token(request).await);
        }
    }
    println!("return 404 because path that the user requested is invalid.");
    Ok(return_error_page(StatusCode::NOT_FOUND, "path not found."))
}
