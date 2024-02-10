from django.shortcuts import render
from django.http import HttpResponse
import Repository.QueryObject as QueryObject
import APIcontroller.rabbitemq_func as API
import pika
import tarantool

def wellcome(request):
    return HttpResponse("<h1>Wellcome Orkestrator service! (MSA)</h1>")

# Функция по созданию постов
def post_create(request,userid,text):
    return HttpResponse(QueryObject.sql_post_insert(userid,text))


# Функция по получению постов
def post_read(request,id):
    return HttpResponse(QueryObject.sql_post_read(id))

# Функция по получению постов
def post_readmq(request):
    # Устанавливаем соединение с сервером RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))
    channel = connection.channel()
 
    # Объявляем очередь, из которой будем получать сообщения
    channel.queue_declare(queue='hello')
 
    file = open("logmq.txt", "w")
    # Функция обработки полученного сообщения
    def callback(channel, method, properties, body):
        body_str = body.decode("utf-8")[:4000]

        file.writelines(body_str + '\n')
    
        sss = int(body_str)+3
        file.writelines(sss + '\n')
        API.post_writemq("0000")
        
    # Подписываемся на очередь и указываем функцию обработки сообщений
    channel.basic_consume('hello', callback)
    
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        #traceback.print_exc(file=sys.stdout)
    
    file.close()
    return HttpResponse ("OK")
  
# Функция по отправке постов
def post_writemq(request,text):
    result = API.post_writemq(text)    
    return HttpResponse(result)

def post_noread(request):
        # Устанавливаем соединение с сервером Tarantool
        connection = tarantool.connect("tarantooldb", 3301)
        counters = connection.space('counter')
        result = counters.index.status.select ('Readed')
        return HttpResponse (result)

