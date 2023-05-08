import configparser

def read_conf_insert_data(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    config.sections()
    # Store the URL of your InfluxDB instance
    my_url = config['questdb.parameters']['url']
    secs_interval = config['questdb.parameters']['secs_interval']
    table = config['questdb.parameters']['table']
    dbname = config['questdb.parameters']['dbname']

    return my_url, secs_interval, table, dbname

def read_conf_fetch_data(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    config.sections()
    # Store the URL of your InfluxDB instance
    my_url = config['questdb.parameters']['url']
    user = config['questdb.parameters']['user']
    password = config['questdb.parameters']['password']
    table = config['questdb.parameters']['table']
    dbname = config['questdb.parameters']['dbname']
    port = config['questdb.parameters']['port']

    return my_url, user, table, dbname, password, port