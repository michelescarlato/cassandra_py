import logging
import sys
import os
import fnmatch
from datetime import datetime
from datetime import timedelta
import time
import socket

import numpy as np

from mira_utils import read_conf,convert_seconds

import pandas as pd
#import pyarrow
from cassandra.cluster import Cluster

from cassandra import ConsistencyLevel
from cassandra.query import BatchStatement

CASSANDRA_PARTITION_NUM = 1500


def write_db_bulk(df, table):
    # cassandra_cluster = Cluster('ip')
    # session = cassandra_cluster.connect('keyspace')
    #df = df.iloc[:, : 6]
    #column_names_to_edit = list(df.columns.values)
    #column_names = column_names_to_edit.pop('timems')
    column_names = list(df.columns.values)
    print(column_names)
    cql_desc = f"""DESC {keyspace}"""
    cql_query_create = """
        CREATE {table_name} ({col_names})
        """.format(table_name=table, col_names=','.join(map(str, column_names)))
    prepared_query = session.prepare(cql_query_create)
    session.execute(prepared_query)
    '''
    cql_query_insert_into = """
        INSERT INTO {table_name} ({col_names})
        VALUES (?,?,?,?,?,?)
        """.format(table_name=table, col_names=','.join(map(str, column_names)))
    for partition in split_to_partitions(df, CASSANDRA_PARTITION_NUM):
        batch = BatchStatement(consistency_level=ConsistencyLevel.QUORUM)
        for index, item in partition.iterrows():
            batch.add(prepared_query, (item.id, item.name))
        session.execute(batch)
'''
def split_to_partitions(self, df, partition_number):
    permuted_indices = np.random.permutation(len(df))
    partitions = []
    for i in range(partition_number):
        partitions.append(df.iloc[permuted_indices[i::partition_number]])
    return partitions


# connection test
'''
row = session.execute(f"SELECT release_version FROM {table}").one()
if row:
    print(row[0])
'''


def load_data(url, csv_dir, epoch, secs_interval, table):
    currentTime = datetime.utcnow()
    print(currentTime)
    while epoch < currentTime:
        print(epoch)
        dir = 0
        while dir <= 2:
            file = 0
            count = len(fnmatch.filter(os.listdir(csv_dir + str(dir)), '*.*'))
            while file < count:
                csv_filename = csv_dir + str(dir) + '/' + str(file) + ".csv"
                if epoch > currentTime:
                    return epoch
                epoch = write_csv_data_to_db_250_values(csv_filename, url, epoch, secs_interval, currentTime, table)
                file = file + 1
            dir = dir + 1
    logging.info('Last data inserted at time _ epoch inside load data: ' + str(epoch))
    print(epoch)
    return epoch


def write_csv_data_to_db_250_values(csv_file, url, new_epoch, secs_interval, currentTime, table):
    data = pd.read_csv(csv_file, sep=',')
    # take the first 250 values
    first_column = data.iloc[:,0]
    second_n_column = data.iloc[:, 1:249].astype(float)
    third_column = data.loc[:,'m001_abs_good']
    row_index = 0
    if new_epoch > currentTime:
        return new_epoch
    for t in first_column:
        # increasing timestamp by x secs
        new_epoch = new_epoch + timedelta(seconds=int(secs_interval))
        first_column.iat[row_index] = new_epoch#, tz='UTC')
        row_index = row_index + 1
    result = pd.concat([first_column, second_n_column,third_column], axis=1)
    write_db_bulk(result, table)
    return new_epoch

'''
def write_db_bulk(data, table):
    # questdb accepts datetime64 nanoseconds format
    data["timems"] = data["timems"].astype("datetime64[ns]")
    with Sender('localhost', 9009) as sender:
        sender.dataframe(data, table_name=table)#, at='timems')

    global points_inserted_count
    points_inserted_count = points_inserted_count + len(data.index)
    print("after bulk write - points inserted so far:" + str(points_inserted_count))
    return
'''

log_name = str(datetime.now())
log_name = log_name.replace(" ","_")
hostname = str(socket.gethostname())
print(log_name)
logging.basicConfig(filename="logs/Insert_data_"+hostname+"_"+str(log_name)+"_run.log", level=logging.INFO)

print(socket.gethostname())
logging.info("Result object: "+hostname)

file_name = sys.argv[1]

url, secs_interval,table, keyspace, port = read_conf.read_conf_insert_data(file_name)
cluster = Cluster([url], port=port)
session = cluster.connect()

# start script temporizer
start = time.time()

points_inserted_count = 0
epoch = datetime.utcnow() - timedelta(days=30)

url, secs_interval,table, dbname, port = read_conf.read_conf_insert_data(file_name)
csv_dir = 'CSV_machine_data/'

# load the CSVs and get the last recorded time inserted
time_end = load_data(url, csv_dir, epoch, secs_interval, table)
print('Last data inserted at time: '+str(time_end))
logging.info('Last data inserted at time: '+str(time_end))
print("Total number of points inserted:" + str(points_inserted_count))
logging.info("Total number of points inserted:" + str(points_inserted_count))

end = time.time()

elapsed_time = end - start
minutes = convert_seconds.convert_seconds(elapsed_time)
print("Total time elapsed:")
print(minutes)
logging.info("Total time elapsed (hh:mm:ss): "+str(minutes))
logging.info("Seconds interval: "+str(secs_interval))
