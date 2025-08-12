import pika

# open connection to localhost and open a channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a queue for sending messages to
channel.queue_declare(queue='hello')

# publish a message to the hello queue (what is an exchange?)
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")

# close connection
connection.close()