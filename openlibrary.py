import requests


isbn = 9780340822777
viewbook = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"

def search(query):
    openlib_query = f"http://openlibrary.org/search.json?q={query}"
    response = requests.get(openlib_query).json()
    #ceiling = min(10, response['num_found'])
    list_of_books  = response['docs']
    totalnum = response['num_found']
    viable_books = []
    i = 0
    while len(viable_books) < 10 and i < totalnum:
        book = list_of_books[i]
        if 'isbn' in book and 'subject' in book:
            viable_books.append(book)
        i += 1
    return viable_books

# harry_potter_books = search("harry potter")
# for book in harry_potter_books:
#     print(book['isbn'][0])
#     print(book['title'])
#     print(book['subject'])
#     print(f"http://covers.openlibrary.org/b/isbn/{book['isbn']}-M.jpg")
