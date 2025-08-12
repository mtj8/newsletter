import pika, sys

# open connection to localhost and open a channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# declare a fanout exchange
channel.exchange_declare(exchange='logs', exchange_type='fanout') # queue name is ignored for a fanout exchange, which sends to all queues

message = ' '.join(sys.argv[1:]) or 'beep boop'
# publish to exchange
channel.basic_publish(exchange='logs',
                      routing_key='',
                      body=message)

print(f" [x] Sent '{message}'")

connection.close()