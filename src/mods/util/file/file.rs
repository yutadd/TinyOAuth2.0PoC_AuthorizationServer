use std::fs::File;
use std::io::Read;
pub fn read_file(filename:String)->Result<String,String>{
    let mut file = match File::open(filename) {
        Ok(file) => file,
        Err(_) => {
            return Err("file not found".to_string())
        }
    };

    let mut contents = String::new();
    if let Err(_) = file.read_to_string(&mut contents) {
        return Err("Can't read file.".to_string())
    }
    Ok(contents)
}