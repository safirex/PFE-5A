import requests


url = "https://data.explore.divia.fr/api/datasets/1.0/gtfs-divia-mobilites/attachments/gtfs_diviamobilites_current_zip"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}
rep = requests.get(url, headers=headers)
rep.encoding = 'utf-8'
# html = rep.text
print(rep.raw)
byte = rep.content
file = open('staticData.zip', 'wb') #write byte
# file = open('data.gtfs', 'w') 

file.write(byte)
file.close()

# r = http.request('GET', 'https://data.explore.divia.fr/api/datasets/1.0/gtfs-divia-mobilites/attachments/gtfs_diviamobilites_current_zip')