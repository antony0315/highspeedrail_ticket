import pika


credentials = pika.PlainCredentials('root', '1234')
parameters = pika.ConnectionParameters(host='localhost',
                                       port=5672,
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

for i in range(100):
    msg = str(i)
    channel.basic_publish(exchange='', 
                          routing_key='hello', 
                          body=msg)
    print(f" [x] Sent '{msg}'")

connection.close()
