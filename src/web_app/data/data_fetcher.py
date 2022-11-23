import sys
import pandas as pd
sys.path.append("../..")
import db.dbConnection as db

engine = db.get_engine()

def select_raw_data():
    return pd.DataFrame( engine.execute('select * from raw_rt_data limit 100;'))

