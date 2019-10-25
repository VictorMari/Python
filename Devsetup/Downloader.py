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
  vscode -> {
                osx: "https://go.microsoft.com/fwlink/?LinkID=620882",
                win: "https://aka.ms/win32-x64-user-stable",
                linux: "https://go.microsoft.com/fwlink/?LinkID=620884",
                linux64: "https://go.microsoft.com/fwlink/?LinkID=620884",
                linux32: "https://go.microsoft.com/fwlink/?LinkID=620885",
                linux64_deb: "https://go.microsoft.com/fwlink/?LinkID=760868",
                linux64_rpm: "https://go.microsoft.com/fwlink/?LinkID=760867",
                linux32_deb: "https://go.microsoft.com/fwlink/?LinkID=760680",
                linux32_rpm: "https://go.microsoft.com/fwlink/?LinkID=760681",
                win64: "https://go.microsoft.com/fwlink/?Linkid=852157",
                win64user: "https://aka.ms/win32-x64-user-stable",
                winzip: "https://go.microsoft.com/fwlink/?Linkid=850641",
                win32: "https://go.microsoft.com/fwlink/?LinkID=623230",
                win32user: "https://aka.ms/win32-user-stable",
                win32zip: "https://go.microsoft.com/fwlink/?LinkID=623231"
            }
"""
import os
import requests
import zipfile
import io
import re
import json


Node = "https://nodejs.org/dist"
NodeIndex = f"{Node}/index.json"
userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36"
coockies = {
    "msresearch"
}

java_cookies ={"oraclelicense": "accept-securebackup-cookie"}
def make_request(url):
    print(f"GET...{url}")
    headers = {"User-Agent": userAgent}
    response = requests.get(url, headers=headers, cookies = java_cookies)
    print(response)
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

def donwloadNode():
    #now download
    routes = make_request(NodeIndex)
    findLts = lambda x: x["lts"] != False and x["security"] == True
    lts = filter(findLts, routes)
    lts = list(lts)[0]

    version = lts["version"]
    filename = f"node-{version}-win-x64.zip"
    zipRoute = f"{Node}/{version}/{filename}"
    DownloadZip(zipRoute)

def downloadJava():
    url = "https://download.oracle.com/otn-pub/java/jdk/13.0.1+9/cec27d702aa74d5a8630c65ae61e4305/jdk-13.0.1_windows-x64_bin.zip"
    
    DownloadZip(url)

def downloadVSCode():
    codeUrl = "https://go.microsoft.com/fwlink/?Linkid=850641"
    DownloadZip(codeUrl)

if __name__ == "__main__":
    downloadJava()

