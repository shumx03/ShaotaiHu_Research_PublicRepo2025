### Polygon Coords to XML Junxiang Xu and Shaotai Hu ###
df <- read.csv("/Users/###")
results_folder <- '/Users/###'
df$y <- abs(df$y)

# Extract the cluster name 
df$cluster_name <- sub("_\\d+$", "", df$name)
cluster_names <- unique(df$cluster_name)

for (cluster_name in cluster_names) {
  cluster_data <- df[df$cluster_name == cluster_name, ]
  shape_names <- unique(cluster_data$name)
  shape_count <- length(shape_names)
  
  xml_output <- paste0("<ShapeCount>", shape_count, "</ShapeCount>\n")
  
  for (shape_name in shape_names) {
    shape_data <- cluster_data[cluster_data$name == shape_name, ]
    point_count <- nrow(shape_data)
    
    shape_tag <- paste0(shape_name)
    
    xml_output <- paste0(xml_output, "<", shape_tag, ">\n")
    xml_output <- paste0(xml_output, "<PointCount>", point_count, "</PointCount>\n")
    
    for (j in 1:point_count) {
      x_value <- shape_data$x[j]
      y_value <- shape_data$y[j]
      xml_output <- paste0(xml_output, "<X_", j, ">", x_value, "</X_", j, ">\n")
      xml_output <- paste0(xml_output, "<Y_", j, ">", y_value, "</Y_", j, ">\n")
    }

    xml_output <- paste0(xml_output, "</", shape_tag, ">\n")
  }
  
  writeLines(xml_output, con = file.path(results_folder, paste0(cluster_name, "_coords.xml")))
}

### for laser resection ###
### copy and paste this to the top of the xml ###
#<ImageData>
#<GlobalCoordinates>1</GlobalCoordinates>
#<X_CalibrationPoint_1>932</X_CalibrationPoint_1>
#<Y_CalibrationPoint_1>756</Y_CalibrationPoint_1>
#<X_CalibrationPoint_2>416</X_CalibrationPoint_2>
#<Y_CalibrationPoint_2>9081</Y_CalibrationPoint_2>
#<X_CalibrationPoint_3>7428</X_CalibrationPoint_3>
#<Y_CalibrationPoint_3>9145</Y_CalibrationPoint_3>

### copy and paste this to the end of the xml ###
#</ImageData>