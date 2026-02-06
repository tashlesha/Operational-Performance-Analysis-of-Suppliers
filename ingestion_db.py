import pandas as pd
import os
from sqlalchemy import create_engine
import logging
import time

print("Pipeline starting...")

# auto-create logs folder
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
    force=True
)

engine = create_engine('sqlite:///inventory.db')

def ingest_db(df, table_name, engine):
    df.to_sql(table_name, con=engine, if_exists='replace', index=False)

folder_path = r'C:\Users\Raksha\Desktop\Ashlesha\VPD\data'

def load_raw_data():
    start = time.time()
    
    for file in os.listdir(folder_path):
        if file.endswith('.csv'):
            print("Processing:", file)
            
            df = pd.read_csv(os.path.join(folder_path, file))
            
            logging.info(f'Ingesting {file}')
            ingest_db(df, file[:-4], engine)

    end = time.time()
    total_time = (end - start)/60
    
    logging.info("Ingestion Complete")
    logging.info(f"Total Time Taken: {total_time} minutes")

    print("Pipeline finished ✅")

load_raw_data()
