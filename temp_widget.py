#!/usr/bin/env python3


import matplotlib
import matplotlib.pyplot as plt

import subprocess
import sys

import time

import os

import pandas as pd

SSH_USER = "lfhcal"
SSH_HOST = "lfhcal-rpi.dyndns.cern.ch"
REMOTE_DATA_DIR = "/home/lfhcal/TempDAQ/temp_daq"

SLEEPTIME = 10  # seconds

if __name__ == "__main__":
    plt.ion()

    while True:
        p = subprocess.run(["ssh", f"{SSH_USER}@{SSH_HOST}", "ls -1rt", REMOTE_DATA_DIR, "|", "tail", "-1"], capture_output=True)
        latest_file = p.stdout.decode("utf-8").strip()
       
        p = subprocess.run(["scp", f"{SSH_USER}@{SSH_HOST}:{REMOTE_DATA_DIR}/{latest_file}", f"data/{latest_file}"], capture_output=True)
        if p.returncode != 0:
            print("Error downloading file:")
            print(p.stderr.decode("utf-8"))
        else:
            pass
            #print(f"File {latest_file} downloaded successfully.")

        df = pd.read_csv(os.path.join("data", latest_file))
        df.columns = [col[0] for col in df.columns]

        df["t"] = pd.to_datetime(df["t"])

        plt.clf()
        for col in df.columns:
            if col not in ["t"]:
                plt.plot(df["t"], df[col], label=f'{col}: {df[col].iloc[-1]:.2f} C')

        plt.xlabel("Time")
        plt.ylabel("Temperature (C)")
        plt.title("Raspberry Pi Temperature DAQ")
        plt.legend()
        
        plt.show()
        plt.pause(SLEEPTIME)