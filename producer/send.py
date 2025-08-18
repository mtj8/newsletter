import pika, datetime, json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare('newsletter', 'topic', durable=True)

date = datetime.date.today().isoformat()

# mock email list
emails = ['jeff@gmail.com', 'me@yahoo.com', 'aaaa@123.edu']

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