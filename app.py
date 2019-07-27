from flask import Flask, jsonify, request, Response
import json

app = Flask(__name__)

books = [
    {
        'name': 'Green eggs and ham',
        'price': 7.99,
        'isbn': 9837439254
    },
    {
        'name': 'the cat in the hat',
        'price': 6.99,
        'isbn': 8497927865
    }
]

#GET /books by default
@app.route('/books')
def get_books():
    return jsonify({'books': books})

def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        new_book = {
            "name": request_data['name'],
            "price": request_data['price'],
            "isbn": request_data['isbn']
        }
        books.insert(0, new_book)
        response = Response("", 201, mimetype='application/json')
        response.headers['Localtion'] = "/books/" + str(new_book['isbn'])
        return response
    else:
        invalidBookObjectErrorMsg = {
            "error": "Invalid book passed in request",
            "helpString": "needed format: blah blah blah"
        }
        response = Response(json.dumps(invalidBookObjectErrorMsg), 400, mimetype='application/json')
        return response

@app.route('/books/<int:isbn>')
def get_book_by_isbn(isbn):
    return_value = {}
    for book in books:
        if book["isbn"] == isbn:
            return_value = {
                'name': book["name"],
                'price': book["price"]
            }
    return jsonify(return_value)

# PUT requires an entire entity
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    new_book = {
        'name': request_data['name'],
        'price': request_data['price'],
        'isbn': isbn
    }
    counter = 0;
    for book in books:
        currentIsbn = book['isbn']
        if currentIsbn == isbn:
            books[counter] = new_book
        counter += 1
    response = Response("", 204)
    return response

# PATCH does not require an entire entity
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    updated_book = {}
    if("name" in request_data):
        updated_book['name'] = request_data['name']
    if("price" in request_data):
        updated_book['price'] = request_data['price']
    for book in books:
        if book['isbn'] == isbn:
            book.update(updated_book)
    response = Response("", 204)
    response.headers['Location'] = "/books" + str(isbn)
    return response

app.run(port=5000)