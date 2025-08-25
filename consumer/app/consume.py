import pika, json, os, ssl
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
        smtp.starttls()
        smtp.login(os.getenv('SMTP_USER', 'user'), os.getenv('SMTP_PASSWORD', 'password'))
        smtp.send_message(msg, from_addr=FROM_EMAIL, to_addrs=to)

    print(f"Email sent to {to}")

def assemble_html(data):
    # Example HTML template
    html_template = """
    <html>
        <body>
            <h1>{title}</h1>
            <p>{body}</p>
        </body>
    </html>
    """
    # Populate the template with data
    return html_template.format(title=data.get('subject', 'Newsletter'), body=data.get('body', ''))

def handle(ch, method, properties, body):
    print(f" [x] Received {body.decode()}")
    body = json.loads(body.decode())

    # Assemble the HTML content
    html_content = assemble_html(body)

    # Send the email
    send_mail(body['email'], body['subject'], html_content)
    print(f" [x] Sent email to {body['email']} with subject '{body['subject']}'")

    channel.basic_ack(delivery_tag=method.delivery_tag)


try:
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')
    params = pika.URLParameters(RABBIT_MQ_URL) # amqps://{user}:{pw}@{b-id}.mq.{region}.on.aws:5671
    params.ssl_options = pika.SSLOptions(context=ssl_context)
    connection = pika.BlockingConnection(params)
except Exception as e:
    print(f"Failed to connect to RabbitMQ: {e}")
    raise e

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
