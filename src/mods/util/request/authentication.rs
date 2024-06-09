use hyper::Request;

use crate::mods::{config::config::CONFIG, db::repository::Repository};
pub fn is_user_loggedin(request: &Request<hyper::body::Incoming>) -> bool {
    let repo = Repository::new(&CONFIG.db.database_url).expect("Failed to create repository");
    let headers = request.headers().clone();
    if let Some(cookie) = headers.get("Cookie") {
        let cookie_str = cookie.to_str().unwrap_or("");
        if cookie_str.contains(CONFIG.session_id_name.as_str()) {
            let splited = cookie_str.split(';');
            for part in splited {
                let trimmed = part.trim();
                if trimmed.starts_with(CONFIG.session_id_name.as_str()) {
                    let session_id = trimmed.split('=').nth(1).unwrap_or("");
                    if !session_id.is_empty() {
                        return repo.is_session_valid(session_id).unwrap_or(false);
                    }
                }
            }
        }
    }
    false
}
