# Use the official Rust image as the base image
FROM rust:latest

# Set the working directory inside the container
WORKDIR /usr/src/app
RUN cargo install cargo-watch
# Expose the port that the server will run on
EXPOSE 8081

# Set the command to run the server
CMD ["cargo", "watch", "-x", "run"]