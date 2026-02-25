import pika
from pika.exchange_type import ExchangeType


def on_message_received(ch, method, properties, body):
    print(f"Analytics Service - received new message: {body}")


connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange="mytopicexchange", exchange_type=ExchangeType.topic)

# exclusive=True means queue will be deleted when connection is closed
queue = channel.queue_declare(queue="", exclusive=True)

# anything start with one word and end with one word
channel.queue_bind(
    exchange="mytopicexchange", queue=queue.method.queue, routing_key="*.europe.*"
)


channel.basic_consume(
    queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received
)

print("Starting consuming")

channel.start_consuming()
