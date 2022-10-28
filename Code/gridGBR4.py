'''
To regridd GBR4 files

1. prepare the GBR4 with prepareGBR
2. create an output grid with createGBR4grid
3. create a regridder with createReggrider
4. regrid the dataset
    nc_gridded = createRegridder(nc, outgrid)
5. create file with 1D coordinates for each variable
6. use GBR4clip.sh to clip the resulting file
'''
import rioxarray
import rasterio
import xarray as xr
import xesmf as xe
import argparse

def makeDaily(nc):
    '''
    aggregate the hourly file into daily averages
    :param nc: input file with temp as variable
    :return: dataset aggregated by day
    '''
    gg = nc.groupby(nc.time.dt.dayofyear)
    return gg.mean()


def prepareGBR4(nc):
## Prepare GBR4 curviliniar gridded netCDF files to regrid
## 1. rename x_centre and y_centre to lon, lat
## 2. replace lon/lat 0 values by NaN
## 3. create coordinates
    nc = nc.squeeze()
    nc = nc.where(nc.latitude<0, drop=True)
    nc = nc.where(nc.longitude>0, drop=True)
    nc = nc.assign_coords({'lon': nc.longitude, 'lat': nc.latitude})
    nc = nc.squeeze()
    nc = nc.rename({'i': 'x', 'j': 'y'})
    return nc

def createGBR4grid():
    ## create a regridder grid for GBR1
    return xe.util.grid_2d(142.02,155.38,0.04,-28.58,-7.41,0.04)


def createReggrider(nc, outGrid, reuse=True):
    ## create a regridder
    return xe.Regridder(nc, outGrid, 'bilinear', reuse_weights=reuse)


## extract one variable from the prepared dataset:
## dhw0m = nc.dhw_max_surf

## perform the gridding over the 1-variable data array
## dhw0m_gridded = regridder(dhw0m)


## now convert the 2D data + 2D coordinates files to 2d data + 1D coordinates
## nc is the gridded data array
## time is a dimension
def cleanGridded(nc):
    latitude = nc.lat[:,0]
    longitude = nc.lon[0,:]
    #time = nc.time
    dhw = nc.values
    ## build the dataset
    nc1D = xr.DataArray(dhw, coords=[latitude, longitude], dims=['lat', 'lon'])
    return nc1D





def extractVariable(nc, varname):
    ##nc is the already gridded dataset
    lon = nc1_gridded.lon[0,:].values
    lat = nc1_gridded.lat[:,0].values
    dhw = nc[varname].values

    dataArray = xr.DataArray(dhw,
                            coords={'lat':lat, 'lon':lon},
                            dims=["lat", "lon"])
    return dataArray




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Grid GBR4 file")
    parser.add_argument('-file', dest='fileName', help="name of GBR1 file", required=True)
    parser.add_argument('-var', dest='var', help="Name of the variable of interest", required=True)
    parser.add_argument('-out', dest='outfile', help="Name of the output file", required=True)
    args = parser.parse_args()

    nc = xr.open_dataset(args.fileName)
    nc1 = prepareGBR4(nc)
    outgrid = createGBR4grid()
    reggrider = createReggrider(nc1, outgrid)
    ncVar = nc1[args.var]
    ncVarg = reggrider(ncVar)
    ncVargc = cleanGridded(ncVarg)
    #ncVargc.rio.write_crs('EPSG:4326', inplace=True)
    ncVargc.to_netcdf(args.outfile)





