from models import Author, Quote
from connection_code import connect


connect


def search_all():
    quotes = Quote.objects()
    for quote in quotes:
        print(quote.to_json())


# all quotes of the author:
def author_search(author_to_search):
    quotes = Quote.objects(Author.fullname == author_to_search)

    for quote in quotes:
        print(quote.to_json())


# quotes with 1 tag:
def tag_search(tag_to_search):
    quotes = Quote.objects(tags__contains=tag_to_search)

    for quote in quotes:
        print(quote.to_json())


# quotes containing one of the tags from the list:
def multi_tag_search(multi_tags_to_search=str):
    tags_list1 = multi_tags_to_search.split(",")
    tags_list = [
        el.strip() for el in tags_list1
    ]  # ensuring results if tags separated and/or not separated by space
    print(tags_list)
    print(type(tags_list))
    quotes = Quote.objects(tags__in=tags_list)

    for quote in quotes:
        print(quote.to_json())


##########################################################################


def parse_input(user_input):
    try:
        input_command = user_input.split(":")[0].strip()
        input_parameter = user_input.split(":")[1].strip()
    except Exception as e:
        return f"pls add command and parameter, error: {e}"

    try:
        func = commands[input_command]
        return func(input_parameter)
    except Exception as e:
        return "en error occured"


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

        result = parse_input(user_input)
        if result is not None:
            print(result)


if __name__ == "__main__":
    main()
