import os
import json

import launchmy







def getConfig():
    with open("config.json", 'r') as configFile:
        config = json.load(configFile)
        return config["launchpadLink"], config["wallets"]



config = getConfig()


isWindows = True if os.name == 'nt' else False


if "launchmynft.io" in config[0]:
    print("Found launchmynft.io link")
    for wallet in config[1]:
        print(f"\nProcessing wallet: {wallet['name']}")
        launchmy.mint([config[0]], isWindows, wallet)
else:
    print("Could not recognize link")

