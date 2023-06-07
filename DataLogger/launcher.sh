#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/orangepi/Documents/DataLogging
sleep 1m
sudo python3 settime.py
sudo python3 LoggerMultiProcess.py > log$(date "+%H:%M").txt

logFile=$(ls -t * | head -1)
cp $logFile gpx_converter/datain.csv
cd gpx_converter
sudo python3 gpxcreator.py

cd ..
mkdir log$(date "+%d-%m")
mv $logFile log$(date "+%d-%m")
logFile="${logFile%.csv}.gpx"
mv "gpx_converter/output.gpx" log$(date "+%d-%m")/$logFile
cd /
sudo shutdown -h now