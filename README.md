# dscovr-epic-wallpaper
Tools for fetching NASA's DSCOVR: EPIC Earth pictures and set your Windows desktop wallpaper.

NASA EPIC::DSCOVR Project : https://epic.gsfc.nasa.gov

Based on API Version 2.0 : https://epic.gsfc.nasa.gov/about/api

NASA's DSCOVR: EPIC (Earth Polychromatic Imaging Camera) project is publishing every day a dozen pictures of earth (2-3 days back)
I thought it could be fun to refresh my Windows Desktop Wallpaper using the latests images published, using the image matching current time/position of earth towards the sun.
Basically at 00:00 UTC West Pacific is facing sun, 12:00 UTC western Europe is facing Sun, and 23:00 UTC east pacific is facing sun.
If you want the same setup, configure you Windows scheduler to run hourly with the following parameters or use the sample batch file in the project.

```
main.py --wallpaper --now
```

# Runtime
Tested on Windows-7-6.1.7601-SP1 - Python Version: Python 2.7.13 (v2.7.13:a06454b1afa1, Dec 17 2016, 20:42:59) [MSC v.1500 32 bit (Intel)] on win32

## Requirements
* python.dateutil
* requests

# Usage
 
```
main.py [-h] [--debug] [--collection {natural,enhanced}] [--date DATE]
               [--position {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23} | --now]
               [--wallpaper] [--proxy-host PROXY_HOST]
               [--proxy-login PROXY_LOGIN] [--proxy-password PROXY_PASSWORD]

```

##optional arguments:
```
  -h, --help            show this help message and exit
  --debug               Enable verbose logging
  --collection {natural,enhanced}
                        Select collection of images. 'natural' or 'enhanced'
                        Default : if not specified, lookup form natural image
                        collection
  --date DATE           [Optional] Date of the picture Default : if not
                        specified, this is the latest day available
  --position {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23}
                        [Optional] Earth position (in Universal Time 0-23))
                        Default : if not specified, lookup the latest position
  --now                 [Optional] Reflect earth position as current hour
  --wallpaper           [Optional] Update Windows Desktop Wallpaper
  --proxy-host PROXY_HOST
                        [Optional] Proxy host:port

  --proxy-login PROXY_LOGIN
                        [Optional] Proxy Login
  --proxy-password PROXY_PASSWORD
                        [Optional] Proxy Password
 
```

#Specifications
## image location
Downloaded images are saved under your home folder 
```
~/.dscovr-epic-wallpaper/images
```
Notes : 
* There is no mechanism implemented to clean your image folder so if you schedule your script to run automatically you might want to clean it time to time. 

## log location
Logs are saved under your home folder
```
~/.dscovr-epic-wallpaper/logs
```
Notes : 
* There is no mechanism implemented to clean your image folder so if you schedule your script to run automatically you might want to clean it time to time. 
* without --debug flag, only errors and exceptions are logged

# Known issues
n/a

# References
Project forked from <https://github.com/russss/dscovr-epic>

Note :
I do not support the tweet functionality inherited from the project above but dit not remove it if you want to use it or fork it.