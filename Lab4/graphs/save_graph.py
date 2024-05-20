import matplotlib.pyplot as plt

import os
import time
import base64
import cv2


def graph_to_b64(id, save_path):
    folder_path = "/".join(save_path.split("/")[:-1])
    os.makedirs(folder_path, exist_ok=True)

    file_path = f"{save_path}{id}.png"
    plt.savefig(file_path)
    plt.close()
    time.sleep(0.1)

    img = cv2.imread(file_path)
    b64 = base64.b64encode(cv2.imencode('.jpg', img)[1]).decode()
    time.sleep(0.1)

    os.remove(file_path)

    return b64