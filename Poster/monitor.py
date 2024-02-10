#!/usr/bin/env python
import pika
import traceback, sys
from APIcontroller import rabbitemq_func as API
from Repository import QueryObject as Query
import json

conn_params = pika.ConnectionParameters('rabbitmq', 5672)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='Post', durable=False)

print("Waiting for messages. To exit press CTRL+C")

def callback(ch, method, properties, body):
    
    file = open("logmonitorPoster.txt", "a")
    
    body_str = body.decode("utf-8")[:4000]
    message = json.loads(body_str)

    if message['operation'] == "get_post":
        rows = Query.sql_post_read(message['user'])
        for rw in rows:
            id = rw[3].strip().strip()
            user = rw[0]
            text = rw[2]
            record = '{"id": "'+ id +'", "user" : "'+ str(user) +'","operation" : "Readed_post", "text" : "'+ text +'" , "status" : "Readed" }'
            print(record)
            #file.writelines(record + '\n')
            API.post_writemqSaga(record)
            API.post_writemq(record)
    elif message['operation'] == "Publish_post":

        id = str(message['id'])
        user = str(message['user'])
        text = str(message['text'])

        # Создадим запись в БД Постера
        Query.sql_post_insert(user,text,id)
        # Вернем событие в Сагу
        record2 = '{"id": "'+ id +'", "user" : "'+ user +'","operation" : "Reading_post", "text" : "'+ text +'" , "status" : "Reading"}'
        file.writelines(record2 + '\n')
        API.post_writemqSaga(record2) # Очередь Publish_post

    #file.writelines(body_str + '\n')
    file.close()

channel.basic_consume('Post', callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)