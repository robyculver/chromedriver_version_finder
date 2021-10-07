import platform
import subprocess
import glob
import re
import packaging
from packaging import version
import requests
import zipfile
import os

##simple script to test capturing version info from multi OS types and versions

#capture platform information
def getOSInfo():
  osPlatform = (platform.platform())
  #mac version capture
  if 'macos' in osPlatform.lower():
    osType = 'mac'
    chromeVersion = list(set(re.findall("(?:[0-9]*\.){3}[0-9]*", subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--version"], capture_output=True, text=True).stdout)))
    chromeVersion = chromeVersion[0]
    #is the processor intel or m1?
    if platform.processor() == 'i386':
      driverType = 'mac64'
    if platform.processor() == 'arm':
      driverType = 'mac64_m1'
  #windows version capture
  elif 'windows' in osPlatform.lower():
    print(osPlatform)
    osType = 'win'
    #handle multiple install directories
    chromeDir = glob.glob("C:\\Program Files (x86)\\Google\\Chrome\\Application\\**\\", recursive=True)
    if not chromeDir:
      chromeDir = glob.glob("C:\\Program Files\\Google\\Chrome\\Application\\**\\", recursive=True)
    chromeDirStr = ''.join(chromeDir)
    parsedVers = []
    for i in list(set(re.findall("(?:[0-9]*\.){3}[0-9]*", chromeDirStr))):
      parsedVers.append(version.parse(i))
    chromeVersion = str(max(parsedVers))
    driverType = 'win32'
  #linux version capture
  elif 'linux' in osPlatform.lower():
    osType = 'linux'
    chromeVersion = subprocess.run(["google-chrome", "--version"])
    driverType = 'linux64'
  return chromeVersion, driverType

def verifyDirectoryExists(path):
  if not os.path.isdir(path):
    print(f"{path} doesn't exist...creating")
    os.makedirs(path)
  return os.path.isdir(path)

def removeZip(path):
  if os.path.isfile(path):
    os.remove(path)
  return os.path.isfile(path)

def getDriver(outputPath=None, deleteZip=True):
  if outputPath:
    if outputPath[-1] == '/' or outputPath[-1] == '\\':
      outputPath = outputPath[:-1]
    if '~' in outputPath:
      outputPath = os.path.expanduser(outputPath)
    verifyDirectoryExists(outputPath)
  chromeVersion, driverType = getOSInfo()
  #chrome driver version must match major version of chrome (1st Octet)
  majorVersion = chromeVersion.split('.')[0]
  chromeDriverVersion = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{chromeVersion.split('.')[0]}").text
  response = requests.get(f'https://chromedriver.storage.googleapis.com/{chromeDriverVersion}/chromedriver_{driverType}.zip')
  totalbits = 0
  if response.status_code == 200:
    if not outputPath:
      outputPath = '.'
    zipLocation = f'{outputPath}/chromedriver.zip'
    with open(zipLocation, 'wb') as f:
      for chunk in response.iter_content(chunk_size=1024):
        if chunk:
          totalbits += 1024
          print("Downloaded",totalbits*1025,"KB...")
          f.write(chunk)
      f.close()
  with zipfile.ZipFile(zipLocation, 'r') as zip_ref:
    zip_ref.extractall(f'{outputPath}')
  if deleteZip:
    print("Chromedriver extracted, removing zip file")
    removeZip(zipLocation)
  else:
    print("Chromedriver Extracted")
  return(os.listdir(outputPath))

def main():
  getDriver()

if __name__ == "__main__":
  main()
