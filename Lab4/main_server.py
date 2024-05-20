import server.graph_server
import server.recommendations_server

import multiprocessing


def create_thread(target, name):
    process_name = f"{name}_process"
    thread = multiprocessing.Process(target=target, name=process_name)
    thread.daemon = True
    thread.start()
    print(f"\nStarting {process_name}...")
    return thread


graph_thread = create_thread(server.graph_server.thread, "graph")
server.recommendations_server.thread()
