# Upwelling Refugia

This repo contains the necessary code to process hourly GBR4 hydro downscaled forecasts

## Procedure

1. Slice the hourly data of one year to summer months. In this case I used 01JAN (time=0) - 15APR (time=2519) to give some room for longer summers in the future. This can be done with NCO tools:  `ncks -d time,0,2519 imput.nc ouput.nc`  

2. Produce a daily average fiel from hourly data for summer months. Use `python3 makeDailyAvg.py input.nc`. It will produce a `daily_...` file containinf the daily averages and a `mean_...` file which is the summer average

3. Grid the file into a regular grid for the GBR. This is the tricky part as the package xesfm is quite difficult to install due to some old dependencies. I don't know if this is still valid for newer releases of the package. Use 
