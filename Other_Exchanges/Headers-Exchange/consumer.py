# Send message from one exchange to another exchange to make complex system
# second exchange accpet message from first exchange
import pika
from pika.exchange_type import ExchangeType


def on_message_recieved(ch, method, properties, body):
    print(f"recieved new message: {body}")


connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# second exchange
channel.exchange_declare(exchange="headerexchange", exchange_type=ExchangeType.headers)

# declare a queue that will be used to send message
channel.queue_declare(queue="letterbox")

# creating binding arguments
bind_args = {"x-match": "all", "name": "brian", "age": "53"}

channel.queue_bind("letterbox", "headerexchange", arguments=bind_args)

channel.basic_consume(
    queue="letterbox", auto_ack=True, on_message_callback=on_message_recieved
)

print("starting consuming")

channel.start_consuming()
