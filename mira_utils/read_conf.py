import configparser

def read_conf_insert_data(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    config.sections()
    # Store the URL of your InfluxDB instance
    my_url = config['cassandra.parameters']['url']
    secs_interval = config['cassandra.parameters']['secs_interval']
    table = config['cassandra.parameters']['table']
    keyspace = config['cassandra.parameters']['keyspace']
    port = config['cassandra.parameters']['port']

    return my_url, secs_interval, table, keyspace, port

def read_conf_fetch_data(conf_file):
    config = configparser.ConfigParser()
    config.read(conf_file)
    config.sections()
    # Store the URL of your InfluxDB instance
    my_url = config['cassandra.parameters']['url']
    user = config['cassandra.parameters']['user']
    password = config['cassandra.parameters']['password']
    table = config['cassandra.parameters']['table']
    keyspace = config['cassandra.parameters']['keyspace']
    port = config['cassandra.parameters']['port']

    return my_url, user, table, keyspace, password, port