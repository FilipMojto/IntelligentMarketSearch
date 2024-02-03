import multiprocessing as mpr
import multiprocessing.connection as mpr_conn
import time

def process_1(conn_1: mpr_conn.PipeConnection, conn_2: mpr_conn.PipeConnection):
    while True:
        data = ""
        if conn_1.poll(timeout=0.01):
            data = conn_1.recv()
            print(f"Process 1 received: {data}")
            conn_2.send(f"Process 1 acknowledges receipt of: {data}")
        time.sleep(1.5)

def process_2(conn_1: mpr_conn.PipeConnection, conn_2: mpr_conn.PipeConnection):
    while True:
        data = "Hi, there!"
        print(f"Process 2 sending data: {data}.")
        conn_1.send(data)
        response = conn_2.recv()
        print(f"Process 2 received response: {response}")
        time.sleep(1.5)

if __name__ == "__main__":
    conn_1, conn_2 = mpr.Pipe()  # Create one pipe for each direction

    proc_1 = mpr.Process(target=process_1, args=(conn_1, conn_2))
    proc_2 = mpr.Process(target=process_2, args=(conn_2, conn_1))

    proc_1.start()
    proc_2.start()

    proc_1.join()
    proc_2.join()