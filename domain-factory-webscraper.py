#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.remote.webdriver import WebDriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import yaml
from pathlib import Path
import sys
import json

OK_CHAR = u'\u2713'
MINUS_CHAR = '\u2014'


def login(driver: WebDriver, username: str, password: str):
    driver.get("https://admin.df.eu")
    sleep(1)
    aktion = driver.find_element(By.LINK_TEXT, 'Kundenmenü')
    aktion.click()
    sleep(1)
    username_field = driver.find_element(By.XPATH, '//*[@id="1"]')
    username_field.send_keys(username)
    password_field = driver.find_element(By.XPATH, '//*[@id="2"]')
    password_field.send_keys(password)

    login_button = driver.find_element(
        By.XPATH, '//*[@id="root"]/div[2]/div/div[1]/main/div/div/div/div/div/div[1]/form/span/button')
    login_button.click()


def analyse_email_mainpage(driver: WebDriver):
    email_link = driver.find_element(By.LINK_TEXT, 'E-Mail-Adressen')
    email_link.click()
    sleep(2)
    # with open('email_php.html', 'w') as f:
    #    f.write(driver.page_source)

    table = driver.find_element(By.XPATH, '//*[@id="accountTable"]')
    rows = table.find_elements(By.CLASS_NAME, 'fancy_row')
    user = []
    for row in rows:
        addr = row.find_element(
            By.XPATH, './td[1]/table/tbody/tr/td[2]').get_attribute('innerHTML').strip()
        alt_addr = None
        if addr.startswith('<span'):
            addr = row.find_element(
                By.XPATH, './td[1]/table/tbody/tr/td[2]/span').get_attribute('data-title').strip()
        if '<small>' in addr:
            alt_addr = addr.split('<small>')[1].replace('</small>', '')
            addr = addr.split('<br>')[0]
        size_str = row.find_element(
            By.XPATH, './td[11]').get_attribute('innerHTML').strip().replace(' MB', '')
        if size_str == '' or size_str == MINUS_CHAR:
            mb_size = None
        else:
            mb_size = int(size_str)
        autoresponder = (row.find_element(
            By.XPATH, './td[2]/img').get_attribute('alt') == OK_CHAR)
        forwarder = (row.find_element(
            By.XPATH, './td[6]/img').get_attribute('alt') == OK_CHAR)
        destinations = []
        if (forwarder):
            row12 = row.find_element(
                By.XPATH, './td[12]').get_attribute('innerHTML').strip()

            if row12.startswith('<span'):
                dest_txt = row.find_element(
                    By.XPATH, './td[12]/span').get_attribute('data-title').split('<br>')
                for mydest in dest_txt[1:]:
                    if (mydest.strip() != ''):
                        destinations.append(mydest.strip())
            else:
                destinations.append(row12)
        user.append({
            'email': addr,
            'alt_email': alt_addr,
            'autoresponder': autoresponder,
            'mailfilter': (row.find_element(By.XPATH, './td[5]/img').get_attribute('alt') == OK_CHAR),
            'forwarder': forwarder,
            'mailbox': (row.find_element(By.XPATH, './td[7]/img').get_attribute('alt') == OK_CHAR),
            'size_in_mb': mb_size,
            'url': row.find_element(By.XPATH, './td[13]/table/tbody/tr/td/a[1]').get_attribute('href'),
            'fwd_destinations': destinations
        })
    return user


def reset_password(driver: WebDriver, url, new_password: str):
    driver.get(url)
    #with open('reset_pw.html', 'w') as f:
    #    f.write(driver.page_source)
    sleep(1)
    checkbox = driver.find_element(By.ID, 'checkboxKeepOldPassword')
    checkbox.click()
    driver.find_element(By.ID, 'newPassword1hidden').send_keys(new_password)
    driver.find_element(By.ID, 'newPassword2hidden').send_keys(new_password)
    driver.find_element(
        By.XPATH, '/html/body/section/article/section/div[11]/form/table/tbody/tr/td[1]/button').click()
    sleep(1)


def main():
    conf = yaml.safe_load(Path('config.yml').read_text())
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    login(driver, conf['username'], conf['password'])
    sleep(5)
    mail_users = analyse_email_mainpage(driver)
    with open('email.json', 'w') as f:
        f.write(json.dumps(mail_users, indent=2))
    for mail_user in mail_users:
        if mail_user['email'] == 'FIXME' and mail_user['mailbox']:
            reset_password(driver, mail_user['url'], conf['new_password'])
    driver.quit()
    # Login ist möglich unter https://admin.df.eu/kunde/index.php?into=appsuite


main()
