from enum import Enum
from msilib.schema import Error
import requests
from sqlalchemy import PrimaryKeyConstraint
from db.dbConnection import *
import pandas as pd
from db.dbschemes import get_db_table_dtype, get_db_table_pkeys
from  files_format_enums import * 



def fetch_and_save():
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


def read(filename:GTFSFilenames):
    content = []
    import zipfile
    with zipfile.ZipFile('staticData.zip') as myzip:
        with myzip.open(filename.name+".txt") as myfile:
            for line in myfile:
                line = line.decode('utf-8').replace('\n','').split(',')
                content.append(line)
    return content

def save_file_content_to_db(filename:GTFSFilenames):
    content = read(filename)
    df = pd.DataFrame(content[1:],columns=content[0])
    print(df)
    
    dtypes = get_db_table_dtype(filename)
    pkeys= get_db_table_pkeys(filename)
    add_Data(dataframe=df,table_name=filename.name,dtype = dtypes)  
    alter_table_add_pk(filename.name,pkeys)

def less_dumb_db_import():
    for filename in GTFSFilenames:
        try:
            save_file_content_to_db(filename=filename)
        except BaseException as err:
            print(err)
            pass



def get_data_scheme(dataframe,table_name,file :GTFSFilenames):
    pass

less_dumb_db_import()

