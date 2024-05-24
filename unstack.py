#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 24 08:41:57 2024

@author: aneesha
"""

import rasterio

def separate_bands(input_file, output_prefix):
    # Open the multi-band file
    with rasterio.open(input_file) as src:
        for i in range(1, src.count + 1):
            # Read the current band
            band = src.read(i)
            # Update the profile for single band
            profile = src.profile
            profile.update(count=1)

            # Define the output file name
            output_file = f"{output_prefix}_band{i}.tif"

            # Write the current band to a new file
            with rasterio.open(output_file, 'w', **profile) as dst:
                dst.write(band, 1)

            print(f"Band {i} written to {output_file}")

if __name__ == "__main__":
    input_file = 'stacked_output.tif'
    output_prefix = 'separated_output'

    separate_bands(input_file, output_prefix)
    print("All bands have been separated and saved.")
