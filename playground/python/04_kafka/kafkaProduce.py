from time import sleep
from json import dumps, loads
from kafka import KafkaProducer
from kafka import KafkaConsumer
import random

producer = KafkaProducer(bootstrap_servers=['hadoop1.libo.com:6667'],
                         value_serializer=lambda x:
                         dumps(x).encode('utf-8'))


data = {'number' : random.randrange(1000)}
print(f"Adding data to queue: {data}")
producer.send('libo_test',value=data)
