import pika, datetime, json, os
import boto3

# connect to rabbitmq
connection = pika.BlockingConnection(pika.URLParameters(os.getenv('RABBIT_MQ_URL', 'amqp://localhost')))
channel = connection.channel()

channel.exchange_declare('newsletter', 'topic', durable=True)

date = datetime.date.today().isoformat()

# email list
emails = ["mattjoshuatan@gmail.com"]

for email in emails:
    channel.basic_publish(
        exchange='newsletter',
        routing_key='daily',
        body=json.dumps({
            'email': email,
            'date': date,
            'subject': 'Newsletter for ' + date,
            'html': f"""
            <h1>Test header for {date}</h1>
            """
        }),
        properties=pika.BasicProperties(
            content_type='application/json',
            delivery_mode=pika.DeliveryMode.Persistent,  # make message persistent
        )
        # other stuff
    )
    print(f'message sent to {email}')

connection.close()