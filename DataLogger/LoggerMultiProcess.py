import io
import pynmea2
import serial
import pytz
import os
import sys
import time
import smbus
import math
import csv
import threading
import multiprocessing
import queue
import logging

from bluedot import BlueDot

from imusensor.MPU9250 import MPU9250
from imusensor.filters import kalman

logger = logging.getLogger()
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

calibrationFile = "/home/orangepi/Documents/DataLogging/Calibration/calData.json"

address = 0x68
bus = smbus.SMBus(3)
imu = MPU9250.MPU9250(bus, address)
imu.loadCalibDataFromFile(calibrationFile)
logger.debug("calibration data loaded succesfully!")

imu.begin()

imu.setAccelRange("AccelRangeSelect8G")
imu.setSRD(1)
imu.setLowPassFilterFrequency("AccelLowPassFilter184")

epoch = time.time()
GPSfreq = 1
currTime = epoch
trainingTime = 0
roll, pitch, yaw, speed, longitude, latitude = "", "", "", "", "", ""
old_long, new_long, old_lat, new_lat = "", "", "", ""
distance, total_distance = 0, 0

boatInHands = False
boatCounter = 0
boatInWater = False

def GPS_thread(Vqueue, Longqueue, Latqueue):
	ser = serial.Serial(
		port = '/dev/ttyS0',
		baudrate = 9600,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS,
		timeout = 1
	)
	sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
	while True:
		try:
			line = sio.readline()
			array = line.split(",")
			msg = pynmea2.parse(line)

			if type(msg) == pynmea2.types.talker.RMC:

				status = msg.status

				if status == 'A':
					speedmps = float(array[7])*0.514444
					try:
						speedmin = int((500/speedmps)//60)
						speedsec = int((500/speedmps) %60)
					except ZeroDivisionError as e:
						speedmin = 0
						speedsec = 0

					try:
						Vqueue.put(speedmps, block = False)
					except:
						Vqueue.get()
						Vqueue.put(speedmps, block = False)
					try:
						Longqueue.put(msg.longitude, block = False)
					except:
						Longqueue.get()
						Longqueue.put(msg.longitude, block = False)
					try:
						Latqueue.put(msg.latitude, block = False)
					except:
						Latqueue.get()
						Latqueue.put(msg.latitude, block = False)

					#logger.debug('The current speed is {0}:{1}/500m or {2}m/s'.format(speedmin, speedsec, speedmps))
					#logger.debug('The current location is {0} ; {1}'.format(msg.longitude, msg.latitude))

		except serial.SerialException as e:
			#logger.debug('Device error: {}'.format(e))
			try:
				ser = serial.Serial(
					port = '/dev/ttyS0',
					baudrate = 9600,
					parity = serial.PARITY_NONE,
					stopbits = serial.STOPBITS_ONE,
					bytesize = serial.EIGHTBITS,
					timeout = 1
				)
				sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
			except:
				break
			continue
		except pynmea2.ParseError as e:
			#logger.debug('Parse error: {}'.format(e))
			continue
		except UnicodeDecodeError as e:
			#logger.debug('UnicodeDecodeError error: {}'.format(e))
			continue
		except:
			continue
		continue
	logger.debug("GPS terminated")


Vqueue = multiprocessing.Queue(maxsize=1)
Longqueue = multiprocessing.Queue(maxsize=1)
Latqueue = multiprocessing.Queue(maxsize=1)

logger.debug("ready to put the boat in the water!")

while not boatInWater:
	try:
		imu.readSensor()
	except TimeoutError as e:
		logger.debug('TimeoutError in imu: {0}'.format(e))
	except OSError as e:
		logger.debug('OSError: {0}'.format(e))
		imu = MPU9250.MPU9250(bus, address)
		imu.loadCalibDataFromFile(calibrationFile)
		logger.debug("calibration data loaded succesfully!")
	sensorfusion = kalman.Kalman()
	imu.computeOrientation()
	sensorfusion.roll = imu.roll
	sensorfusion.pitch = imu.pitch
	sensorfusion.yaw = imu.yaw

	count = 0
	epoch = time.time()

	dt = epoch - currTime
	currTime = epoch

	sensorfusion.computeAndUpdateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2],\
												imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)
	
	if not boatInHands and (sensorfusion.roll > 170 or sensorfusion.roll < -170):
		boatCounter = boatCounter + 1
		#logger.debug("boat is still in trestles, counter: {}".format(boatCounter))
		if boatCounter == 100:
			boatInHands = True
			boatCounter = 0
			logger.debug("boat is above the head")
	elif not boatInHands: boatCounter = 0

	
	if boatInHands and ( 0 < sensorfusion.roll < 30 or 0 > sensorfusion.roll > -30):
		boatCounter = boatCounter + 1
		#logger.debug("boat is still above the head, counter: {}".format(boatCounter))
		if boatCounter == 100:
			boatInWater = True
			boatCounter = 0
			logger.debug("boat is in the water! Training starts in 2 minutes!")
	elif boatInHands: boatCounter = 0

