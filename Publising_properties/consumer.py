import pika

# always use docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
connection_parameters = pika.ConnectionParameters(host="localhost")

print(connection_parameters)

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

channel.queue_declare(queue="TestQueue")


def on_message_recieved(channel, method, properties, body):
    print(f"recieved new message: {body}")


channel.basic_consume(
    queue="TestQueue", auto_ack=True, on_message_callback=on_message_recieved
)

print("Starting Consuming")

channel.start_consuming()
