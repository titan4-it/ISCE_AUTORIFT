#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 08:41:00 2024

@author: aneesha
"""

import rasterio
from rasterio.enums import Resampling
from rasterio.warp import calculate_default_transform, reproject, aligned_target
from rasterio.windows import from_bounds
import numpy as np

def resample_and_crop(src, ref, dst_path):
    # Calculate the transform, width, and height of the target image
    transform, width, height = calculate_default_transform(
        src.crs, ref.crs, ref.width, ref.height, *ref.bounds
    )
    kwargs = src.meta.copy()
    kwargs.update({
        'crs': ref.crs,
        'transform': transform,
        'width': width,
        'height': height
    })

    # Create an array to hold the resampled data
    data = np.zeros((src.count, height, width), dtype=src.dtypes[0])

    # Resample the source image to match the reference image
    for i in range(1, src.count + 1):
        reproject(
            source=rasterio.band(src, i),
            destination=data[i-1],
            src_transform=src.transform,
            src_crs=src.crs,
            dst_transform=transform,
            dst_crs=ref.crs,
            resampling=Resampling.bilinear
        )

    # Write the resampled and cropped output
    with rasterio.open(dst_path, 'w', **kwargs) as dst:
        dst.write(data)

def stack_geotiff(input1, input2, output):
    # Open the first input file
    with rasterio.open(input1) as src1:
        band1 = src1.read(1)  # Read the first band
        profile = src1.profile  # Get the profile (metadata) of the first image

    # Open the second input file and resample it to match the first
    with rasterio.open(input2) as src2:
        resampled_input2 = 'resampled_' + input2
        resample_and_crop(src2, src1, resampled_input2)
        with rasterio.open(resampled_input2) as resampled_src2:
            band2 = resampled_src2.read(1)  # Read the resampled first band

    # Update the profile to reflect the number of layers
    profile.update(count=2)

    # Write the stacked output
    with rasterio.open(output, 'w', **profile) as dst:
        dst.write(band1, 1)  # Write the first band
        dst.write(band2, 2)  # Write the second band

if __name__ == "__main__":
    input_file_1 = 'S2A_MSIL2A_20240524T100031_N0510_R122_T33TUG_20240524T155653_resampled-001.tif'
    input_file_2 = 'S2A_MSIL1C_20240524T100031_N0510_R122_T33TUG_20240524T134121_resampled-002.tif'
    output_file = 'stacked_output.tif'

    stack_geotiff(input_file_1, input_file_2, output_file)
    print(f'Stacked image saved as {output_file}')
