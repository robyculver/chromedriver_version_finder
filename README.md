# chromedriverversion

Python module for capturing and the needed version of chromedriver to run selenium tests on your system.

This has been tested against multiple Windows and MacOS installations of Chrome.  Also an older version of ubuntu.  But the Linux compatibility likely needs work.


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install chromedriverversion.

```bash
pip install chromedriverversion
```

## Usage

By Default chromedriver version downloads and extracts chrome driver in the directory where it's being run
```python
from chromedriverversion import getDriver
getDriver.getDriver()
```
Optionally you can specify a path where to download chromedriver, if the Path doesn't exist it will create it for you
```python
getDriver.getDriver('~/chromedriver')

getDriver.getDriver('C:\Windows\Users\Administrator\Documents')
```
By Default the chromedriver.zip is deleted, however you can choose not to delete the file:
```python
from chromedriverversion import getDriver

getDriver.getDriver(deleteZip=False)
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html)