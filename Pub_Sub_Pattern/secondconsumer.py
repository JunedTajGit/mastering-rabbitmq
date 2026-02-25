import pika
from pika.exchange_type import ExchangeType


def on_message_recieved(channel, method, properties, body):
    print(f"secondconsumer : recieved new message: {body}")


# always use docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
connection_parameters = pika.ConnectionParameters(host="localhost")

print(connection_parameters)

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.exchange_declare(exchange="pubsub", exchange_type=ExchangeType.fanout)

# each consumer have a dedicated queue and is provied at runtime and deleted automatically.
# exculsive=True means it will be deleted once used.
queue = channel.queue_declare(queue="", exclusive=True)

channel.queue_bind(exchange="pubsub", queue=queue.method.queue)

channel.basic_consume(
    queue=queue.method.queue, auto_ack=True, on_message_callback=on_message_recieved
)

print("second Starting Consuming")

channel.start_consuming()
