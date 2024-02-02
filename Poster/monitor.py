#!/usr/bin/env python
import pika
import traceback, sys
from APIcontroller import rabbitemq_func as API
from Repository import QueryObject as Query
import json

conn_params = pika.ConnectionParameters('rabbitmq', 5672)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='post', durable=False)

print("Waiting for messages. To exit press CTRL+C")

def callback(ch, method, properties, body):
    
    file = open("logmonitor.txt", "w")
    
    body_str = body.decode("utf-8")[:4000]
    message = json.loads(body_str)

    if message['operation'] == "get_post":
        rows = Query.sql_post_read(message['user'])
        API.post_writemq(rows)
    elif message['operation'] == "create_post":
        Query.sql_post_insert(message['user'],message['text'])
        print ("You can become a backend developer.")
    
    file.writelines(body_str + '\n')
    file.close()

channel.basic_consume('post', callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)