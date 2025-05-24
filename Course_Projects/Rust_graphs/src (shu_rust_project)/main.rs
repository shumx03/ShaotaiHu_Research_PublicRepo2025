// Shaotai Hu DS210 Project
// Is California road network design logical and effective?
// Note:
// The data is directed
// link to data used: https://snap.stanford.edu/data/roadNet-CA.html

mod reader;
mod random;

use std::fs::File;
use std::io::prelude::*;
use rand::prelude::*;
use std::collections::VecDeque;

type Vertex = usize;
type ListOfEdges = Vec<(Vertex, Vertex)>;
type AdjacencyLists = Vec<Vec<Vertex>>;
struct Graph {
    n: usize,
    outedges: AdjacencyLists,
}

// impl functions for Graph to make directed graph
impl Graph {
    fn add_directed_edges(&mut self, edges:&ListOfEdges) {
        for (u,v ) in edges {
            self.outedges[*u].push(*v);
        }
    }
    fn sort_graph_lists(&mut self) {
        for l in self.outedges.iter_mut(){
            l.sort();
        }
    }
    fn create_directed(n: usize, edges: &ListOfEdges) -> Graph{
        let mut g = Graph{n,outedges:vec![vec![];n]};
        g.add_directed_edges(edges);
        g.sort_graph_lists();
        g
    }
}

