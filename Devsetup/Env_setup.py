import requests
import json
import os
import zipfile
import re
import io
import subprocess
from hashlib import sha256
import shutil

class Resource:
    def __init__(self, download_strategy, verify_strategy, install_strategy):
        self.download_resource = download_strategy
        self.verify_hash = verify_strategy
        self.install_resource = install_strategy
        

    def download(self):
        self.file_bytes = self.download_resource()
    
    def verify(self):
        return self.verify_hash(self.file_bytes)

    def install(self):
        self.install_resource(self.file_bytes)

def make_request(url):
    print(f"GET...{url}")
    response = requests.get(url)
    print(response)
    if response.ok:
        isJson = response.headers["Content-Type"] == "application/json"
        return response.json() if isJson else response.content
    else:
        print(f"Error when processing endpoint {url} status: {response.status_code}")
        return make_request(url)

def Node_strategies(configs):
    def Download_Strategy():
        #find latest stable release
        index_file = f"{configs['url']}/{configs['Index-path']}"
        routes = make_request(index_file)
        findLts = lambda x: x["lts"] != False and x["security"] == True
        lts = filter(findLts, routes)
        lts = list(lts)[0]

        #construct url
        Node_url = configs['url']
        version = lts["version"]
        file_type = configs['file']
        file_name = f"node-{version}-{file_type}"
        Node_file = f"{Node_url}/{version}/{file_name}"
        hash_file = f"{Node_url}/{version}/SHASUMS256.txt"
        configs["HashFile"] = hash_file
        return make_request(Node_file)

    def verify_strategy(bytes):
        downloaded_file_hash = sha256(bytes).hexdigest()
        hashes = make_request(configs["HashFile"])
        hashes = str(hashes)
        hash_index = hashes.rfind(downloaded_file_hash)
        return hash_index >= 0
        
    def install_strategy(bytes):
        z = zipfile.ZipFile(io.BytesIO(resource.file_bytes))
        z.extractall()
        name = z.infolist()[0].filename
        current_directory = os.getcwd()
        origin_path = os.path.join(current_directory, name)
        destination_path = os.path.join(configs['Installation']['Path'], name)
        shutil.move(origin_path, destination_path)
        print(f"Moving directory: {destination_path}\n destination: {destination_path}")

        #set up permanent env variables
        #"[Environment]::SetEnvironmentVariable("DCRCLIFILE", "C:\Users\pzsr7z\Desktop\DCRCLIFILE.txt", "User")"
        binaries = os.path.join(destination_path, "/node.exe")
        variable_name = configs["Installation"]["Variables"][0]
        command = f'[Environment]::SetEnvironmentVariable("{variable_name}", "{binaries}", "User")'
        env_proces = subprocess.run(["powershell.exe", command], stderr=True)
        print(f"Setting env variable: {variable_name}: {binaries}")
        print(env_proces.stderr)
    return [Download_Strategy,verify_strategy,install_strategy]



if __name__ == "__main__":
    with open("config.json", "r") as f:
        config  = json.load(f)["Node"]
        config["file"] = config["file-types"]["Windows"][7]
        stg = Node_strategies(config)

        resource = Resource(*stg)
        resource.download()
        if resource.verify() == True:
            resource.install()
