import pika


credentials = pika.PlainCredentials('root', '1234')
parameters = pika.ConnectionParameters(host='localhost',
                                       port=5672,
                                       credentials=credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')

def callback(ch, method, properties, body):

    print(f" [x] Received {body.decode()}")
    # channel.basic_ack(method.delivery_tag)

channel.basic_consume(queue='hello',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

connection.close()
