import pika
from pika.exchange_type import ExchangeType

connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()
# Enable publish confirms
channel.confirm_delivery()

# enable transaction
channel.tx_select()

channel.exchange_declare(exchange="pubsub", exchange_type=ExchangeType.fanout)

# Creates durable queue that survives restarts
channel.queue_declare("TestQueue", durable=True)

message = "Hello I want to broadcast this message"

channel.basic_publish(
    exchange="pubsub",
    routing_key="",
    # set properties including custom (headers), delivery_mode(message presistance), expiration and content_type
    properties=pika.BasicProperties(
        headers={"name": "brain"},
        delivery_mode=1,
        expiration=13413441,
        content_type="application/json",
    ),
    body=message,
    # set the publish to be mandatory - i.e. recieve a notification of failure
    mandatory=True,
)

# commit transaction
channel.tx_commit()

# rollback a transaction
channel.tx_rollback()

print(f"Sent message: {message}")
