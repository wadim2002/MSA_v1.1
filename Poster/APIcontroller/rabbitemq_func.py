import pika

def post_readmq():
    testtext = "ОТВЕТ"
    
    # Устанавливаем соединение с сервером RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))
    channel = connection.channel()
 
    # Объявляем очередь, из которой будем получать сообщения
    channel.queue_declare(queue='hello')
 
    # Функция обработки полученного сообщения
    def callback(channel, method, properties, body):
        #Service.post_writemq(testtext)
        print(body)
 
    # Подписываемся на очередь и указываем функцию обработки сообщений
    channel.basic_consume('hello', callback)
    channel.start_consuming()
    channel.close()
    connection.close()

# Функция по отправке постов
def post_writemq(text):
    # Устанавливаем соединение с сервером RabbitMQ
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq',5672))#("amqp://guest:guest@rabbitmq:5672/vhost"))
    channel = connection.channel()
    
    # Объявляем очередь, в которую будем отправлять сообщения
    channel.queue_declare(queue='OUT', durable=False)
    
    # Отправляем сообщение в очередь
    channel.basic_publish(exchange='', routing_key='OUT', body=text)    
    connection.close()
    
    return True