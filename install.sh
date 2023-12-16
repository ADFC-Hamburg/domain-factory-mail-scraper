#!/bin/sh
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
python -m venv ./myvenv
./myvenv/bin/pip3 install selenium webdriver-manage lxml pyyaml
