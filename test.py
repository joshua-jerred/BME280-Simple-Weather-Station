import dsws
import threading
import time


def collectThread():
    while True:
        dsws.Collect("config.json")
        print("Collected")
        time.sleep(3)


def startServerThread():
    dsws.StartServer("config.json")


if __name__ == "__main__":
    collect = threading.Thread(target=collectThread)
    collect.start()
    startServer = threading.Thread(target=startServerThread)
    startServer.start()
    collect.join()
    startServer.join()
