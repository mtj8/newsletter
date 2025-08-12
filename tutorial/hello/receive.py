import pika
import sys
import os

def main():
    # open connection to localhost and open a channel
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # declare a queue 
    channel.queue_declare(queue='hello')

    # callback function subscribes to the queue and is called whenever a message is recieved from the queue.
    def callback(ch, method, properties, body):
        print(f" [x] Received {body}")

    # consume messages from the queue using the callback
    channel.basic_consume(queue='hello',
                        auto_ack=True,
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