// function to get n for Graph
fn node_count(path: &str) -> usize {
    let mut count: usize = 0;
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
    for (i, j) in data{
        if j > count{
            count = j;
        }
    }
    return count+1;
}
fn main() {

    // using reader to read data into "roadnetwork"
    let mut road_edges = reader::read_txt("roadNetCAProject.txt");
    road_edges.sort();

    // node_count should be equal to 1971280+1=1971281
    let n = node_count("roadNetCAProject.txt");

    let graph = Graph::create_directed(n, &road_edges);

    // these are dead ends in the road
    // not really used, but good to have, since they pretty much have 0 edges and can mess up iteration
    let mut end_points: Vec<usize> = Vec::new();
    for (i, j) in graph.outedges.iter().enumerate(){
        if j.len() == 0{
            end_points.push(i);
        }
    }

    // finds the overall average distance from a vertex to every other vertex in the CA road network graph
    fn average_distances() -> usize{
        let mut road_edges = reader::read_txt("roadNetCAProject.txt");
        road_edges.sort();
    
        let n = node_count("roadNetCAProject.txt");
    
        let graph = Graph::create_directed(n, &road_edges);
        let mut ran_sample: Vec<usize> = Vec::new();
        
        // random sampling
        // the 2000 sample is randomly selected thus represents the population
        let sample_count = 2000;
        for _ in 0..sample_count{
            let sample = random::sample();
            ran_sample.push(sample);
        }

        // average distances via breadth first search
        // each randomly selected vertex's average distance to every other vertex in the graph

        // sample_average_dis vector holds the format of 
        // (vertex, its average distance to every other vertex in the graph)
        let mut sample_average_dis: Vec<(usize, usize)> = Vec::new();
        for vtx in ran_sample{
            let start = vtx;
            let mut distance: Vec<Option<usize>> = vec![None;graph.n];
            distance[start] = Some(0);
            let mut queue: VecDeque<Vertex> = VecDeque::new();
            queue.push_back(start);
    
            while let Some(v) = queue.pop_front() {
                for i in graph.outedges[v].iter(){
                    if let None = distance[*i] {
                        distance[*i] = Some(distance[v].unwrap()+1);
                        queue.push_back(*i);
                    }   
                }
            }

            // I take the vertex's all distances to every other node on the graph
            // sum the distances then divide by count
            // push that node and its average distance to every other node into a vector for storage.
            let mut total_dis:usize = 0;
            let mut temp_count: usize = 0;
            for v in 0..graph.n{
                temp_count += 1;
                if distance[v] != None{
                    total_dis += distance[v].unwrap();
                }
            }
            let aver_dis = total_dis/temp_count;
            // println!("Vertex {} 's average distance to every other vertex is {}", start, aver_dis);
            sample_average_dis.push((start, aver_dis));
        }
    
        let mut average_travel_distance: usize = 0;
        for (_ss, jj) in sample_average_dis{
            average_travel_distance += jj;
        }
        let total_aver_travel = average_travel_distance/sample_count;
        println!
        ("The overall average distance from a node to every other node is {:?}", total_aver_travel);
        total_aver_travel
    }

    // centrality
    // finding top 50 nodes with highest degree
    // higher degree = more importance, as the vertex can be a important downtown road intersection
    // returns the percent of top 50 center nodes with average distance to every other node less than
    // overall average distance to every other node from average_distance()
    fn centrality(){
        let total_average_dis: usize = 305;
        let mut good_distance: f64 = 0.0;
        let mut road_edges = reader::read_txt("roadNetCAProject.txt");
        road_edges.sort();

        let n = node_count("roadNetCAProject.txt");

        let graph = Graph::create_directed(n, &road_edges);
        let mut centrality_measure: Vec<(usize, usize)> = Vec::new();
        for (node, edges) in graph.outedges.iter().enumerate(){
            centrality_measure.push((edges.len(), node));
        }
        centrality_measure.sort();
        centrality_measure.reverse();
    
        let mut fifty = 0;
        println!("Top 50 nodes with highest degree");
        for (xx, yy) in centrality_measure{
            if fifty < 51{
                fifty += 1;
                let start = yy;
                let mut distance: Vec<Option<usize>> = vec![None;graph.n];
                distance[start] = Some(0);
                let mut queue: VecDeque<Vertex> = VecDeque::new();
                queue.push_back(start);
        
                while let Some(v) = queue.pop_front() {
                    for i in graph.outedges[v].iter(){
                            if let None = distance[*i] {
                                distance[*i] = Some(distance[v].unwrap()+1);
                                queue.push_back(*i);
                        }   
                    }
                }
                let mut total_dis:usize = 0;
                let mut temp_count: usize = 0;
                for v in 0..graph.n{
                    temp_count += 1;
                    if distance[v] != None{
                        total_dis += distance[v].unwrap();
                    }
                }
                let aver_dis = total_dis/temp_count;
                if total_average_dis > aver_dis{
                    good_distance += 1.0;
                }
                println!("degree: {:?}, node: {:?}, average distance to every other node: {:?}", xx, yy, aver_dis);
            }
        }
        let percentage = good_distance/50.0*100.0;
        println!("percent of top 50 center nodes that has lower /
                 average distance than overall average distance is {:?} % ", percentage);
    }

    // a useful function that allows me to see the distance between individual nodes.
    fn distance_between(str:usize, end:usize){
        let mut road_edges = reader::read_txt("roadNetCAProject.txt");
        road_edges.sort();

        let n = node_count("roadNetCAProject.txt");

        let graph = Graph::create_directed(n, &road_edges);
        let start = str;
        let mut distance: Vec<Option<usize>> = vec![None;graph.n];
        distance[start] = Some(0);
        let mut queue: VecDeque<Vertex> = VecDeque::new();
        queue.push_back(start);
    
        while let Some(v) = queue.pop_front() {
            for i in graph.outedges[v].iter(){
                if let None = distance[*i] {
                    distance[*i] = Some(distance[v].unwrap()+1);
                    queue.push_back(*i);
                }   
            }
        }
    
        let distance_between = distance[end].unwrap();
        println!("{:?}", distance_between);

    }

    // average_distances() takes roughly 2 minutes to run
    // use cargo --release
    average_distances();
    centrality();
    
}
    // 2 tests in total:
    // test 1 is going to see if average_distance() gives a distance 
    // within range of all possible average distances.
    // takes almost 2 minutes to run
    #[test]
    fn test_distance(){
        // after running average_distance() 10 times
        // I got different values each time, since it is random sampling
        // the average was roughly 305
        // I am not repeating the function here to save time.
        let rough_total_aver_dis:usize = 305;

        let mut road_edges = reader::read_txt("roadNetCAProject.txt");
        road_edges.sort();
    
        let n = node_count("roadNetCAProject.txt");
    
        let graph = Graph::create_directed(n, &road_edges);
        let mut ran_sample: Vec<usize> = Vec::new();
        
        let sample_count = 2000;
        for _ in 0..sample_count{
            let sample = random::sample();
            ran_sample.push(sample);
        }

        let mut sample_average_dis: Vec<usize> = Vec::new();
        for vtx in ran_sample{
            let start = vtx;
            let mut distance: Vec<Option<usize>> = vec![None;graph.n];
            distance[start] = Some(0);
            let mut queue: VecDeque<Vertex> = VecDeque::new();
            queue.push_back(start);
    
            while let Some(v) = queue.pop_front() {
                for i in graph.outedges[v].iter(){
                    if let None = distance[*i] {
                        distance[*i] = Some(distance[v].unwrap()+1);
                        queue.push_back(*i);
                    }   
                }
            }

            let mut total_dis:usize = 0;
            let mut temp_count: usize = 0;
            for v in 0..graph.n{
                temp_count += 1;
                if distance[v] != None{
                    total_dis += distance[v].unwrap();
                }
            }
            let aver_dis = total_dis/temp_count;
            sample_average_dis.push(aver_dis);
        }
        let max = sample_average_dis.iter().max().unwrap();
        let min = sample_average_dis.iter().min().unwrap();

        if rough_total_aver_dis <= *max && rough_total_aver_dis >= *min{
            assert_eq!(1, 1);
        } else {
            assert_eq!(1, 2);
        }

    }

    // test 2 tests to see if the highest centrality degree
    // from centrality() matches the max value in a vector of all number of edges in the graph
    // centrality gives 12 has highest degree
    #[test]
    fn test_centrality(){
        let most_central:usize = 12;

        let mut road_edges = reader::read_txt("roadNetCAProject.txt");
        road_edges.sort();

        let n = node_count("roadNetCAProject.txt");

        let graph = Graph::create_directed(n, &road_edges);
        let mut centrality_measure: Vec<usize> = Vec::new();
        for (node, edges) in graph.outedges.iter().enumerate(){
            centrality_measure.push(edges.len());
        }

        let max_degree = centrality_measure.iter().max().unwrap();
        assert_eq!(max_degree, &most_central);
    }

