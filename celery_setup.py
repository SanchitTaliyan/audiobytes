from subprocess import Popen

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

if __name__ == "__main__":

    # celery workers
    worker_processes: list[Popen] = []
    for queue in queue_config.keys():
        command = (
            f"{celery_path} -A proj worker "
            f"-Q {queue} "
            f"-l INFO "
            f"--concurrency={queue_config[queue]["concurrency"]} "
            f"--autoscale={queue_config[queue]["autoscale"]} "
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