from models import Author, Quote
from connection_code import connect
import json

connect

# define file paths
quotes_file = r"./json_files/qoutes.json"
authors_file = r"./json_files/authors.json"

# open content from files
with open(authors_file, "r") as fh:
    unpacked_authors = json.load(fh)

with open(quotes_file, "r") as fh:
    unpacked_quotes = json.load(fh)


# parse all attributes of class Author from unpacked json file:
authors_instances = [Author(**author) for author in unpacked_authors]
# insert instances into collections:
for author in authors_instances:
    aut = author
    aut.save()

# parse all attributes of class Quote 'manually',to avoid giving author as a str
# but as instance of Author class, so refference works properly:
quotes_instances = [
    Quote(
        tags=quote.get("tags", []),
        author=Author.objects(fullname=quote.get("author")).first(),
        quote=quote.get("quote", ""),
    )
    for quote in unpacked_quotes
]

# insert instances into collections:
for quote in quotes_instances:
    quote.save()
