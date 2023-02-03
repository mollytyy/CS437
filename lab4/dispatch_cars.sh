#!/bin/bash

python3 pub_emission.py --endpoint aazb9d7j4pzxg-ats.iot.us-east-2.amazonaws.com --thingName veh0 --vehicleID veh0 --vehicleCSV ./data2/vehicle0.csv &
python3 pub_emission.py --endpoint aazb9d7j4pzxg-ats.iot.us-east-2.amazonaws.com --thingName veh1 --vehicleID veh1 --vehicleCSV ./data2/vehicle1.csv &
python3 pub_emission.py --endpoint aazb9d7j4pzxg-ats.iot.us-east-2.amazonaws.com --thingName veh2 --vehicleID veh2 --vehicleCSV ./data2/vehicle2.csv &
python3 pub_emission.py --endpoint aazb9d7j4pzxg-ats.iot.us-east-2.amazonaws.com --thingName veh3 --vehicleID veh3 --vehicleCSV ./data2/vehicle3.csv &
python3 pub_emission.py --endpoint aazb9d7j4pzxg-ats.iot.us-east-2.amazonaws.com --thingName veh4 --vehicleID veh4 --vehicleCSV ./data2/vehicle4.csv &