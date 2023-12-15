from producer import Contact
import pika
from mongoengine import connect
import sys
import json

# MongoDB connection:
try:
    connect(
        db="hw8",
        host="mongodb+srv://jasinsky:BmCJg7doGgfFEACx@mj.l7d1sxj.mongodb.net/?retryWrites=true&w=majority",
    )
except Exception as e:
    print(f"the error {e} occured")


def sender():
    pass


def main():
    # RabbitMQ connection:
    credentials = pika.PlainCredentials(username="guest", password="guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue="contacts_queue")
    print("RabbitMQ connected")

    #######################################################

    # Callback function for handling messages
    def callback(ch, method, properties, body):
        data = json.loads(body)
        contact_id = data.get("contact_id")
        # Simulate email sending
        sender()

        # Update the logical field to True after sending the message
        contact = Contact.objects.get(id=contact_id)
        contact.message_sent = True
        contact.save()

        print(f"Message sent to {contact.full_name}")

    # Swich to listen for messages mode:
    channel.basic_consume(
        queue="contacts_queue", on_message_callback=callback, auto_ack=True
    )

    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Message sending was interrupted")
        sys.exit(0)
