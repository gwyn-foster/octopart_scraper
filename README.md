# octopart_scraper


## data_extraction.py
Used to populate the inventory using Digikey and Mouser product barcodes.

Download chrome driver from here: http://chromedriver.chromium.org/downloads, make sure you choose the version of chromedriver that matches your version of chrome. 
Move chromedriver to your path variable
Make sure python is installed.
Install selenium webdriver
```
	pip install selenium
```

Scan all of the barcodes, one per line, into barcodes.rtf.
From your terminal:
```
	cd BarcodeScanning
	python data_extraction.py
```
The program will run and populate inventory_data.csv.
Remember that inventory_data.csv writes over itself each time the program is run, it is recommended that you import the data to a program like google sheets or excel.
