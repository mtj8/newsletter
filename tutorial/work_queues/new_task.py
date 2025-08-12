import pika, sys

# open connection to localhost and open a channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# create a queue for sending messages to
channel.queue_declare(queue='new_work', durable=True)

# publish a message to the work queue (what is an exchange?)
message = ' '.join(sys.argv[1:]) or "Hello World!" 
channel.basic_publish(exchange='',
                      routing_key='new_work',
                      body=message,
                      properties=pika.BasicProperties(
                          delivery_mode = pika.DeliveryMode.Persistent # make message persistent
                      ))
print(f" [x] Sent '{message}'")

# close connection
connection.close()