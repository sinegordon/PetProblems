#import paho.mqtt.subscribe as subscribe
import paho.mqtt.client as mqtt
from pymongo import MongoClient
import time
import json
import struct


config = json.load(open('./iot_config.json'))
mongo_client = MongoClient(config['mongo_host'], config['mongo_port'])
db = mongo_client[config['mongo_db']]
collection = db[config['mongo_collection']]
mqtt_client = mqtt.Client()


def on_message_print(message):
    try:
        msg = (message.payload).decode("utf-8")
        json_data = {'timestamp': round(time.time()), 'message': msg}
        print(f'Topic - {message.topic}. Message - {json.dumps(json_data)}.')
        transaction_id = collection.insert_one(json_data).inserted_id
        print(f'Inserted_id - {transaction_id}.')
    except Exception as ex:
        print(str(ex))


def on_message_time(message):
    try:
        msg = message.payload
        (message_id, client_id) = struct.unpack(">HI", msg)
        #client_id = int.from_bytes(msg[3:], byteorder='little', signed=False)
        #message_id = int.from_bytes(msg[0:2], byteorder='little', signed=False)
        print(f'Time request from client_id = {client_id}')
        json_data = {'timestamp': round(time.time()), 'client_id': client_id, 'message': msg.decode('utf-8','ignore')}
        print(f'Topic - {message.topic}. Message - {json.dumps(json_data)}.')
        transaction_id = collection.insert_one(json_data).inserted_id
        print(f'Inserted_id - {transaction_id}.')
        resp = struct.pack(">HI", message_id, round(time.time()))
        mqtt_client.publish(f'{config["mqtt_topic"]}/time/{client_id}/response', resp)
    except Exception as ex:
        print(str(ex))


def on_message(mosq, obj, message):
    print(f'Message {message.payload} to {message.topic}')
    if '/print' in message.topic:
        on_message_print(message)
    elif '/time/request' in message.topic:
        on_message_time(message)


def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {str(rc)}')
    client.subscribe('#')

#subscribe.callback(on_message_print, f'{config["mqtt_topic"]}/print', hostname=config["mqtt_host"])
#subscribe.callback(on_message_time, f'{config["mqtt_topic"]}/time/request', hostname=config["mqtt_host"])

mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.connect(config["mqtt_host"])
mqtt_client.loop_forever()
