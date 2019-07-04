# skag-generator
A python tool for generating Single Keyword Ad Groups (SKAGs) templates for Google Ads. SKAGs are a popular way to structure Google Ads for granular detail and analysis of various keyword and ad copy combinations, however it can be time consuming to setup.

This tool uses a simple excel template input that once populated and the script has run, produces the various combinations of ad groups, keywords and ads that can then be bulk uploaded into Google Ads Editor.

## Getting Started

These instructions will get the project set up on your local machine for running the tool.

### Prerequisites

1. Python (version 3+) installed
2. pip package installer installed (usually installed with python versions later than 2.7.9 or 3.4)
3. (optional) virtualenv package installed 
```
pip install virtualenv
```
### Setup

#### Environment Setup

I have provided a requirements.txt file that can be run to automatically install all necessary packages for the SKAG tool.
Navigate to the directory where this repository is stored (the root of the folder /skag-generator) and type:
```
pip install -r requirements.txt
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

#### Excel File

The 'input_file' contains a pre-populated setup for an ad campaign for footwear. I'll be referring to this example going forward through the step by step

1. Input campaign name
2. Choose what keyword match types you want - input 'Yes' or 'No':
    - Exact - [red shoes for sale]
    - Phrase - "red shoes for sale"
    - Broad Match Modifier - +red +shoes +for +sale
3. Row 10 onwards are for keyword combinations and ad copy
4. The script will combine and create all possible combinations of the keywords included e.g.
```
red trainers deal
black desert boots for sale
green shoes accessories
```
5. The ad copy rows will create multiple variations of ads, but unlike keywords, will not mix and match to create various combinations. That function is built in to Google's 'Responsive Search Ads' and therefore does not require dynamic creation in thie script. These ads are specifically for 'Expanded Text Ads'
    1. Input ad text
    2. Placeholders can be used to substitute in keywords into ads using 'kw1', 'kw2' etc.
    3. The spreadsheet automatically calculates and alerts the user (Row 8) if their combination of ad copy and keywords will be over ad character limits
```
Example output:
kw2 in every colour => shoes in every colour
kw2 kw3 - boots for sale
kw1 kw2 for sale => brown desert boots for sale
```
6. Enter final URL - can use dynamic keyword placeholders if necessary
7. Save input_file and run Python script

## Other Information

### Further Notes

Please don't hesitate to provide feedback, feature improvements and bugs on this repository.

### To Do

- Include template for Responsive Search Ads
- Lock down Excel Spreadsheet 
- Code structure - separate out classes into separate modules

