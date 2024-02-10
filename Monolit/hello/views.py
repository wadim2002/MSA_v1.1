from django.http import HttpResponse
import psycopg2
import pika
import rabbitpy
import traceback, sys
import json
import datetime

def wellcome(request):
    return HttpResponse("<h1>Wellcome my Python app!</h1>")
def index(request):
    conn = psycopg2.connect(dbname="postrges", user="postrges", password="123456", host="master", port="5432")
    with conn:
        with conn.cursor() as cursor:
            print("Подключение установлено")
            #cursor = connection.cursor()
            # Выполнение SQL-запроса для вставки данных в таблицу
            insert_query = """ INSERT INTO people (name, age) VALUES ('Aaaa',55)"""
            cursor.execute(insert_query)
            conn.commit()
                 
    print(cursor.closed)    # True - курсор закрыт
    # cursor.close()  # нет смысла - объект cursor уже закрыт
    conn.close()    # объект conn не закрыт, надо закрывать
    return HttpResponse("<h1>БД подключена</h1>")

def login(request,name,password):
    conn = psycopg2.connect(dbname="postrges", user="postrges", password="123456", host="master", port="5432")

    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE name='"+str(name)+"' AND password ='" + str(password) + "'"
    cursor.execute(query)
    
    rows = cursor.fetchall()

    if rows != []:
        result = "Ваш идентификатор =" + str(rows[0][0])
    else:
        result = "Нет такого пользователя"

    cursor.close()
    conn.close()

    return HttpResponse(result)       
   
def getuser(request,id):
    #conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="db", port="5432")
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="dbslave", port="5432")
    
    cursor = conn.cursor()

    query = "SELECT name FROM users WHERE id='"+str(id) + "'"
    cursor.execute(query)
    
    rows = cursor.fetchall()

    if rows != []:
        result = "Ваше имя =" + str(rows[0][0])
    else:
        result = "Нет такого пользователя"

    cursor.close()
    conn.close()

    return HttpResponse(result)   
 
def register(request,name,surname,old,sex,hobby,sity,password):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="123456", host="master", port="5432")

        cursor = conn.cursor()

        query = "INSERT INTO public.users(name, surname, age, sex, interests, city, password) VALUES ('"+ name +"', 'users', 33, 'man', 'Hob1', 'Sity1', 'Pass1');"

        cursor.execute(query)
        conn.commit()  
    
        cursor.close()
        conn.close()

        return HttpResponse('Пользователь зарегистрирован')      
def search(request,firstName,secondName):
    print ("==============================старт=========================")
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="dbslave", port="5432")

    cursor = conn.cursor()
    # firstName LIKE ? and secondName LIKE ?). Сортировать вывод по id анкеты.
    query = "SELECT name, surname FROM users WHERE (name LIKE '"+ firstName + "%') AND (surname LIKE '" + secondName + "%') ORDER BY id"
    # (title LIKE '%Cook%') AND (title LIKE '%Recipe%')

    cursor.execute(query)
    
    rows = cursor.fetchall()

    print(rows)

    if rows != []:
        result = "Ваше имя =" + str(rows[0][0]) + " Фамилия =" + str(rows[0][1])
    else:
        result = "Нет такого пользователя"

    cursor.close()
    conn.close()

    return HttpResponse(rows)

def refresh(request):
    myredis = myCash()
    myredis.removeAllKeys
    myredis.validation('posts','100')
    return HttpResponse('ok')

class myCash:
    def setincash(key , value):
        r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
        r.mset({key: value})
        return True;
    def getincach(key):
        r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
        return r.get(key);
    def validation(self, table, countrecords):
        conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="dbslave", port="5432")
    
        cursor = conn.cursor()

        query = "SELECT * FROM "+ table +" ORDER BY id DESC LIMIT " + countrecords
        
        cursor.execute(query)
    
        rows = cursor.fetchall()

        r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
        
        for row in rows:
            r.mset({row[0]: row[2]})

        cursor.close()
        conn.close()
        return True
    
    def removeAllKeys():
        r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
        rows = r.keys("*")
        for i in rows:        
            r.delete(i)
        return True    

