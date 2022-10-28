# Upwelling Refugia

This repo contains the necessary code to process hourly GBR4 hydro downscaled forecasts

## Procedure

1. Slice the hourly data of one year to summer months. In this case I used 01JAN (time=0) - 15APR (time=2519) to give some room for longer summers in the future. This can be done with NCO tools:  `ncks -d time,0,2519 imput.nc ouput.nc`  

2. Produce a daily average fiel from hourly data for summer months. Use `python3 
