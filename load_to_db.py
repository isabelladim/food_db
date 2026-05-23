import pandas as pd
from sqlalchemy import create_engine
from pathlib import Path
import os 
from dotenv import load_dotenv
from sqlalchemy.engine import URL

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

SKIP_SHEETS = {"Contents"}


def load_data(filepath) -> dict[str, pd.DataFrame]:
    #Load all sheets from an AUSNUT Excel file  
    all_sheets = pd.read_excel(filepath, sheet_name=None,skiprows=2)
    return {
        sheet: df 
        for sheet, df in all_sheets.items() 
        if sheet not in SKIP_SHEETS
    }

def upload_to_postgres(df, table_name, engine) -> None:
    df.to_sql(table_name, engine, schema="raw", if_exists='replace', index=False)

def main():
    #load env file
    load_dotenv()

    port_number = os.getenv("DB_PORT")
    db_host = os.getenv("DB_HOST")
    db_name = os.getenv("DATABASE_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_folderpath = os.getenv("DB_FOLDER_PATH")

    connection_url = URL.create(
    drivername="postgresql+psycopg2",
    username=db_user,
    password=db_password,  
    host=db_host,
    port=port_number,
    database=db_name)

    engine = create_engine(connection_url)

    print(engine)
    
    #upload to DB
    folder_path = Path(db_folderpath)
    for file in folder_path.iterdir():
        if file.is_file():
            logger.info(f"Processing file: {file.name}")
            try:
                dfs = load_data(file)
                for sheet_name, df in dfs.items():
                    upload_to_postgres(df, sheet_name, engine)
            except Exception as e:
                logger.error(f"Failed to process {file.name}: {e}")
                continue
    logger.info("Ingestion complete")

if __name__ == "__main__":
    main()