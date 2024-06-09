use hyper::server::conn::http1;
use hyper::service::service_fn;
use hyper_util::rt::TokioIo;
use mods::config::config::CONFIG;
use std::net::SocketAddr;
use tokio::net::TcpListener;
mod mods;
use crate::mods::routes::routes::hello;
use crate::mods::db::seed::data_seeding;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error + Send + Sync>> {
    println!("starting server!");
    let seedingresult=data_seeding();
    if seedingresult.is_ok(){
        let addr = SocketAddr::from(([0, 0, 0, 0], CONFIG.self_server_port));
        let listener = TcpListener::bind(addr).await?;
        loop {
            let (stream, _) = listener.accept().await?;
            let io = TokioIo::new(stream);
            tokio::task::spawn(async move {
                if let Err(err) = http1::Builder::new()
                    .serve_connection(io, service_fn(hello))
                    .await
                {
                    eprintln!("Error serving connection: {:?}", err);
                }
            });
        }
    }else{
        eprintln!("{:?}", seedingresult.err());
        Err(Box::new(std::io::Error::new(std::io::ErrorKind::Other, "Seeding failed"))as Box<dyn std::error::Error + Send + Sync>)
        
    }
    
}
