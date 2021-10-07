import platform
import subprocess
import glob
import re
import packaging
from packaging import version
import requests

##simple script to test capturing version info from multi OS types and versions

#capture platform information
osPlatform = (platform.platform())

#mac version capture
if 'macos' in osPlatform.lower():
  print(osPlatform)
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
  print(f"Chrome Version = {chromeVersion}")
  driverType = 'win32'
#linux version capture
elif 'linux' in osPlatform.lower():
  print(osPlatform)
  osType = 'linux'
  chromeVersion = subprocess.run(["google-chrome", "--version"])
  print(f"Chrome Version = {chromeVersion}")
  driverType = 'linux64'
#get first octet of version to get complete version needed for chrome driver
majorVersion = chromeVersion.split('.')[0]
chromeDriverVersion = requests.get(f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{majorVersion}").text
chromeDriverFile = f'chromedriver_{driverType}.zip'
#print chrome driver version and url where to download
print(f"Chrome Driver Version = {chromeDriverVersion}")
print(f"Download location is: https://chromedriver.storage.googleapis.com/{chromeDriverVersion}/{chromeDriverFile}")
