"""
  #Purpose
  Script to set up a development environment in windows and linux computers without the need of having root access.
  If runed as root it will install the tools permanently if not the environment will be only temporal. For every programm installed it will
  Hash the content and it will perform the comparition with the check sums provided

  #Tools
  -Java:
      It will download the jdk from the provided url as a .zip
      it will extract it in the default path 
      And it will set up the appropiate environment variables for Path and JDK_HOME
  -Git:
      Downloads git from a given mirror and does the same process as java
  -Maven:
      Makes sure that jdk is installed and sets up the binaries for maven
  -Graddle:
      Same as Maven
  -Other Programs: Node, Docker, Npm and Pip packages
  -IDE´s: Visual Studio Code, Netbeans,

  Node -> https://nodejs.org/dist  
  node-v12.12.0-win-x64.zip
"""
import os
import requests
import zipfile
import io
import re
import json


Node = "https://nodejs.org/dist"
NodeIndex = f"{Node}/index.json"
def make_request(url):
    print(f"GET...{url}")
    response = requests.get(url)
    if response.ok:
        isJson = response.headers["Content-Type"] == "application/json"
        return response.json() if isJson else response.content
    else:
        print(f"Error when processing endpoint {url} status: {response.status_code}")
        return make_request(url)
    
def DownloadZip(url):
    file = make_request(url)
    z = zipfile.ZipFile(io.BytesIO(file))
    z.extractall()

if __name__ == "__main__":
    #now download
    routes = make_request(NodeIndex)
    findLts = lambda x: x["lts"] != False and x["security"] == True
    lts = filter(findLts, routes)
    lts = list(lts)[0]

    version = lts["version"]
    filename = f"node-{version}-win-x64.zip"
    zipRoute = f"{Node}/{version}/{filename}"
    DownloadZip(zipRoute)

