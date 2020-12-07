import rasterio
from rasterio import plot
import matplotlib.pyplot as plt
import numpy as np
from osgeo import gdal
import os

infn = './input/ayuso_rededge.tif'
outfn = './output/ndvi.tif'

img = rasterio.open(infn)
plot.show(img)


def openRaster(fn, access=0):
    ds = gdal.Open(fn, access)
    if ds is None:
        print("Error opening Raster dataset")
    return ds

def getRasterBand(fn, band=1, access=0):
    ds = openRaster(fn, access)
    band = ds.GetRasterBand(band).ReadAsArray()
    return band
    
def createRasterFromTemplate(fn, ds, data, ndv=-9999.0, driverFmt="GTiff"):
    driver = gdal.GetDriverByName(driverFmt)
    outds = driver.Create(fn, xsize=ds.RasterXSize, ysize=ds.RasterYSize, bands=1, eType=gdal.GDT_Float32)
    outds.SetGeoTransform(ds.GetGeoTransform())
    outds.SetProjection(ds.GetProjection())
    outds.GetRasterBand(1).SetNoDataValue(ndv)
    outds.GetRasterBand(1).WriteArray(data)
    outds = None
    ds = None
    
def ndvi(nirband, redband, ndv=-9999.0):
    nirband[nirband < 0] = np.nan
    nirband[nirband > 10000] = np.nan
    nirband[redband < 0] = np.nan
    nirband[redband > 10000] = np.nan
    ndviband = (nirband-redband)/(nirband+redband)
    ndviband[np.isnan(ndviband)] = ndv
    return ndviband

# Plot redband vs nirband
redband = getRasterBand(infn, 3)
nirband = getRasterBand(infn, 5)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6))
plot.show(redband, ax=ax1, cmap='Blues')
plot.show(nirband, ax=ax2, cmap='Blues')
fig.tight_layout()
plt.show()

ndviband = ndvi(nirband, redband)
createRasterFromTemplate(outfn, gdal.Open(infn), ndviband)

img = rasterio.open('./output/ndvi.tif')
plot.show(img)