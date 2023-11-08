from flask import Flask, jsonify, request, Response

from src.utils.exceptions import AppException

from src.service import loader as docker, postgres
from src.utils import env

import json
import logging 

app = Flask(__name__)


def get_logger():
    logging.basicConfig(
        format=f"[%(asctime)s.%(msecs)03d][%(levelname)s][%(funcName)s()] %(message)s",
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger = logging.getLogger(env.__LOGGING_NAME__)
    logger.setLevel(logging.getLevelName(env.__LOGGING_LEVEL__))

    return logger

def check():
    logger.info("Checking the postgres conection based on the config.properties file")

    try:
        postgres._get_connection().close()
        logger.info("Connection ok")

    except Exception as e:
        logger.info("It was not possible to connect to postgress")
        logger.info(e)
        logger.info("it may be missing the file config.property or some of its attributes: ")    
        logger.info("    [postgres]")
        logger.info("    database.dbname=<dbname>")
        logger.info("    database.user=<user_name>")
        logger.info("    database.password=<password>")
        logger.info("    host=<host>")
        logger.info("    port=<port>")
        logger.info("    load.lines_limit=<lines_limit>")
        logger.info("    ") 
    logger.info("Checking done")

logger = get_logger()
logger.info("Initiating websever")
check()

@app.route('/migration/load/historic/<source>/<database>/<table>', methods=['POST'])
def historic_load(source, database, table):
    try:
        logger.debug("calling '/migration/load/historic/<source>/<database>/<table>'")

        loader = docker.Factory(request=request, source =source, database=database, table=table)

        response, status = loader.load()

        return Response(response=json.dumps(response), status=status, mimetype='application/json')

    except AppException as e:
        r = {'msg':str(e.message)}
        return Response(response=json.dumps(r), status=e.status_code, mimetype='application/json')

if __name__ == '__main__':
    app.run(port=8000, debug=True)
