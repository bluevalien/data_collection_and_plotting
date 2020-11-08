I added this to /etc/crontab to log the data every minute\n
`* * * * * pi /home/pi/weather/weather_logger.py >> /home/pi/weather/weather_logger.log`\n
then add this to generate the plot every 5 minutes, change the 5 to a 10 for 10 minutes if you'd like\n
`*/5 * * * * pi /home/pi/weather/plot_weather.py >> /home/pi/weather/plot_weather.log`\n
The data collection cose was based off the example here:\n
[git.uwaterloo.ca/s8weber/envsense/.../get_bme280.py](https://git.uwaterloo.ca/s8weber/envsense/-/blob/0f5fbc485d479482897d6cac5f147a8203cd214a/get_bme280.py)\n

