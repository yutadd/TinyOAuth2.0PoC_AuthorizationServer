
use std::convert::Infallible;
use http_body_util::Full;
use hyper::body::Bytes;
use hyper::{Request, Response};
pub async fn hello(request: Request<hyper::body::Incoming>) -> Result<Response<Full<Bytes>>, Infallible> {
    let path = request.uri().path().to_string();
    let method = request.method().clone();
    if method.as_str()=="GET"{
        if path=="/chk/loggedin" {

        }else if path == "/ask/login"{

        }else if path == "/ask/authorization"{

        }else if path=="/act/authorization"{

        }else{
            
        }
    }else if method.as_str()=="POST"{
        if path=="/act/login"{

        }else{

        }
    }else{

    }

    // let headers = request.headers().clone();
    let/*mut*/ response = Response::new(Full::new(Bytes::from("Hello, World!")));
    // *response.status_mut() = hyper::StatusCode::OK;
    // response.headers_mut().insert("Content-Type", "text/plain".parse().unwrap());
    Ok(response)
}