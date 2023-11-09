import configparser


def get_property(scope, key, default=None):
    try:
        value =  config.get(scope, key)
    except:
        value = default

    return value

def set_global(c=None):
    global __LOGGING_NAME__
    global __LOGGING_LEVEL__
    global config

    if c is None:
        config = configparser.RawConfigParser()
        config.read('config.properties')
    else:
        config=c


    __LOGGING_NAME__ = get_property('logging', 'name', "default")
    __LOGGING_LEVEL__ = get_property('logging', 'level' , "DEBUG")



set_global()
