import sys
import logging
import os

if __name__ == "__main__":
    logging.basicConfig(filename='prova.log',level=logging.DEBUG,format='%(asctime)s - %(levelname)s - (%message)s')
    logging.info(os.getenv('USER')+ " Starting program")