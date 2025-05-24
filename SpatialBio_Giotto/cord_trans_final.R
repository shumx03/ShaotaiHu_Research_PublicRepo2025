### cord_trans_final Shaotai Hu and Junxiang Xu ###
### Path setup ###
python_path = "/path/python"

library(Giotto)
library(data.table)

data_path = '/Users/vis_dir'
results_folder = '/Users/new_results'
poly_path = '/Users/###'

instrs = createGiottoInstructions(
  save_dir = results_folder,
  save_plot = TRUE,
  show_plot = TRUE,
  return_plot = FALSE, 
  python_path = python_path
)

### getting cell meta data from visium_object (assuming clustering is done on visium_object) ###
#cell_meta = pDataDT(visium_object)

### Target ###
visium_dir = data_path
LMD_dir = "/Users/###.jpg"
LMD_gimg = createGiottoLargeImage(LMD_dir)

### Source ###
g <- createGiottoVisiumObject(visium_dir = visium_dir,
                               gene_column_index = 2,
                               png_name = '###.png')

### Load the polygons ###
polyselection = data.table::fread(file = file.path(poly_path, '###.txt'))

### Create and add Giotto polygon information ###
my_polyselection <- createGiottoPolygonsFromDfr(polyselection, 
                                                name = 'selections')

g <- addGiottoPolygons(gobject = g,
                                 gpolygons = list(my_polyselection))

g <- addPolygonCells(g)

gimg = getGiottoImage(g)

### Pick your landmarks ###
landmarks <- interactiveLandmarkSelection(gimg, LMD_gimg)
#affine_mtx <- calculateAffineMatrixFromLandmarks(landmarks[[1]],landmarks[[2]])

### Apply transformation ###
g_transformed <- affine(g,affine_mtx,pre_multiply = TRUE)

g_fin <- addGiottoLargeImage(gobject = g_transformed, largeImages = list('LMD' = LMD_gimg))

### Look at landmark results ###
spatPlot2D(g_fin, show_image = T, cell_color = 'in_tissue', point_alpha = 0.3, return_plot = T)

### merge cell_meta to meta data from g_fin for visualization###
meta_gfin = pDataDT(g_fin)

merged_dt <- merge(cell_meta, meta_gfin, by = "cell_ID")

g_fin <- setCellMetadata(g_fin, x = createCellMetaObj(merged_dt))
copy_gfin = g_fin

new_gtrans = setCellMetadata(g_transformed, x = createCellMetaObj(merged_dt))

### Visualizing transformed polygons on LMD ###
poly2 = spatPlot2D(g_fin, image_name = 'image', cell_color = 'Kniche', point_alpha = 1, point_size = 2, coord_fix_ratio = 1, show_image = TRUE)
plotPolygons(g_fin, x = poly2)

### Visualizing transformed polygons on H&E ###
#poly3 = spatPlot2D(new_gtrans, image_name = 'image', cell_color = 'Kniche', point_alpha = 1, point_size = 2, coord_fix_ratio = 1, show_image = TRUE)
#plotPolygons(new_gtrans, x = poly3)

### Saving transformed polygons ###
final_polys = getPolygonInfo(g_fin, polygon_name= 'selections', return_giottoPolygon = TRUE)
df_poly = GiottoClass:::as.data.table.giottoPolygon(final_polys,geom = "XY")
df_poly[, c("geom", "part", "hole") := NULL]
setnames(df_poly, "poly_ID", "name")
data.table::fwrite(df_poly, file = file.path(results_folder, '###_new.txt'))

### Quick test on the transformed polygons ###
my_polygon_coordinates = data.table::fread(file = file.path(results_folder, '###_better.txt'))

extractedpolysnew <- createGiottoPolygonsFromDfr(my_polygon_coordinates,
                                                 name = "newchecking",
                                                 calc_centroids = TRUE)

copy_gfin<- addGiottoPolygons(gobject = copy_gfin,
                              gpolygons = list(extractedpolysnew))


poly10 = spatPlot2D(copy_gfin, point_alpha = 0, show_image = TRUE)

plotPolygons(copy_gfin, x = poly10, polygon_name = "newchecking")