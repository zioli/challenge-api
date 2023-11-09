import configparser
import pytest
import logging 
from src.utils import env

logger = logging.getLogger("tester")
logger.setLevel(logging.getLevelName("DEBUG"))

def test_GetProperty(mocker):

    c = configparser.RawConfigParser()
    c['postgres'] =  {
        'database.dbname': 'test_dbname',
        'database.user': 'test_dbuser',
        'database.password': 'test_dbpassword',
        'host': 'test_localhost',
        'port': '0000',
        'load.lines_limit': '9999'
    }

    c['logging'] =  {
        'name': 'test_challenge', 
        'level': 'test_level'

    }

    mocker.patch("src.utils.env.config", c)

    assert env.get_property("postgres", "database.dbname") == "test_dbname"
    assert env.get_property("postgres", "database.user") == "test_dbuser"
    assert env.get_property("postgres", "database.password") == "test_dbpassword"
    assert env.get_property("postgres", "host") == "test_localhost"
    assert env.get_property("postgres", "port") == '0000'
    assert env.get_property("postgres", "load.lines_limit") == '9999'

    assert env.get_property("logging", "name") == 'test_challenge'
    assert env.get_property("logging", "level") == 'test_level'

    assert env.get_property("not_existing_scope", "not_existing_attribute", "default_value") == 'default_value'
    assert env.get_property("postgres", "not_existing_attribute", "default_value_testing") == 'default_value_testing'
    assert env.get_property("postgres", "not_existing_attribute_without_default_value") == None

def test_GlobalVariables_default_value(mocker):
    c = configparser.RawConfigParser()

    c['logging'] =  {}

    env.set_global(c)

    assert env.__LOGGING_NAME__ == 'default'
    assert env.__LOGGING_LEVEL__ == 'DEBUG'
