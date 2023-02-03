import json
import logging
import sys

import greengrasssdk

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

maxco2 = {"veh0":0, "veh1":0, "veh2":0, "veh3":0, "veh4":0}

# Counter
my_counter = 0
def lambda_handler(event, context):
    global my_counter
    #TODO1: Get your data
    vehicle_id = event.get('vehicle_id')
    co2 = float(event.get('vehicle_CO2'))

    #TODO2: Calculate max CO2 emission
    if float(maxco2[vehicle_id]) < co2:
        maxco2[vehicle_id] = co2

    #TODO3: Return the result
    client.publish(
        topic="lab4/" + vehicle_id + "/maxco2",
        payload=json.dumps(
            {vehicle_id: maxco2[vehicle_id]}
        ),
    )
    my_counter += 1

    return
