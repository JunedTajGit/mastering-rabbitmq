import pika
import time
import random

connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue="letterbox")

messageId = 1

while True:
    message = f"sending messageId: {messageId}"

    # exchange = Default
    # default or direct exchange
    channel.basic_publish(exchange="", routing_key="letterbox", body=message)

    print(f"sent message: {message}")

    # time is less then consumer, means producer process message more frequently then consumer.
    time.sleep(random.randint(1, 4))

    messageId += 1

connection.close()
