import pika
import sys
import os
import time

# callback function subscribes to the queue and is called whenever a message is recieved from the queue.
def callback(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    time.sleep(body.count(b'.'))
    print(" [x] Done")

    # acknowledgment
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    # open connection to localhost and open a channel
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # declare a queue 
    channel.queue_declare(queue='new_work', durable=True)

    # ensure that workers are given messages equally
    channel.basic_qos(prefetch_count=1)
    
    # consume messages from the queue using the callback
    channel.basic_consume(queue='new_work',
                        on_message_callback=callback)

    # start consuming
    print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try: 
            sys.exit(0)
        except SystemExit:
            os._exit(0)