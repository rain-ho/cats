### Taken from https://pypi.python.org/pypi/paho-mqtt
### Requires Paho-MQTT package, install by:
### pip install paho-mqtt

import paho.mqtt.client as mqtt
import sys
import subprocess
import time
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()
# Change accordingly to the MQTT Broker and topic you want to subscribe
# In the example it would be either "test.mosquitto.org" or "fd00::1" if
# running a mosquitto broker on your localhost
MQTT_URL         = "localhost"
MQTT_TOPIC_EVENT = "deec/evt/status"
#MQTT_TOPIC_CMD   = "deec/cmd/leds"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe(MQTT_TOPIC_EVENT)
    print("Subscribed to " + MQTT_TOPIC_EVENT)
    #lient.subscribe(MQTT_TOPIC_CMD)
    #print("Subscribed to " + MQTT_TOPIC_CMD)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    

    if isinstance(msg.payload, bytes):
        payload_str = msg.payload.decode("utf-8").strip()
    elif isinstance(msg.payload, str):
        payload_str = msg.payload.strip()
    else:
        print("Invalid payload type")
        return

    # Rest of your code...

    # Remove the opening and closing curly braces
    payload_str = payload_str[1:-1]

    # Split the key-value pairs by comma
    pairs = payload_str.split(',')

    # Create a dictionary to store the key-value pairs
    parsed_payload = {}

    # Iterate over the pairs, split them by colon, and store in the dictionary
    for pair in pairs:
        key, value = pair.split(':')
        parsed_payload[key.strip('"')] = float(value)

    # Access the values using the keys
    boardID = parsed_payload["board"]
    a_id = parsed_payload["a_id"]
    temp = parsed_payload["temp"]
    hum = parsed_payload["hum"]
    light_smoke = parsed_payload["light_smk"]


    print("a_id:", a_id)
    print("temp:", temp)
    print("hum:", hum)
    print("light_smk:", light_smoke)

    if int(boardID) == 1:
        subprocess.run(['./test_post', str(temp), str(hum), str(light_smoke)], capture_output=True, text=True)
    elif int(boardID) == 0:
        result = subprocess.run(['./post2', str(light_smoke)], capture_output=True, text=True)

    result = subprocess.run(['./testget'], capture_output=True, text=True)
    return_code = result.returncode
    return_code = int(return_code)
    print("RISK: "+ str(return_code))

    if ((return_code >= 35 and return_code < 68) or (return_code > 10000)):
        print (return_code)

        account_sid = os.environ.get(account_sid)
        auth_token = os.environ.get(auth_token)
        client = Client(account_sid, auth_token)

        message = client.messages.create(
          from_='+16183684908',
          body='Potential safety issue detected. \
                Check your APP for details. \
                https://cats-iot23.streamlit.app',
          to='YOUR_PHONE_NUMBER'
        )
        print("SMS")
        time.sleep(3 * 60)

















































  


    sys.stdout.write('\n')
    sys.stdout.flush()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

print("connecting to " + MQTT_URL)
client.connect(MQTT_URL, 1883, 60)
client.loop_forever()
