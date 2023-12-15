from mongoengine import connect
import configparser

config = configparser.ConfigParser()
config.read("./config.ini")

mongo_user = config.get(section="DB", option="USER")
mongodb_pass = config.get(section="DB", option="PASS")
db_name = config.get(section="DB", option="DB_NAME")
domain = config.get(section="DB", option="DOMAIN")

url = f"mongodb+srv://{mongo_user}:{mongodb_pass}@{domain}/{db_name}?retryWrites=true&w=majority"

try:
    connect(db=db_name, host=url)
    print("successfully connected")
except Exception as e:
    print(f"the error {e} occured")