def getposts(request):
    r = redis.Redis(host='172.23.0.2', port=6379, db=0, password=None, socket_timeout=None)
    rows = r.keys("*")

    sss = []
    for i in rows:
        sss.append(r.get(i))
        sss.append("<br><br>")

    return HttpResponse(sss)   

# Функция по созданию постов
def post_create(request,userid,text):
    # подключение к БД
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="db_monolit", port="5432")
    # создание курсора
    cursor = conn.cursor()
    # строка запроса
    query = "INSERT INTO post (id_user, text) VALUES ('" + str(userid) + "','" + text + "')"
    cursor.execute(query)
    conn.commit()  

    cursor.close()
    conn.close()
    
    return HttpResponse("Пост создан (Legasy)")

# Функция по отправке сообщения
def dialog_send(request,user,text):
    # подключение к БД
    conn = psycopg2.connect(dbname="postrges", user="postrges", password="pass", host="master", port="5432")
    # создание курсора
    cursor = conn.cursor()
    # строка запроса
    query = "INSERT INTO messages (id_user, text) VALUES ('"+str(user) + "','"+ text + "')"
    #INSERT INTO products (product_no, name, price) VALUES (1, 'Cheese', DEFAULT);
    cursor.execute(query)
    conn.commit()  
    
    result = "Сообщение отправлено"

    cursor.close()
    conn.close()

    return HttpResponse(result)

def post_send(request):
    # подключение к БД
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="dbslave", port="5432")
    # создание курсора
    cursor = conn.cursor()
    # строка запроса
    query = "SELECT text FROM posts where ID=1"
    cursor.execute(query)
    
    rows = cursor.fetchall()

    mess = str(rows[0][0])

    # Устанавливаем соединение с сервером RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))#("amqp://guest:guest@rabbitmq:5672/vhost"))
    channel = connection.channel()
    
    # Объявляем очередь, в которую будем отправлять сообщения
    channel.queue_declare(queue='hello')
    
    # Отправляем сообщение в очередь
    channel.basic_publish(exchange='', routing_key='hello', body=mess)    
    connection.close()

    cursor.close()
    conn.close()

    return HttpResponse(mess)

def post_read_old(request):
    # Устанавливаем соединение с сервером RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))
    channel = connection.channel()
 
    # Объявляем очередь, из которой будем получать сообщения
    channel.queue_declare(queue='hello')
 
    # Функция обработки полученного сообщения
    def callback(channel, method, properties, body):
        print(f"Received: '{body}'")
 
    # Подписываемся на очередь и указываем функцию обработки сообщений
    channel.basic_consume('hello', callback)
    channel.start_consuming()
    channel.close()
    connection.close()

def post_read(request,id):
    # подключение к БД
    conn = psycopg2.connect(dbname="postgres", user="postgres", password="pass", host="db_monolit", port="5432")
    # создание курсора
    cursor = conn.cursor()
    # строка запроса
    query = "SELECT * FROM post WHERE id_user ='" + str(id) + "'"

    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()  

    cursor.close()
    conn.close()

    return HttpResponse(json.dumps(rows))

def post_createmq(request, userid, text):
    conn_params = pika.ConnectionParameters('rabbitmq', 5672)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue='Publish_post')

    channel.basic_publish(exchange='',
			  routing_key='Publish_post',
              body='{"id": "", "user" : "'+ str(userid) +'","operation" : "Publish_post", "text" : "'+ str(text) +'" , "status" : ""}')

    connection.close()
    logger("Poster", "create_post")

    return HttpResponse("Пост создан (MSA)")

