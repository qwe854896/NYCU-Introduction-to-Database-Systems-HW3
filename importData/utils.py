import pandas as pd
import logging

def recoverFromCSV(conn):
    # Create temp table
    with conn.cursor() as cur:
        cur.execute(open("preprocess.sql", "r").read())
        conn.commit()

    # Import from csv to temp
    copy_sql = """
          COPY temp FROM stdin WITH CSV HEADER
          DELIMITER as ','
          """

    file_name = "Video_Games.csv"
    with open(file_name, 'r') as f:
        # next(f)
        conn.cursor().copy_expert(sql=copy_sql, file=f)
        conn.commit()

    # import temp to Video_Games
    with conn.cursor() as cur:
        cur.execute(open("importData.sql", "r").read())
        conn.commit()

from SQL import fetchConn

def dfToTemp(df):
    try:
        conn = fetchConn().connect()
        df.to_sql('temp', con=conn, if_exists='replace', index=False)
    except Exception as e:
        logging.info(e)


from scrape import scrapeTodf

def scrapeInsert(conn):
    logging.info('Scraping is started.')
    df = scrapeTodf()
    logging.info('Scraping is done.')
    
    logging.info('Importing data is started.')
    dfToTemp(df)
    logging.info('Importing data is done.')
    
    # import temp to Video_Games
    with conn.cursor() as cur:
        cur.execute(open("importData.sql", "r").read())
        conn.commit()