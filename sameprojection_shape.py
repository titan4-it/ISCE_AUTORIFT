from osgeo import gdal, gdalconst

def align_images(reference_file, input_file, output_file, no_data_value=0):
    # Open the reference file to get georeference information
    ref_ds = gdal.Open(reference_file, gdalconst.GA_ReadOnly)
    ref_geotransform = ref_ds.GetGeoTransform()
    ref_projection = ref_ds.GetProjection()
    ref_x_size = ref_ds.RasterXSize
    ref_y_size = ref_ds.RasterYSize
    ref_band_count = ref_ds.RasterCount
    ref_data_type = ref_ds.GetRasterBand(1).DataType

    # Open the input file to be aligned
    input_ds = gdal.Open(input_file, gdalconst.GA_ReadOnly)

    # Create the output file with the same size and data type as the reference file
    driver = gdal.GetDriverByName('GTiff')
    output_ds = driver.Create(output_file, ref_x_size, ref_y_size, ref_band_count, ref_data_type)

    # Set the georeference information to the output file
    output_ds.SetGeoTransform(ref_geotransform)
    output_ds.SetProjection(ref_projection)

    # Reproject the input image to match the reference image's georeference
    for i in range(1, ref_band_count + 1):
        output_band = output_ds.GetRasterBand(i)
        output_band.SetNoDataValue(no_data_value)
        gdal.ReprojectImage(input_ds, output_ds, None, None, gdalconst.GRA_NearestNeighbour)

    ref_ds = None
    input_ds = None
    output_ds = None

# Input files
reference_file = 'LC08_L2SP_07.TIF'
input_file = 'LC08_L2SP_25.TIF'
output_file = 'aligned_output.tif'

# Align images
align_images(reference_file, input_file, output_file, no_data_value=0)
