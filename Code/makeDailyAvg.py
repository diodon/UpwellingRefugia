## produce a daily average files using summer files form GBR4 forecast

import xarray as xr
import sys

fileName = sys.argv[1]
outFileName = 'daily_' + fileName
outFileNameMean = 'mean_' + fileName
print(fileName)

with xr.open_dataset(fileName) as nc:
    nc = nc.squeeze()
    gg = nc.groupby(nc.time.dt.dayofyear)
    ncDay = gg.mean('time')
    ncDay.temp.attrs = {'long_name': 'estimated sea surface temperature',
                        'comments': 'daily average from GBR4 Hydro hourly data'}
    ## make avegare map
    ncDayMean = ncDay.mean('dayofyear')

ncDay.to_netcdf(outFileName)
ncDayMean.to_netcdf(outFileNameMean)





