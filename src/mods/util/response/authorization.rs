use hyper::Request;
use http_body_util::Full;
use hyper::body::Bytes;
use hyper::Response;
use crate::mods::util::file::file::read_file;
use crate::mods::util::request::versatale::get_query_params;
pub fn return_authorization_page(request : &Request<hyper::body::Incoming>)->Response<Full<Bytes>>{
    let query_params = get_query_params(request.uri());
    let client_id = query_params.get("client_id").map_or("", String::as_str);
    let response_type = query_params.get("response_type").map_or("", String::as_str);
    let state = query_params.get("state").map_or("", String::as_str);
    let success_redirect_uri = query_params.get("success_redirect_uri").map_or("", String::as_str);
    let fail_redirect_uri = query_params.get("fail_redirect_uri").map_or("", String::as_str);
    let scope = query_params.get("scope").map_or("", String::as_str);
    let contents = read_file("templates/authorize_page.html".to_string())
        .unwrap_or("# there is error reading templates/authorize_page.html".to_string())
        .replace("{{client_id}}", client_id)
        .replace("{{response_type}}", response_type)
        .replace("{{state}}", state)
        .replace("{{success_redirect_uri}}", success_redirect_uri)
        .replace("{{fail_redirect_uri}}", fail_redirect_uri)
        .replace("{{scope}}", scope);
    let response = Response::new(Full::new(Bytes::from(contents)));
    response
}