from abc import ABC, abstractmethod
from src.service import postgres
from src.utils import env
import io
from werkzeug.datastructures import FileStorage 
import logging
import json

logger = logging.getLogger(env.__LOGGING_NAME__)

import sys 

sys.path.append(".")

from src.utils.exceptions import AppException


class Loader(ABC):
    """
        Pending documentatios
    """
    @abstractmethod
    def validate(self):
        pass

    @abstractmethod
    def load(self):
        pass

    def __init__(self, source, request, dababase, table):
        self.source = source
        self.request = request
        self.table = table
        self.database = dababase


        self.validate()

class Test(Loader):
    """
        Teesting loader 
    """
    def __init__(self, request, dababase, table):
        super().__init__('test', request, dababase, table)

    def validate(self):
        pass

    def load(self):
        """
            Done for testing purpose.
            We have to transfor any file content into a werkzeug.datastructures.FileStorage and then load the data into postgres
        """

        content = b"""brand , model, year
brand_a,model_a,2000
brand_b,model_b,2022"""

        f = io.BytesIO(content)
        file = FileStorage(f)
        header = not self.request.args.get("header", "true").strip().lower() in ['false', 'no', 'not', '0']

        postgres.load(file_storage=file, table_name=self.table, database=self.database, header=header)

        return  { 'msg' : 'the table was loaded successfully'} , 200


class Aws(Loader):
    """
        AWS loader pending to develop
    """
    def __init__(self, request, dababase, table):
        super().__init__('aws', request, dababase, table)

    def validate(self):
        pass

    def load(self):
        raise AppException("We are sorry, it was not not implemented any loader for AWS so far." , 501)
        # raise Exception(f"We are sorry, it was not not implemented any loader for AWS so far.")

class Gcp(Loader):
    """
        GCP loader pending to develop
    """
    def __init__(self, request, dababase, table):
        super().__init__('gcp', request, dababase, table)

    def validate(self):
        pass

    def load(self):
        raise AppException(f"We are sorry, it was not not implemented any loader for GCP so far.", 501)

class Content(Loader):

    def __init__(self, request, dababase, table):
        logger.info("Content loader instantiated")
        super().__init__('content', request, dababase, table)

    def validate(self):
        logger.info("validating the request")

        if self.request is None:
            raise AppException("Invalid request object", 500)

        if self.table is None or self.database is None:
            raise AppException(f"Invalid database [{self.database}] or table [{self.table}]", 500)

        file = self.request.files.get('file', None)
        if file is None:
            raise AppException("It has to be passed a file form-data as parameter named ´file´. See documentation for more details", 400)


    def load(self):
        logger.info("initiate the loading process")
        self.validate()

        file = self.request.files.get('file')

        header = not self.request.args.get("header", "true").strip().lower() in ['false', 'no', 'not', '0']
        logger.debug(f"header : {header}")

        postgres.load(file_storage=file, table_name=self.table, database=self.database, header=header)

        return  { 'msg' : 'the table was loaded successfully'} , 200
 

def health():
    print(env.__LOGGING_NAME__)

def Factory(request, source, database, table):
    """ 
        Factory Method

    """
    loaders = {
        "content": Content,
        "gcp": Gcp,
        "aws": Aws,
        "test": Test,
    }
 
    logger.info("called the Factory method")
    logger.debug(f"   source   : {source}")
    logger.debug(f"   database : {database}")
    logger.debug(f"   table    : {table}")
    logger.debug(f"availabel loaders :")
    logger.debug(str(loaders))

    loader = loaders.get(source.strip().lower(), None)
    logger.debug(f"loaded loader {loader}")

    if loader is None:
        raise AppException(f"It was not found any loader for ´{source}´. See https://github.com/zioli/challenge-api for more information", 400)


    return loader(request, database, table)















