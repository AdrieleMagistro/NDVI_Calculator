# NDVI_Calculator

## Initial Information
From the information in my possession, the image from which the **normalized difference vegetation index (NDVI)** must be extrapolated is a 5-band orthomosaic from a flight using a RedEdge-MX camera.

The specifications of the RedEdge-MX sensor are shown in the figure below, and can be consulted on the **MicaSense** web page at this link: 
https://micasense.com/rededge-mx/
![](https://github.com/AdrieleMagistro/terraview/blob/main/imgs/redEdge_specs.png)

The purpose of this task is to calculate the normalized difference vegetation index from a starting image acquired with the RedEdge-MX sensor. From Wikipedia: 
https://en.wikipedia.org/wiki/Normalized_difference_vegetation_index
it can be calculated using the following formula:

![equation](http://latex.codecogs.com/gif.latex?NDVI%3D%5Cfrac%7B(NIR-Red)%7D%7B(NIR+Red)%7D)

where **Red** and **NIR** stand for the spectral reflectance measurements acquired in the red (visible) and near-infrared regions, respectively.
In our case, following the order of the bands shown in the sensor specifications, Red is the **third band**, while near-IR is the **fifth band**.

## Input Image
The starting image is shown in the following figure.
![](https://github.com/AdrieleMagistro/terraview/blob/main/imgs/original.png)

## Red and NIR extrapolation
First of all, I extrapolated from the starting image the information contained in the Red and Near-IR bands using the following code.
```python
infn = './input/path'
outfn = './output/path'

def openRaster(fn, access=0):
    ds = gdal.Open(fn, access)
    if ds is None:
        print("Error opening Raster dataset")
    return ds

def getRasterBand(fn, band=1, access=0):
    ds = openRaster(fn, access)
    band = ds.GetRasterBand(band).ReadAsArray()
    return band
    
redband = getRasterBand(infn, 3)
nirband = getRasterBand(infn, 5)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6))
plot.show(redband, ax=ax1, cmap='Blues')
plot.show(nirband, ax=ax2, cmap='Blues')
fig.tight_layout()
```
The following image compares the two results obtained.
![](https://github.com/AdrieleMagistro/terraview/blob/main/imgs/red_vs_nir.png)

## Result
I calculated the NDVI and created the processed image using the **ndvi** and **createRasterFromTemplate** functions, as shown in the following code snippet.
```python
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
    
ndviband = ndvi(nirband, redband)
createRasterFromTemplate(outfn, gdal.Open(infn), ndviband)
```
Finally, I got the following image as requested by the Task.
![](https://github.com/AdrieleMagistro/terraview/blob/main/imgs/ndvi.png)

## QGIS Visualization
To make the result clearer, since the health of the plants can be related to NVDI in the way shown in the following image, I decided to use the QGIS Open Source Tool and choose a color scale that reflects the correlation previously described.
![](https://github.com/AdrieleMagistro/terraview/blob/main/imgs/plants_h.jpg)

The final result is shown in the following figure.
![](https://github.com/AdrieleMagistro/terraview/blob/main/imgs/qgis.png)
