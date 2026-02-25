import pika
from pika.exchange_type import ExchangeType

# In this pattern, producer won't declare queue or even doesn't know about any queue
# it just send message to the exchange then exchange will send message to queue as per binding.
# In this consumer is responsible to create a queue as per it's utility.

connection_parameters = pika.ConnectionParameters("localhost")

connection = pika.BlockingConnection(connection_parameters)

channel = connection.channel()

# In this pattern, producer won't declare queue or even doesn't know about any queue
# channel.queue_declare(queue="letterbox")

# here fanout exchange type is being created with name pubsub.
channel.exchange_declare(exchange="mytopicexchange", exchange_type=ExchangeType.topic)

# since this is fanout pattern, so message will be sent to all the subscribed queue using binding
# using binding to identify which service is consuming message and message will be sent to exchange instead of queue
user_payment_message = "this message is to be routed"

# removed the routing_key value means queue.
channel.basic_publish(
    exchange="mytopicexchange",
    routing_key="user.europe.payments",
    body=user_payment_message,
)

# message should get this message as it quality in all type of wild cards.
# : "user.#", "#.payments", "*.europe.*"

print(f"sent message: {user_payment_message}")

business_order_message = "A european buisness ordered goods"
# message should get this message as it quality in all type of wild cards.
# : "user.#", "#.payments", "*.europe.*"
channel.basic_publish(
    exchange="mytopicexchange",
    routing_key="user.europe.payments",
    body=user_payment_message,
)

# message should get this message as it quality in all type of wild cards.
print(f"sent message: {business_order_message}")


business_order_message = "A european buisness ordered goods"

channel.basic_publish(
    exchange="mytopicexchange",
    routing_key="business.europe.order",
    body=user_payment_message,
)

# message should get this message as it quality in all type of wild cards.
print(f"sent message: {business_order_message}")


connection.close()
