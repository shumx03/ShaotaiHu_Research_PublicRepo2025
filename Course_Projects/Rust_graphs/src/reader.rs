use std::fs::File;
use std::io::prelude::*;

type Vertex = usize;
type ListOfEdges = Vec<(Vertex, Vertex)>;

// reader function
pub fn read_txt(path: &str) -> ListOfEdges {
    let mut data: ListOfEdges = Vec::new();
    let file = File::open(path).expect("Could not open file");
    let buf_reader = std::io::BufReader::new(file).lines();
    for line in buf_reader{
        let line_str = line.expect("error reading");
        let v: Vec<&str> = line_str.trim().split_whitespace().collect();
        let x = v[0].parse::<usize>().unwrap();
        let y = v[1].parse::<usize>().unwrap();
        data.push((x,y));
    }   
    return data;
}