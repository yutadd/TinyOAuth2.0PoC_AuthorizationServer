use http_body_util::Full;
use hyper::body::Bytes;
use hyper:: Response;

pub fn return_redirect_request(uri:String)->Response<Full<Bytes>>{
    let mut response = Response::new(Full::new(Bytes::from("")));
    *response.status_mut() = hyper::StatusCode::FOUND;
    response.headers_mut().insert("Location", uri.parse().unwrap());
    response
}
