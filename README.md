# skag-generator
A python tool for generating Single Keyword Ad Groups (SKAGs) templates for Google Ads. SKAGs are a popular way to structure Google Ads for granular detail and analysis of various keyword and ad copy combinations, however it can be time consuming to setup.

This tool uses a simple excel template input that once populated and the script has run, produces the various combinations of ad groups, keywords and ads that can then be bulk uploaded into Google Ads Editor.

## Getting Started

These instructions will get the project set up on your local machine for running the tool.

### Prerequisites

1) Python (version 3+) installed
2) pip package installer installed (usually installed with python versions later than 2.7.9 or 3.4)
3) (optional) virtualenv package installed 
```
pip install virtualenv
```
### Setup

#### Environment Setup

I have provided a requirements.txt file that can be run to automatically install all necessary packages for the SKAG tool.
Navigate to the directory where this repository is stored (the root of the folder /skag-generator) and type:
```
install -r requirements.txt
```
Once installed, you can enter 'pip list' into the command prompt and should see something similar to below:
```
Package         Version
--------------- -------
DateTime        4.3
numpy           1.16.4
pandas          0.24.2
pip             19.1.1
python-dateutil 2.8.0
pytz            2019.1
setuptools      41.0.1
six             1.12.0
wheel           0.33.4
xlrd            1.2.0
XlsxWriter      1.1.8
zope.interface  4.6.0
```

#### Running Script

In the root of the repository you can now type:
```
python generate-ads.py
```

If everything goes ok you will see:
```
skag csv created successfully
skag excel created successfully
```

The 'output' folder should now contain the relevant SKAG files in a format ready to be uploaded to Google Ads Editor

To be continued...
