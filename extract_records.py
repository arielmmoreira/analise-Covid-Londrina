from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
import re

def set_up_driver(url):
    try:
        driver = webdriver.Chrome(r'C:\chromedriver\chromedriver.exe')
        driver.get(url)
    except:
        print("An error occurred when setting up driver")

    return driver

def get_total_records(driver):
    records_list = driver.find_elements_by_css_selector(".amcharts-chart-div circle")
    records = [record.get_attribute("aria-label") for record in records_list]

    return records


def extract_total_records():
    url = 'https://geo.londrina.pr.gov.br/portal/apps/opsdashboard/index.html#/d2d6fcd7cb5248a0bebb8c90e2a4a482'
    driver = set_up_driver(url)
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
    timeout = 30

    try:
        records = WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions).until(get_total_records)
    except:
        return
    finally:
        driver.quit()

    # Lists to store each classification
        cases = []
        healed = []
        deaths = []

        # Get records by classification
        for item in records:
            classification = re.split("[A-Z]\s", item, 1)[0]
            if classification == "CONFIRMADO":
                cases.append(item)
            elif classification == "RECUPERADO":
                healed.append(item)
            elif classification == "OBITO":
                deaths.append(item)

        return cases, healed, deaths


def extract_district_records():
    url = "https://geo.londrina.pr.gov.br/portal/apps/opsdashboard/index.html#/d2d6fcd7cb5248a0bebb8c90e2a4a482"
    driver = set_up_driver(url)
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
    timeout = 30

    try:
        records = WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions).until(get_district_records)
    except:
        return
    finally:
        driver.quit()

    return records


def get_district_records(driver):
    records = driver.find_elements_by_xpath("//*[@id='ember160']/margin-container/full-container")
    records_list = records[0].text.split("\n")
    records_list.pop(0)

    return records_list
