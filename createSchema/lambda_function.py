import sys
import logging
import rds_config
import psycopg2

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
    This function create the schema.
    """

    with conn.cursor() as cur:
        cur.execute(open("createSchema.sql", "r").read())
    conn.commit()

    return "Schema is updated."