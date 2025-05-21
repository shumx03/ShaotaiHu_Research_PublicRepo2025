use rand::prelude::*;
type Vertex = usize;

pub fn start() -> Vertex{
    let ran_start = rand::thread_rng().gen_range(0..1971281) as usize;
    return ran_start;
}

pub fn end() -> Vertex{
    let start = start();
    let ran_end = rand::thread_rng().gen_range(0..1971281) as usize;
    if start != ran_end{
        return ran_end;
    } else {
        let ran_end_two = rand::thread_rng().gen_range(0..1971281) as usize;
        return ran_end_two;
    } 
}

pub fn sample() -> Vertex{
    let ran_sample = rand::thread_rng().gen_range(0..1971281) as usize;
    return ran_sample;
}
