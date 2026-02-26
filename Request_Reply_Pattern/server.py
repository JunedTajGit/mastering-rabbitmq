# In this pattern, both client or server or producer or consumer will produce or consume message.
# it's client resposilty to produce message and consume server replys
import pika


# writing callback method, callback method will be called for notification or alert
def on_request_message_recieved(ch, method, properties, body):
    print(f"request recieved: {body} - correctionid: {properties.correlation_id}")

    # when we recieve request, then response or reply will be publish to default exchange
    ch.basic_publish(
        "",
        routing_key=properties.reply_to,  # reply is a queue,
        body=f"Hey its your reply to {properties.correlation_id}",
    )


# connecting to rabbitmq
connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# creating temp or empty queue and set exclusive = True to auto dispose message
reply_queue = channel.queue_declare(queue="request-queue", exclusive=True)

channel.basic_consume(
    queue="request-queue",
    auto_ack=True,
    on_message_callback=on_request_message_recieved,
)

print("Starting server here")

channel.start_consuming()
