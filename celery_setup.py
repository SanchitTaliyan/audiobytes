import os
from subprocess import Popen
from time import sleep

from config import cfg

def create_log_file_if_not_exists(log_file):
    log_dir = os.path.dirname(log_file)

    # Ensure the log directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Ensure the log file exists
    if not os.path.exists(log_file):
        open(log_file, 'a').close()

def terminate_processes(processes: list[Popen]):
    for process in processes:
        try:
            process.terminate()
        except Exception as e:
            print(f"Error terminating process: {e}")

queue_config = {
    'default': {
        "concurrency": 1,
        "autoscale": "10,1",
    }
}

celery_path = "/venv/bin/celery"
log_path = "/home/ubuntu/audiobytes/logs"

if __name__ == "__main__":

    # celery workers
    worker_processes: list[Popen] = []
    for queue in queue_config.keys():
        worker_log_file = f"{log_path}/{queue}_worker.log"

        create_log_file_if_not_exists(worker_log_file)

        command = (
            f"{celery_path} -A proj worker "
            f"-Q {queue} "
            f"-l INFO "
            f"--concurrency={queue_config[queue]["concurrency"]} "
            f"--autoscale={queue_config[queue]["autoscale"]} "
            f"--logfile={worker_log_file} "
            f"--hostname=worker@{queue} "
            f"-E")
        worker_processes.append(Popen(command, shell=True))

    try:
        for worker_process in worker_processes:
            worker_process.wait()

    except Exception:
        print("\nTerminating processes...")
        terminate_processes(worker_processes)
        print("All processes terminated. Exiting.")