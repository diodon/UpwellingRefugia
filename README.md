# Upwelling Refugia

This repo contains the necessary code to process hourly GBR4 hydro downscaled forecasts.

## Procedure

1. Slice the hourly data of one year to summer months. In this case I used 01JAN (time=0) - 15APR (time=2519) to give some room for longer summers in the future. This can be done with NCO tools:  `ncks -d time,0,2519 imput.nc ouput.nc`  

2. Produce a daily average fiel from hourly data for summer months. Use `python3 makeDailyAvg.py input.nc`. It will produce a `daily_...` file containinf the daily averages and a `mean_...` file which is the summer average

3. Grid the file into a regular grid for the GBR. This is the tricky part as the package xesfm is quite difficult to install due to some old dependencies. I don't know if this is still valid for newer releases of the package. Use `gridGBR4.py` to produce a regular gridded file. This code has some components that have to be run in sequence:  
    - Prepare the GBR4 with the function `prepareGBR`. Change dimension names, and squeeze the file. xesfm expecte i, j dimesions to be names as x, y
    - Create an output grid with the function `createGBR4grid`. In this case, I am using 0.04x0.04 cells bounded to lon/lat ([142.02,155.38],[-28.58,-7.41])
    - Create a regridder with the function `createReggrider`. It uses the cleaned GBR4 file and the regular grid we just created above
    - regrid the dataset: `nc_gridded = createRegridder(nc, outgrid)`
    - create file with 1D coordinates for each variable and fix names. Use the function `cleanGridded`
    
4. Produce the anomaly map. This is done by subtracting the longitudinal mean of every latitude to the each values of the transect. Use  
  
5. you can use NCO tools to clip the file or to concatenate multiple files into one (note: in the resulting files `time` is an unlimited dimension)


## Note

I am using a conda environment for the regridding process, which is provided on request (1.2 GB)


