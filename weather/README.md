I added this to /etc/crontab to log the data every minute  
`* * * * * pi /home/pi/weather/weather_logger.py >> /home/pi/weather/weather_logger.log`  
then add this to generate the plot every 5 minutes, change the 5 to a 10 for 10 minutes if you'd like  
`*/5 * * * * pi /home/pi/weather/plot_weather.py >> /home/pi/weather/plot_weather.log`  
The data collection code is based off the example here:  
[git.uwaterloo.ca/s8weber/envsense/.../get_bme280.py](https://git.uwaterloo.ca/s8weber/envsense/-/blob/0f5fbc485d479482897d6cac5f147a8203cd214a/get_bme280.py)  

![](https://i.imgur.com/3bL5se7.png)  
[imgur link](https://imgur.com/a/gtaP7zo)
