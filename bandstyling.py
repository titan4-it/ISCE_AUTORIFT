#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 29 17:39:02 2024

@author: aneesha
"""

import numpy as np
import matplotlib.pyplot as plt
import rasterio

# Paths to the TIFF files
band1_path = 'separated_output_band1.tif'
band2_path = 'separated_output_band2.tif'
band3_path = 'separated_output_band3.tif' 
band4_path = 'separated_output_band4.tif'  

# Function to read and normalize a band
def read_and_normalize_band(file_path, vmin, vmax):
    with rasterio.open(file_path) as band:
        data = band.read(1)
    data = np.where(data == data.min(), np.nan, data)  # Replace min value with NaN to avoid issues with normalization
    data = (data - np.nanmin(data)) / (np.nanmax(data) - np.nanmin(data))
    data = data * (vmax - vmin) + vmin  # Normalize to the specific range
    return data
def read_and_normalize_band_ip(file_path, vmin, vmax):
    with rasterio.open(file_path) as band:
        data = band.read(1)
    data = (data - data.min()) / (data.max() - data.min())
    data = data * (vmax - vmin) + vmin  # Normalize to the specific range
    return data
# Read and normalize each band with specific limits
band1_data = read_and_normalize_band(band1_path, -5, 5)
band2_data = read_and_normalize_band(band2_path, -5, 5)
band3_data = read_and_normalize_band_ip(band3_path, 0, 1)  # Light interpolation mask
band4_data = read_and_normalize_band(band4_path, 32, 64)  # Chip size used

# Plot the individual bands
fig, axes = plt.subplots(2, 2, figsize=(18, 12))

# Common properties
extent = [-500000, -10000, -1800000, -1500000]

# Plot Band 1 with the specified title
cax1 = axes[0, 0].imshow(band1_data, cmap='RdYlBu', extent=extent, vmin=-5, vmax=5)
axes[0, 0].set_title('(a) Estimated horizontal pixel displacement (in pixels)')
axes[0, 0].axis('on')
fig.colorbar(cax1, ax=axes[0, 0], orientation='vertical')

# Plot Band 2 with the specified title
cax2 = axes[0, 1].imshow(band2_data, cmap='RdYlBu', extent=extent, vmin=-5, vmax=5)
axes[0, 1].set_title('(b) Estimated vertical pixel displacement (in pixels)')
axes[0, 1].axis('on')
fig.colorbar(cax2, ax=axes[0, 1], orientation='vertical')

# Plot Band 3 as a binary mask
cax3 = axes[1, 0].imshow(band3_data, cmap='binary', extent=extent)
axes[1, 0].set_title('(d) Light interpolation mask')
axes[1, 0].axis('on')
fig.colorbar(cax3, ax=axes[1, 0], orientation='vertical')
# Plot Band 4 with the specified title
cax4 = axes[1, 1].imshow(band4_data, cmap='RdYlBu', extent=extent, vmin=32, vmax=64)
axes[1, 1].set_title('(c) Chip size used (in pixels)')
axes[1, 1].axis('on')
fig.colorbar(cax4, ax=axes[1, 1], orientation='vertical')

# Set the same limits for x-axis and y-axis
for ax in axes.flat:
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])

plt.tight_layout()
plt.show()
