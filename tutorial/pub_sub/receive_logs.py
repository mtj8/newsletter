import pika

# open connection to localhost and open a channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declare the fanout exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout')

# create a queue for this specific worker that is deleted when the consumer is closed
result = channel.queue_declare(queue='', exclusive=True)


# bind this queue to the exchange
channel.queue_bind(exchange='logs', queue=result.method.queue)

print(' [x] Waiting for logs.')

def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")

channel.basic_consume(queue=result.method.queue, on_message_callback=callback, auto_ack=True)

channel.start_consuming()