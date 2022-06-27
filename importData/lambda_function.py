from concurrent.futures import ProcessPoolExecutor
import sys
import logging
import rds_config
import psycopg2

from utils import recoverFromCSV, scrapeInsert

# rds settings
rds_host  = rds_config.rds_host
username  = rds_config.db_username
password  = rds_config.db_password
db_name   = rds_config.db_name
db_port   = rds_config.db_port

logger = logging.getLogger('')
logger.setLevel(logging.INFO)

try:
    conn = psycopg2.connect(database=db_name, user=username, password=password, host=rds_host, port=db_port, connect_timeout=5)
except psycopg2.OperationalError as e:
    logger.error("ERROR: Unexpected error: Could not connect to PostgreSQL instance.")
    logger.error(e)
    sys.exit()

logger.info("SUCCESS: Connection to RDS PostgreSQL instance succeeded")

def lambda_handler(event, context):
    """
    This function import the data from Video_Games.csv
    and scrape new data into database.
    """
    
    # Recover from default csv
    recoverFromCSV(conn=conn)
    logger.info('recover from csv is done.')
    
    # Scrape and Insert
    scrapeInsert(conn=conn)

    item_count = 0
    with conn.cursor() as cur:
        cur.execute("select * from Video_Games")
        for row in cur:
            item_count += 1
            # print(row)
    conn.commit()

    return "Total %d items in RDS PostgreSQL table" % (item_count)