gps = multiprocessing.Process(target=GPS_thread, args = (Vqueue, Longqueue, Latqueue))
gps.start()

waitingTime = 0
logger.debug(120)
for i in range(120):
	continue
	time.sleep(1)
	waitingTime = waitingTime + 1
	logger.debug(120-waitingTime)

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%a_%d.%m_%Hu%M", named_tuple)
logger.debug("Training started on {0}.".format(time_string))

filename = os.path.join("data_" + time_string + ".csv")
f = open(filename, "w")
f.write("x,y,z,roll,pitch,yaw,speed,longitude,latitude,distance,time\n")

currtime = time.time()

while boatInWater:
	try:
		imu.readSensor()
	except TimeoutError as e:
		logger.debug('TimeoutError in imu: {0}'.format(e))
	except OSError as e:
		logger.debug('OSError: {0}'.format(e))
		imu = MPU9250.MPU9250(bus, address)
		imu.loadCalibDataFromFile(calibrationFile)
		logger.debug("calibration data loaded succesfully!")
	sensorfusion = kalman.Kalman()
	imu.computeOrientation()
	sensorfusion.roll = imu.roll
	sensorfusion.pitch = imu.pitch
	sensorfusion.yaw = imu.yaw

	count = 0
	epoch = time.time()

	dt = epoch - currTime
	currTime = epoch
	trainingTime = trainingTime + dt

	sensorfusion.computeAndUpdateRollPitchYaw(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], imu.GyroVals[0], imu.GyroVals[1], imu.GyroVals[2],\
												imu.MagVals[0], imu.MagVals[1], imu.MagVals[2], dt)
	
	if not Vqueue.empty() and not Longqueue.empty() and not Latqueue.empty():
		speed, new_long, new_lat = Vqueue.get(), Longqueue.get(), Latqueue.get()
		try:
			distance = math.acos(math.sin(math.radians(float(old_lat)))*math.sin(math.radians(float(new_lat)))+math.cos(math.radians(float(old_lat)))*math.cos(math.radians(float(new_lat)))*math.cos(math.radians(float(new_long))-math.radians(float(old_long))))*6371000
			total_distance = total_distance + distance
		except ValueError as e:
			logger.debug(e)
		old_long, old_lat = new_long, new_lat
		longitude, latitude = new_long, new_lat
		#logger.debug("total distance is: {0}m and distance is: {1}m".format(total_distance, distance))
		#logger.debug('got long and lat from queue: {0:.2f},{1:.2f} at: {2}'.format(longitude, latitude, time.strftime("%Hu%M", time.localtime())))

	f.write("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10}\n".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2], roll, pitch, yaw, speed, longitude, latitude, total_distance, trainingTime))
	roll, pitch, yaw, speed, longitude, latitude, distance = "", "", "", "", "", "", ""
	
	roll, pitch, yaw = sensorfusion.roll, sensorfusion.pitch, sensorfusion.yaw

	if not gps.is_alive():
		gps = threading.Thread(target=GPS_thread, args = (Vqueue, Longqueue, Latqueue))
		gps.start()

	if sensorfusion.roll > 170 or sensorfusion.roll < -170:
		boatCounter = boatCounter + 1
		#logger.debug("boat is still in the water, counter: {}".format(boatCounter))
		if boatCounter == 30:
			boatInWater = False
			logger.debug("boat is above the head!")
	else: boatCounter = 0

named_tuple = time.localtime() # get struct_time
time_string = time.strftime("%a_%d.%m_%Hu%M", named_tuple)
logger.debug("Training stopped on {0}.".format(time_string))
gps.kill()

f.close()