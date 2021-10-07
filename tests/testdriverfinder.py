import unittest, os
from chromedriverversion import getDriver

class testSum(unittest.TestCase):
  def test_getosinfo(self):
    chromeVersion, osType = getDriver.getOSInfo()
    assert type(chromeVersion) is str
    assert type(osType) is str
    assert len(chromeVersion) > 4
    assert len(osType) > 3

  def test_createdir(self):
    self.assertTrue(getDriver.verifyDirectoryExists(os.getcwd()))

  def test_deletefile(self):
    with open('./test.zip', 'wb') as tf:
      self.assertFalse(getDriver.removeZip('./test.zip'))

  def test_getDriver(self):
    dirList = getDriver.getDriver()
    print(dirList)
    self.assertTrue(('chromedriver' in dirList or 'chromedrive.exe' in dirList) and ('chromedriver.zip' not in dirList))
    dirList = getDriver.getDriver(deleteZip=False)
    print(dirList)
    self.assertTrue(('chromedriver' in dirList or 'chromedrive.exe' in dirList) and ('chromedriver.zip' in dirList))

if __name__ == '__main__':
  unittest.main()