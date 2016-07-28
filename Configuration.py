"""
Module for containing all required initialization logic.

It exposes a function that should ALWAYS be indepotent,
which means that it can be called one or possible multiple
times without creating fatal errors (other than those originated
by latency.)
"""
import sys
import logging
import logging.config
import os
from os.path import join, dirname
from dotenv import load_dotenv


def load():
    """Load and check all the necessary configuration options"""
    # Load environment variables from envfile if present
    ENVFILE_PATH = join(dirname(__file__), '..', '.env')
    load_dotenv(ENVFILE_PATH)

    # Load logging setup
    LOGFILE_PATH = join(dirname(__file__), '..', 'logging.conf')
    logging.config.fileConfig(LOGFILE_PATH)

    productiononly = {'EMAIL_USER',
                      'EMAIL_PASSWORD',
                      'EMAIL_RECIPIENTS'}

    alwaysRequired = {'AVALUOS_DB_URL',
                      'AVALUOS_DB_POOL_SIZE',
                      'FOVISSSTE_DB_URL',
                      'FOVISSSTE_DB_POOL_SIZE'}

    reqs = set()

    if os.getenv('FLASK_ENV') == 'dev':
        required = reqs.union(alwaysRequired)
    else:
        required = reqs.union(productiononly | alwaysRequired)

    real = set(os.environ.keys())

    bad = False
    diff = required - real
    if len(diff) > 0:
        bad = True
        logging.error('Missing environment variables: %s', ', '.join(diff))

    if bad:
        sys.exit(1)
    else:
        logging.info('All environment variables are valid.')


if __name__ == '__main__':
    load()
