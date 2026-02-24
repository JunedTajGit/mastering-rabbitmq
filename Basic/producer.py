import pika

"""
The Pika library is a pure-Python client library for communicating with RabbitMQ message brokers
using the Advanced Message Queuing Protocol
"""
connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()


# declare queue
channel.queue_declare(queue="letterbox")

# define message
message = "Hello this is my first message"

# defulat or direct exchange
channel.basic_publish(exchange="", routing_key="letterbox", body=message)

print(f"message sent: {message}")

connection.close()
