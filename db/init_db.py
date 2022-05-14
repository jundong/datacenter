import os, logging, json
import pandas as pd
import numpy as np
from db import mongo_db

logger = logging.getLogger(__name__)

def init_db() -> None:
    init_data_path = os.path.join(os.path.dirname(__file__), "init_data")
    files = ['sites.csv', ]
    for file in files:
        file_path = os.path.join(init_data_path, file)
        df = pd.read_csv(file_path, sep=",")
        logger.info(f"{file_path}  load successed")
        table_name = file.replace(".csv", "")
        collection = mongo_db[table_name]
        collection.insert(json.loads(df.T.to_json()).values())