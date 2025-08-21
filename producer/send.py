import pika, datetime, json, os
import boto3

# boto3 resource for dynamodb
db = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
subscribers = db.Table('subscribers')

# connect to rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare('newsletter', 'topic', durable=True)

date = datetime.date.today().isoformat()

# email list
emails = [item for item in subscribers.scan()['Items']]
emails = [e['email'] for e in emails]

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