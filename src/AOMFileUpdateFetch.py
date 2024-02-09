import requests
from bs4 import BeautifulSoup
url = "https://transport.data.gouv.fr/api/datasets/5d31d8b69ce2e703da90b699"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
rep = requests.get(url, headers=headers)
rep.encoding = 'utf-8'
html = rep.text
print(html)