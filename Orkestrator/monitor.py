#!/usr/bin/env python
import pika
import traceback, sys
from APIcontroller import rabbitemq_func as API
from Repository import QueryObject as Query
import json
import tarantool
import uuid

conn_params = pika.ConnectionParameters('rabbitmq', 5672)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue='Publish_post', durable=False)

print("Waiting for messages. To exit press CTRL+C")

def callback(ch, method, properties, body):
    
    file = open("logmonitorOrc.txt", "w")
    
    body_str = body.decode("utf-8")[:4000]
    message = json.loads(body_str)

    # Записываем событие в Сагу
    if message['operation'] == "Publish_post":
        # Запишем в Тарантул запись
        # Устанавливаем соединение с сервером Tarantool
        connection = tarantool.connect("tarantooldb", 3301)
        counters = connection.space('counter')
        id = str(uuid.uuid4())
        sss = id + message['user']+ message['text'] + 'Publish'
        file.writelines (sss + '\n')
        counters.insert((id , int(message['user']), message['text'] , 'Publish'))
        record = '{"id": "'+ id +'", "user" : "'+ str(message['user']) +'","operation" : "Publish_post", "text" : "'+ str(message['text']) +'" , "status" : "Publish"}'        
        # Опубликуем запись в очередь для чтения
        API.post_writemq(record) # Очередь Post
    elif message['operation'] == "Reading_post":
        # Устанавливаем соединение с сервером Tarantool
        connection = tarantool.connect("tarantooldb", 3301)
        counters = connection.space('counter')
        id = str(message['id'])
        counters.update(id, [('=', 3, 'Reading')])
        #counters.insert('-' , int(message['user']), message['text'] , 'Readed')
    #    Query.sql_post_insert(message['user'],message['text'])
    #    print ("You can become a backend developer.")
    elif message['operation'] == "Readed_post":
        # Устанавливаем соединение с сервером Tarantool
        connection = tarantool.connect("tarantooldb", 3301)
        counters = connection.space('counter')
        id = str(message['id'])
        counters.update(id, [('=', 3, 'Readed')])
    if message['operation'] == "CounterNoReadPost":
        # Устанавливаем соединение с сервером Tarantool
        connection = tarantool.connect("tarantooldb", 3301)
        counters = connection.space('counter')
        #result = counters.index.status.select ("Readed")
        result = str(counters.select('Reading', index=1).rowcount)
        print (result)
        API.post_CountNoRead(result) # Очередь Post
        #print (set)
        #box.space['counter'].index.status:count {'Publish'}        
    file.close()

channel.basic_consume('Publish_post', callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
except Exception:
    channel.stop_consuming()
    traceback.print_exc(file=sys.stdout)