#! /usr/bin/python3
from bs4 import BeautifulSoup
import re
import requests
import sys

def info(n,genbk,size,p):
    s=n.split()
    m='+'.join(s)
    #print(m)

    search_url = "https://www.googleapis.com/books/v1/volumes?q=" + m +"&maxResults=1&fields=items(id)&key=keyy"
    header = {
        'Accept-Encoding': 'gzip',
        'User-Agent' : 'gzip'
    }
    search_res = requests.get(search_url, headers=header)
    search_rjson = search_res.json()
    #print(search_url)
   # print(search_rjson)
    try:
        book_id  = search_rjson['items'][0]['id']
        book_url = "https://www.googleapis.com/books/v1/volumes/" + book_id +"?key=keyy&fields=volumeInfo/categories"
        r = requests.get(book_url,headers=header)
        book_info = r.json()
        try:
            res = book_info['volumeInfo']['categories']
           # print(n)
           # print(res)
            s = ''.join(res)
            gen = re.split(', | /', s)
            length = len(gen)
            for i in range(length):
                if (gen[i] == ' ' + genbk or gen[i] == genbk):
                    p=p+1
                    print(p)
                    print(size)
                    print(n)
                    print('----------------')
                    # if(p==size):
                    #     os._exit(1)
        except KeyError:
            pass
    except KeyError:
        pass
    return p


print("Enter genre eg. Fiction ")
genbk = 'Thrillers'
print('No. of books u wanna look upon: ')
size = int(input())
print('Looking for ' + genbk + '... hold on!')
shelfList = ['I-3','D11','D12','D13','GR-1','GR-2','GR-3']
p = 0
for k in shelfList:
    print('Going for shelf '+k)
    url = 'http://172.31.1.40/cgi-bin/OPAC.exe?UName=&Option=PageView&SQL=SELECT+accNo,title,author,status,shelfNo+FROM+BookDetails+WHERE+shelfNo+LIKE+|{'+k+'{|+ORDER+BY+shelfNo+asc&pageSize=180&absolutePage=1'
    r = requests.get(url)
    bs = BeautifulSoup(r.text,"lxml")
    ht = bs.body.form.center.table
    inside = ht.tr.next_sibling.next_sibling.next_sibling.next_sibling.table.next_sibling
    for sibling in inside.tr.next_siblings:
    # print('=======================================')
        data = repr(sibling.td.next_sibling.next_sibling.string)
        p = info(data,genbk,size,p)
        if p == size:
            print('break') #isn't working
            sys.exit()

print(p)
# l = ['Fiction / Science Fiction / Action & Adventure', 'Fiction / Thrillers / General', 'Fiction / Science Fiction / Hard Science Fiction']
# s = ''.join(l)
# gen = re.split(', | /',s)
# length = len(gen)
# genre = 'Hard Science'
# for i in range(length):
#     if(gen[i]==' '+genre or gen[i]==genre):
#         print('----')
# print(len(gen))