def post_readmq(request, id):
    conn_params = pika.ConnectionParameters('rabbitmq', 5672)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue='Post')

    channel.basic_publish(exchange='',
			  routing_key='Post',
			  body='{"user" : "'+ str(id) +'","operation" : "get_post"}')

    connection.close()
    logger("Monolit", "get_post")
    
    res = monitor_monolit()
    return HttpResponse(res)

def monitor_monolit():
    out = []
    conn_params = pika.ConnectionParameters('rabbitmq', 5672)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue='OUT', durable=False)

    print("Waiting for messages. To exit press CTRL+C")

    def callback(ch, method, properties, body):
        message = json.loads(body.decode("utf-8")[:4000])
        #print('value = ' + message['value'])
        out.append (message)
        #print (str(out['value']))

        
        
        #out.append (body.decode("utf-8")[:4000])
        #file = open("logmonitormonolit.txt", "a")
        #file.writelines(out + '\n')
        #file.close()

    channel.basic_consume('OUT', callback, auto_ack=True)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        traceback.print_exc(file=sys.stdout)
    logger("Poster", "get_post_result")
    return out
    
def logger(service_name, operation_name):
    file = open("logger.txt", "a")
    log_record = str(datetime.datetime.now()) + " *** " + service_name + " *** " + operation_name 
    file.seek(0, 2)
    file.writelines(log_record + '\n')
    file.close()
    
def post_noread(request):
    conn_params = pika.ConnectionParameters('rabbitmq', 5672)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue='Publish_post')

    channel.basic_publish(exchange='',
			  routing_key='Publish_post',
              body='{"id": "", "user" : "0","operation" : "CounterNoReadPost", "text" : "-" , "status" : "-"}')

    connection.close()
    print("Monolit send request for count message")
    
    out=[]
    # URL для соединения
    url = 'amqp://guest:guest@rabbitmq:5672/%2F'

    # Открытие соединения RabbitMQ
    connection = rabbitpy.Connection(url)            # Создание нового объекта соединения, подключение к RabbitMQ

    # открытие канала для взаимодействия с RabbitMQ
    channel = connection.channel('OUT')                   # Открытие канала для взаимодействия

    # Создание объекта для взаимодействия с очередью
    queue = rabbitpy.Queue(channel, 'OUT')       # Создание нового объекта очереди для получения сообщений

    # Пока в данной очереди имеются сообщения, идёт его опрос с применением Basic.Get
    while len(queue) > 0:                         # цикл до тех пор, пока в очереди имеются сообщения
        message = queue.get()                        # выборка очередного сообщения
        #print('Message:')
        #print(' ID: %s' % message.properties['message_id'])                # Получение сообщения из обрабатываемой очереди
        #print(' Time: %s' % message.properties['timestamp'].isoformat())   # Печать штампа времени свойства отформатированного в виде штампа времени ISO 8601 
        print(' Body: %s' % message.body)            # Печать тела сообщения
        if json.loads(message.body)['operation']=='CounterNoReadPost':
            out.append(json.loads(message.body)['value'])
            message.ack() 
    #res = monitor_orkestrator()
    print("Monolit end scan request for count message")
    #print (res)
    return HttpResponse('Не прочитано сообщений ' + str(out[0]) + ' шт.')

def monitor_orkestrator():
    out = []
    conn_params = pika.ConnectionParameters('rabbitmq', 5672)
    connection = pika.BlockingConnection(conn_params)
    channel = connection.channel()

    channel.queue_declare(queue='OUT', durable=False)

    print("Monolit waiting Statistic")

    def callback(ch, method, properties, body):
        val = json.loads(body.decode("utf-8")[:4000])['value']
        out.append(val)
        return out
        #print(out)
        #message = body.decode("utf-8")[:4000]
        
        #body_str = json.loads(message)
        #print('=============' +  body_str)
        #out.append(message)
        #print(out)
    channel.basic_consume('OUT', callback, auto_ack=True)
    #print(out)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    except Exception:
        channel.stop_consuming()
        traceback.print_exc(file=sys.stdout)
    return out