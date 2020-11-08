#!/usr/bin/python3
import bme280
import smbus2
import time

port = 1
address = 0x76
bus = smbus2.SMBus(port)

calibration_params = bme280.load_calibration_params(bus, address)

# the sample method will take a single reading and return a
# compensated_reading object
data = bme280.sample(bus, address, calibration_params)

## the compensated_reading class has the following attributes
#print(data.id)
#print(data.timestamp)
#print(data.temperature)
#print(data.pressure)
#print(data.humidity)

# there is a handy string representation too
#print(data)

with open('/home/pi/weather_log.csv', 'a') as csv_log:
    csv_log.write(
        "{},{},{},{},{}\n".format(
        round(time.time(),0),
        0, #exit code
        round(data.temperature, 2),
        round(data.humidity, 2),
        round(data.pressure, 2)
        ))

