#! /usr/bin/python3
from bs4 import BeautifulSoup
import re
import requests

def info(n):
    s=n.split()
    m='+'.join(s)
    #print(m)
    search_url = "https://www.googleapis.com/books/v1/volumes?q=" + m +"&maxResults=1"
    search_res = requests.get(search_url)
    search_rjson = search_res.json()
    book_id  = search_rjson['items'][0]['id']
    book_url = "https://www.googleapis.com/books/v1/volumes/" + book_id
    r = requests.get(book_url)
    book_info = r.json()
    try:
        res = book_info['volumeInfo']['categories']
        print(res)
    except KeyError:
        print("Oops!")
        print(n)


print("Enter self: eg GR-2 ")
self = input()
print('No. of books u wanna look upon: ')
size = input()
url = 'http://172.31.1.40/cgi-bin/OPAC.exe?UName=&Option=PageView&SQL=SELECT+accNo,title,author,status,shelfNo+FROM+BookDetails+WHERE+shelfNo+LIKE+|{'+self+'{|+ORDER+BY+shelfNo+asc&pageSize='+size+'&absolutePage=1'
r = requests.get(url)
bs = BeautifulSoup(r.text,"lxml")
ht = bs.body.form.center.table
inside = ht.tr.next_sibling.next_sibling.next_sibling.next_sibling.table.next_sibling
i =1
for sibling in inside.tr.next_siblings:
   print('=======================================')
   data = repr(sibling.td.next_sibling.next_sibling.string)
   info(data)
   i=i+1

# l = ['Fiction / Science Fiction / Action & Adventure', 'Fiction / Thrillers / General', 'Fiction / Science Fiction / Hard Science Fiction']
# s = ''.join(l)
# gen = re.split(', | /',s)
# length = len(gen)
# for i in range(length):
#     if gen[i]=='Thrillers':
#         print(gen[i])
# print(len(gen))