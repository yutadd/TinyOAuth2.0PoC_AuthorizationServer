
use http_body_util::Full;
use hyper::body::Bytes;
use hyper::Response;

use crate::mods::util::file::file::read_file;

// Start Generation Here
pub fn return_login_page() -> Response<Full<Bytes>> {
    let contents=read_file("templates/login_page.html".to_string()).unwrap_or("# there is error reading templates/login_page.html".to_string());
    let response = Response::new(Full::new(Bytes::from(contents)));
    response
}
