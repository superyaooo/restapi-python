from flask import Flask, jsonify, request, Response
import json
from settings import *
from BookModel import *

#GET /books by default
@app.route('/books')
def get_books():
    return jsonify({'books': Book.get_all_books()})

def validBookObject(bookObject):
    if ("name" in bookObject and "price" in bookObject and "isbn" in bookObject):
        return True
    else:
        return False

@app.route('/books', methods=['POST'])
def add_book():
    request_data = request.get_json()
    if(validBookObject(request_data)):
        Book.add_book(request_data['name'], request_data['price'], request_data['isbn'])
        response = Response("", 201, mimetype='application/json')
        response.headers['Localtion'] = "/books/" + str(request_data['isbn'])
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
    return_value = Book.get_book(isbn)
    return jsonify(return_value)

# PUT requires an entire entity
@app.route('/books/<int:isbn>', methods=['PUT'])
def replace_book(isbn):
    request_data = request.get_json()
    Book.replace_book(isbn, request_data['name'], request_data['price'])
    response = Response("", 204)
    return response

# PATCH does not require an entire entity
@app.route('/books/<int:isbn>', methods=['PATCH'])
def update_book(isbn):
    request_data = request.get_json()
    if("name" in request_data):
        Book.update_book_name(isbn, request_data['name'])
    if("price" in request_data):
        Book.update_book_price(isbn, request_data['price'])
    response = Response("", 204)
    response.headers['Location'] = "/books" + str(isbn)
    return response

@app.route('/books/<int:isbn>', methods=['DELETE'])
def delete_book(isbn):
    request_data = request.get_json()
    if(Book.delete_book(isbn)):
        return Response("", 204)
    return Response("", 404, mimetype='application/json')

app.run(port=5000)