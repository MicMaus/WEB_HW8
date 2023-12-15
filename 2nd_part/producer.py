import pika
from faker import Faker
from mongoengine import connect, Document, StringField, BooleanField
import json


# Contact class model:
class Contact(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    message_sent = BooleanField(default=False)


def main():
    # MongoDB connection:
    try:
        connect(
            db="hw8",
            host="mongodb+srv://jasinsky:BmCJg7doGgfFEACx@mj.l7d1sxj.mongodb.net/?retryWrites=true&w=majority",
        )
    except Exception as e:
        print(f"the error {e} occured")

    # RabbitMQ connection:
    credentials = pika.PlainCredentials(username="guest", password="guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue="contacts_queue")
    print("RabbitMQ connected")

    fake = Faker()

    # Generate fake contacts and send messages:
    for _ in range(10):  # 10 is number of fake contacts
        contact = Contact(
            full_name=fake.name(),
            email=fake.email(),
        )
        contact.save()
        message_body = json.dumps({"contact_id": str(contact.id)})
        channel.basic_publish(
            exchange="",
            routing_key="contacts_queue",
            body=message_body,
        )

    print("Contacts generated and messages sent to RabbitMQ.")
    connection.close()


if __name__ == "__main__":
    main()
