
use std::convert::Infallible;
use http_body_util::Full;
use hyper::body::Bytes;
use hyper::{Request, Response};
use crate::mods::config::config::CONFIG;
use crate::mods::services::authentication::{act_login, ask_login, redirect_by_login_state};
pub async fn hello(request: Request<hyper::body::Incoming>) -> Result<Response<Full<Bytes>>, Infallible> {
    let path = request.uri().path().to_string();
    let method = request.method().clone();
    if method.as_str()=="GET"{
        if path==CONFIG.endpoints.check_loggedin {
            return Ok(redirect_by_login_state(&request))
        }else if path == CONFIG.endpoints.ask_login{
            return Ok(ask_login(&request));
        }else if path == CONFIG.endpoints.ask_authorization{
            
        }else if path==CONFIG.endpoints.act_authorization{

        }else{
        }
    }else if method.as_str()=="POST"{
        if path==CONFIG.endpoints.act_login{
            return Ok(act_login(request).await)
        }else{

        }
    }else{

    }
    
    Ok(redirect_by_login_state(&request))
}