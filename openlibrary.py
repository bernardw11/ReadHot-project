import requests


isbn = 9780340822777
viewbook = "https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&jscmd=data&format=json"

#don't need this function cuz the google books function gonna work.
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

def findsubjects(title, author):
    openlib_query = f"https://openlibrary.org/search.json?q=title%3A{title}+author%3A{author}"
    #print(openlib_query)
    response = requests.get(openlib_query).json()

    subjects = {}
    count = 0

    #do we want a ceiling?
    ceiling = min(10, len(response['docs']))
    list_of_books  = response['docs'][:ceiling]
    #list_of_books  = response['docs']
    for book in list_of_books:
        if 'subject' in book:
            listofsubjects = book['subject']
            for s in listofsubjects:
                s = s.lower()
                if s in subjects:
                    subjects[s] += 1
                else:
                    if "reading level" not in s and "accessible" not in s:
                        subjects[s] = 1
                count += 1
    return subjects

def clean_subject_dict(subjects):
    pass
    #clean the mess up: look for reading level, etc.


# harry_potter_books = search("harry potter")
# for book in harry_potter_books:
#     print(book['isbn'][0])
#     print(book['title'])
#     print(book['subject'])
#     print(f"http://covers.openlibrary.org/b/isbn/{book['isbn']}-M.jpg")
