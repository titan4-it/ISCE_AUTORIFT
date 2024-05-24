from osgeo import gdal

input_file = 'offset.tif'
output_files = ['band1.tif', 'band2.tif', 'band3.tif', 'band4.tif']

# Open the input dataset
dataset = gdal.Open(input_file)

# Get the georeferencing information from the input dataset
geotransform = dataset.GetGeoTransform()
projection = dataset.GetProjection()

for i in range(1, dataset.RasterCount + 1):
    band = dataset.GetRasterBand(i)
    band_data = band.ReadAsArray()

    # Create the output dataset with the same georeferencing information
    driver = gdal.GetDriverByName('GTiff')
    output_dataset = driver.Create(output_files[i-1], band.XSize, band.YSize, 1, band.DataType)
    
    # Set the geotransform and projection
    output_dataset.SetGeoTransform(geotransform)
    output_dataset.SetProjection(projection)
    
    # Write the band data to the output dataset
    output_band = output_dataset.GetRasterBand(1)
    output_band.WriteArray(band_data)

    # Flush the cache to write to disk
    output_dataset.FlushCache()

# Close the datasets
dataset = None
output_dataset = None
