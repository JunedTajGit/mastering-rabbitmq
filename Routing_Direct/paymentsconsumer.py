import pika
from pika.exchange_type import ExchangeType


def on_message_received(ch, method, properties, body):
    print(f"Payment Service - received new message: {body}")


connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange="routing", exchange_type=ExchangeType.direct)

# exclusive=True means queue will be deleted when connection is closed
queue = channel.queue_declare(queue="", exclusive=True)

channel.queue_bind(
    exchange="routing", queue=queue.method.queue, routing_key="paymentsonly"
)
# we can have multiple binding so message can be recieve by both if in case of both key
channel.queue_bind(exchange="routing", queue=queue.method.queue, routing_key="both")


channel.basic_consume(
    queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_received
)

print("Starting consuming")

channel.start_consuming()
