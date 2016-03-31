"""Redis worker"""

import os

import redis

from yeast_growth import generate_arguments_and_quantify_yeast

def main():
    r = redis.StrictRedis(host='redis')

    data_path = '/data'

    task_file = r.lpop('workqueue')

    while task_file is not None:
        fq_task_file = os.path.join(data_path, task_file)
        generate_arguments_and_quantify_yeast(fq_task_file)
        task_file = r.lpop('workqueue')


if __name__ == "__main__":
    main()