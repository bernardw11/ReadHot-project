import requests
from openlibrary import findsubjects

#not sure if needed but uh here
key = 'AIzaSyAyyqw3Ph9MdqM8kPoQpuRNVcfEv7VODzs'

def search(title):
    gbooks_query = f"https://www.googleapis.com/books/v1/volumes?q={title}"
    response = requests.get(gbooks_query).json()
    list_of_books = response['items']
    viable_books = []
    for book in list_of_books:
        info = book['volumeInfo']
        if 'authors' not in info:
            info['authors'] = "Author Not Available"
        if 'industryIdentifiers' in info:
            if 'imageLinks' not in info:
                info['imageLinks'] = {}
                info['imageLinks']['thumbnail'] = "/static/img/default_book_cover.jpg"
            info['subject'] = findsubjects(info['title'], info['authors'][0])
            #print(info['subject'])
            viable_books.append(book)
    return viable_books


# harry_potter = search("harry potter")
# for book in harry_potter:
#     print(book['id'])
#     print(book['volumeInfo']['title'])
