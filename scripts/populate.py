"""Redis communicator"""

import os
import redis

def main():
    r = redis.StrictRedis(host='redis')

    data_path = '/data'

    file_list = os.listdir(data_path)
    for file in file_list:
        r.lpush('workqueue', file)

   # r.set('nodename', 'rosina')
    #print r.get('nodename')
    #r.lpush('workqueue', 'mutant_22.jpg')

if __name__ == "__main__":
    main()