# In this pattern, both client or server or producer or consumer will produce or consume message.
# it's client resposilty to produce message and consume server replys
import pika
import uuid


# writing callback method, callback method will be called for notification or alert
def on_reply_message_recieved(ch, method, properties, body):
    print(f"reply recieved: {body}")


# connecting to rabbitmq
connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# creating temp or empty queue and set exclusive = True to auto dispose message
reply_queue = channel.queue_declare(queue="", exclusive=True)

channel.basic_consume(
    queue=reply_queue.method.queue,
    auto_ack=True,
    on_message_callback=on_reply_message_recieved,
)

# declaring main queue
channel.queue_declare(queue="request_queue")

message = "Can I request a reply?"

correction_id = str(uuid.uuid4())

print(f"sending request: {correction_id}")

channel.basic_publish(
    exchange="",
    routing_key="request-queue",
    properties=pika.BasicProperties(
        reply_to=reply_queue.method.queue, correlation_id=correction_id
    ),
    body=message,
)

print(f"Starting Client")

channel.start_consuming()
