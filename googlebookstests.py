import requests

#not sure if needed but uh here
key = 'AIzaSyAyyqw3Ph9MdqM8kPoQpuRNVcfEv7VODzs'

def search(title):
    gbooks_query = f"https://www.googleapis.com/books/v1/volumes?q={title}"
    response = requests.get(gbooks_query).json()
    list_of_books = response['items']
    return list_of_books


harry_potter = search("harry potter")
for book in harry_potter:
    print(book['id'])
    print(book['volumeInfo']['title'])
