from time import sleep
from json import dumps, loads
from kafka import KafkaProducer
from kafka import KafkaConsumer
import random

#producer = KafkaProducer(bootstrap_servers=['hadoop1.libo.com:6667'],
#                         value_serializer=lambda x:
#                         dumps(x).encode('utf-8'))
#
#
#data = {'number' : random.randrange(1000)}
#print(f"Adding data to queue: {data}")
#producer.send('libo_test',value=data)

consumer = KafkaConsumer(
    'libo_test',
     bootstrap_servers=['hadoop1.libo.com:6667'],
     auto_offset_reset='latest',
     enable_auto_commit=True,
#     group_id='my-group',
     value_deserializer=lambda x: loads(x.decode('utf-8')))

for message in consumer:
    message = message.value
    print('Message read from queue {}'.format(message))
