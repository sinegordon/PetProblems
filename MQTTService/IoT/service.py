import paho.mqtt.subscribe as subscribe
from pymongo import MongoClient
import time
import json


config = json.load(open('./iot_config.json'))
client = MongoClient(config['host'], config['port'])
db = client[config['db']]
collection = db[config['collection']]

def on_message_print(client, userdata, message):
    try:
        msg = (message.payload).decode("utf-8")
        json_data = {'timestamp': round(time.time()), 'message': msg}
        print(f'Topic - {message.topic}. Message - {json.dumps(json_data)}.')
        transaction_id = collection.insert_one(json_data).inserted_id
        print(f'Inserted_id - {transaction_id}.')
    except Exception as ex:
        print(str(ex))


subscribe.callback(on_message_print, config["mqtt_topic"], hostname=config["mqtt_host"])

while True:
    time.sleep(1)