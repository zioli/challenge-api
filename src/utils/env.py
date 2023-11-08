import configparser

global __LOGGING_NAME__
global __LOGGING_LEVEL__
global config

config = configparser.RawConfigParser()
config.read('config.properties')

def get_property(scope, key, default=None):
    try:
        value =  config.get(scope, key)
    except:
        value = default

    return value


__LOGGING_NAME__ = get_property('logging', 'name', "default")
__LOGGING_LEVEL__ = get_property('logging', 'level' , "DEBUG")


