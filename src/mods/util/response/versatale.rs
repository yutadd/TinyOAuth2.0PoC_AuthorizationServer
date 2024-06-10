use http_body_util::Full;
use hyper::body::Bytes;
use hyper:: Response;

pub fn return_redirect_request(uri:String)->Response<Full<Bytes>>{
    let mut response = Response::new(Full::new(Bytes::from("")));
    *response.status_mut() = hyper::StatusCode::FOUND;
    response.headers_mut().insert("Location", uri.parse().unwrap());
    response
}
use hyper::header::CONTENT_TYPE;

pub fn return_error_page(status_code: hyper::StatusCode, message: &str) -> Response<Full<Bytes>> {
    let mut response = Response::new(Full::new(Bytes::from(message.to_string())));
    *response.status_mut() = status_code;
    response.headers_mut().insert(CONTENT_TYPE, "text/html".parse().unwrap());
    response
}
