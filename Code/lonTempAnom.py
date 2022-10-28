## Calculate longitunial temp anomaly

import sys
from datetime import date
import numpy as np
import xarray as xr

## fileName = '/media/eklein/T7blue/UpwellingForecast/summerDaily/kk.nc'
## outfileName = '/media/eklein/T7blue/UpwellingForecast/summerDaily/kkAnom.nc'
## fileYear = "2050"
fileName = sys.argv[1]
outfileName = sys.argv[2]

fileYear = fileName.split('.nc')[0][-4:]
year = int(fileYear)


with xr.open_dataset(fileName) as nc:
    ## define output array
    tempAnom = np.zeros([len(nc.lat), len(nc.lon)])
    latList = nc.lat.values
    lonList = nc.lon.values

    ## rename variable
    nc = nc.rename_vars({'__xarray_dataarray_variable__': 'temp'})
    ## replace zeros by nan
    nc = nc.where(nc.temp>0, np.nan, drop=False)

    ## loop over latitude
    for i in range(len(nc.lat)):
        lat0 = nc.lat[i].values
        temp0 = nc.temp.sel(lat=lat0)
        tempMean = np.nanmean(temp0)
        tempAnom[i,:] = temp0 - tempMean

    ## make dataarray
    da = xr.DataArray(tempAnom, coords=[latList, lonList], dims=["lat", "lon"])
    da = da.expand_dims({'time': 1})

    ds = xr.Dataset({'temp': nc.temp,
                     'tempAnom': da,
                     'year': year})

    ## var attrs
    ds.temp.attrs = {'long_name': "mean sea surface temperature",
                     'units': "degree Celsius"}
    ds.tempAnom.attrs = {'long_name': "sea surface temperature latitudinal anomaly",
                         'units': "degree Celsius"}

    ## Global attrs
    ds.attrs = {'title': "Longitudinal SST Anomaly",
                'description': "The sst anomaly is calculated over each latitudinal transect subtracting the transect mean. The base data is summer sst average for hourly sst data",
                'source_file': fileName.split("/")[-1],
                'year': fileYear,
                'creation_date': str(date.today())}

    ds.to_netcdf(outfileName, unlimited_dims='time')
