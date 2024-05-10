import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib

from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

import os

dir_path = "../output/building/"
print_path = "../print/"

files = os.listdir(dir_path)


for file in files:
    # df にする
    df = pd.read_csv(dir_path+file)

    id = file.split(".")[0]

    # lod ごとに分ける "lod" = 0 , 1
    lod_0_df = df[df['lod'] == 0]
    lod_1_df = df[df['lod'] == 1]

    # lat と lon で散布図を描く
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(2, 2, 1)
    ax.plot(lod_0_df['lon'], lod_0_df['lat'], 'o-')
    ax.set_xlabel('lon')
    ax.set_ylabel('lat')
    plt.savefig(print_path+id+"_lod0.png") 

    # lat と lon で散布図を描く
    fig = plt.figure(figsize=(20, 20))
    for i in range(4):
        ax = fig.add_subplot(2, 2, i+1, projection='3d')
        ax.plot(lod_1_df['lon'], lod_1_df['lat'],lod_1_df['height'], 'o-')
        ax.set_xlabel('lon')
        ax.set_ylabel('lat')
        ax.set_zlabel('floor')
        ax.view_init(azim=0+i*45, elev=15)
    plt.savefig(print_path+id+"_lod1.png") 