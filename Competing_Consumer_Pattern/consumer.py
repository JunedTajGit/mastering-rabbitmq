"""
auto_ack = True will be commented, because once a message is get recieved at consumer
and if consumer is busy then message can be picked by another consumer
and after successfully processed then mananully acknowledge the message.

To check this pattern in action run 2 instances of consumer.

"""

import pika
import time
import random


def on_message_received(ch, method, properties, body):
    processing_time = random.randint(1, 6)

    print(f"received: {body}, will take {processing_time} to process")
    # this message will be processed in this much time.
    time.sleep(processing_time)
    # after processing, need to send acknowledgement manually
    ch.basic_ack(delivery_tag=method.delivery_tag)
    print("Finished processing the message")


connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue="letterbox")
# this setting will only one message to be fetch to process
# if is commented, means it will back to round robbin
channel.basic_qos(prefetch_count=1)

channel.basic_consume(queue="letterbox", on_message_callback=on_message_received)

print("starting consuming")

channel.start_consuming()
