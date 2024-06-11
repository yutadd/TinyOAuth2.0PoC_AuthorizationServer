use http_body_util::Full;
use hyper::body::Bytes;
use hyper::{Request, Response};
use crate::mods::config::config::CONFIG;
use crate::mods::db::repository::Repository;
use crate::mods::util::request::versatale::{basic_authentication, get_params_from_body};

use crate::mods::util::response::token::{return_token_object, return_error_object};
pub async fn exchange_token(request: Request<hyper::body::Incoming>) -> Response<Full<Bytes>> {
    println!("exchanging token");
    if let Some(client_id)=basic_authentication(&request){
        let query_params = get_params_from_body(request).await;
        let grant_type = query_params.get("grant_type").map_or("", String::as_str);
        let code = query_params.get("code").map_or("", String::as_str);
        let success_redirect_url = query_params.get("success_redirect_url").map_or("", String::as_str);
        let fail_redirect_url=query_params.get("fail_redirect_url").map_or("", String::as_str);
            if let Ok(repo)=Repository::new(&CONFIG.db.database_url){
                if repo.is_redirect_url_valid(&client_id.to_string(),&success_redirect_url.to_string()).expect("Error verifying redirect url"){
                    if repo.is_redirect_url_valid(&client_id.to_string(),&fail_redirect_url.to_string()).expect("Error verifying redirect url"){
                        if grant_type=="code"{
                            let token=repo.issue_token(code.to_string()).expect("Error issueing token");
                            return return_token_object(token)
                        }else{
                            return_error_object("we only support code as grant type".to_string(),"check your grant type".to_string())
                        }
                    }else{
                        return_error_object("Invalid fail redirect url".to_string(), "check your redirect url".to_string())
                    }
                }else{
                    return_error_object("Invalid success redirect_url".to_string(), "check your redirect url".to_string())
                }
            }else{
                return_error_object("Couldn't connect to DB repo.".to_string(),"check if the database is up.".to_string())
            }
    }else{
        return_error_object("Invalid_authorization_header".to_string(),"check yourauthorization header".to_string())
    }
    
}