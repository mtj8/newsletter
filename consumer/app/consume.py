import pika, json, os
from smtplib import SMTP
from email.mime.text import MIMEText

SMTP_SERVER = os.getenv('SMTP_HOST', 'localhost')
SMTP_PORT = os.getenv('SMTP_PORT', 1025)

FROM_EMAIL = os.getenv('FROM_EMAIL', 'mattjoshuatan@gmail.com')

RABBIT_MQ_URL = os.getenv('RABBIT_MQ_URL', 'amqp://localhost')

def send_mail(to, subject, html):
    print(f"Sending email to {to} with subject '{subject}'")

    msg = MIMEText(html, 'html')
    msg['Subject'] = subject
    msg['From'] = FROM_EMAIL
    msg['To'] = to

    with SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
        smtp.send_message(msg, from_addr=FROM_EMAIL, to_addrs=to)

    print(f"Email sent to {to}")

def handle(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    body = json.loads(body.decode())

    send_mail(body['email'], body['subject'], body['html'])
    print(f" [x] Sent email to {body['email']} with subject '{body['subject']}'")

    channel.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='newsletter',
                    exchange_type='topic', 
                    durable=True)

channel.queue_declare(queue='newsletter.send', durable=True)

channel.queue_bind(queue='newsletter.send',
                exchange='newsletter', 
                routing_key='daily')

channel.basic_consume('newsletter.send', on_message_callback=handle)

channel.start_consuming()
