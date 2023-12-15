from models import Author, Quote
from connection_code import connect
import json


connect


def search_all():
    quotes = Quote.objects()
    return quotes


# all quotes of the author:
def author_search(author_to_search):
    quotes = Quote.objects(Author.fullname == author_to_search)
    return quotes


# quotes with 1 tag:
def tag_search(tag_to_search):
    quotes = Quote.objects(tags__contains=tag_to_search)
    return quotes


# quotes containing one of the tags from the list:
def multi_tag_search(multi_tags_to_search=str):
    tags_list1 = multi_tags_to_search.split(",")
    tags_list = [
        el.strip() for el in tags_list1
    ]  # ensuring results if tags separated and/or not separated by space
    quotes = Quote.objects(tags__in=tags_list)
    return quotes


##########################################################################


def parse_input(user_input):
    try:
        input_command = user_input.split(":")[0].strip()
        input_parameter = user_input.split(":")[1].strip()
    except IndexError as e:
        print(f"pls add command and parameter, error: {e}")

    if not input_parameter:
        print("pls add mandatory parameter")
    else:
        try:
            func = commands[input_command]
            return func(input_parameter)
        except Exception as e:
            print(f"en error occured: {e}")


commands = {
    "name": author_search,
    "tag": tag_search,
    "tags": multi_tag_search,
}
#########################################################################


def main():
    while True:
        user_input = input("your input: ")

        if user_input.startswith("exit"):
            print("Good bye!")
            break

        quotes = parse_input(user_input)  # quotes is Quote.objects
        try:
            quotes[0]
            for quote in quotes:
                #     print(quote.to_json())
                quote_dict = quote.to_json()
                utf8_json = json.dumps(quote_dict, ensure_ascii=False).encode("utf-8")
                print(utf8_json)
        except IndexError:
            print("nothing found")


if __name__ == "__main__":
    main()