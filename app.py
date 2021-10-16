import json
import random
from random import shuffle
from flask import Flask, request, Response

app = Flask(__name__)


def read_json():
    with open("books.json", "r", encoding="utf-8") as f:
        try:
            books = json.load(f)
        except:
            books = []
    return books


def create_isbn():
    sec_1 = 978
    sec_2 = random.randint(1,7)
    numbers = list(range(0, 9))
    shuffle(numbers)
    sec_3 = numbers[:3]
    sec_4 = numbers[:5]
    sec_5 = random.randint(1,4)
    new_isbn = sec_1-sec_2-sec_3-sec_4-sec_5
    return new_isbn


def create_id(books):
    if not books:
        return 1
    max_id = 0
    for book in books:
        if book["id"] > max_id:
            max_id = book["id"]
    return  max_id + 1


@app.route("/books/<int:id>")
def get_book(id: int):
    is_get_book = False
    books = read_json()
    cur_book = ""
    for book in books:
        if book["id"] == id:
            cur_book = book
            is_get_book = True
            break
    if not is_get_book:
        return Response ("Нет такой книги", content_type="text/html"), 400
    return  Response (json.dumps(cur_book, ensure_ascii=False))



@app.route("/create", methods=["POST"])
def create_book():
    new_book = request.get_json()
    books = read_json()
    new_id = create_id(books)
    new_book["id"] = new_id
    new_isbn = create_isbn()
    new_book["ISBN"] = new_isbn
    with open("books.json", "w", encoding="utf-8") as f:
        json.dumps(books, f, ensure_ascii=False, indent="\n")
    return Response(json.dumps(books, ensure_ascii=False), content_type="application/json"), 201




if __name__ == '__main__':
    app.run()
