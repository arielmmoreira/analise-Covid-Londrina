from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
import re, csv, datetime

def main():
    # Set parameters to get url
    url = 'https://geo.londrina.pr.gov.br/portal/apps/opsdashboard/index.html#/d2d6fcd7cb5248a0bebb8c90e2a4a482'
    driver = webdriver.Chrome(r'C:\chromedriver\chromedriver.exe')
    driver.get(url)

    # Set parameters to get records
    ignored_exceptions = (NoSuchElementException, StaleElementReferenceException)
    timeout = 30
    records = WebDriverWait(driver, timeout, ignored_exceptions=ignored_exceptions).until(extract_records)

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

    write_csv(cases, healed, deaths)


def extract_records(driver):
    records_list = driver.find_elements_by_css_selector(".amcharts-chart-div circle")
    records = [record.get_attribute("aria-label") for record in records_list]
    return records


def write_csv(cases, healed, deaths):
    with open("../total_records.csv", 'w', newline="") as csv_file:
        header = ["id", "data", "casos confirmados", "novos casos",
                  "recuperados", "novos recuperados", "obitos", "novos obitos",
                  "dia da semana", "media movel confirmados", "media movel obitos"]
        writer = csv.writer(csv_file)
        writer.writerow(header)

        # Set variables to store records of 'yesterday'
        cases_last_day = 0
        healed_last_day = 0
        deaths_last_day = 0

        # Set variables to store moving average
        cases_last_seven_days = []
        moving_avg_cases = 0

        deaths_last_seven_days = []
        moving_avg_deaths = 0

        total_records = len(cases)
        for i in range(total_records):
            # Get date of records
            month = re.search("\s[a-zA-Z]{3}", cases[i]).group().strip(" ").lower()
            day = re.search("\s[0-9]{2}", cases[i]).group().strip(" ")
            year = re.search("\s[0-9]{4}\s", cases[i]).group().strip(" ")
            date = f"{day}-{month}-{year}"
            weekday = get_weekday(day, month, year)

            # Get today's cases. That's the accumulated cases from url data
            total_cases = cases[i][cases[i].find(year) + 5:]
            total_cases = int(re.sub(",", "", total_cases))

            total_healed = healed[i][healed[i].find(year) + 5:]
            total_healed = int(re.sub(",", "", total_healed))

            total_deaths = deaths[i][deaths[i].find(year) + 5:]
            total_deaths = int(re.sub(",", "", total_deaths))

            # Compute daily cases
            daily_cases = 0
            if total_cases > cases_last_day:
                daily_cases = total_cases - cases_last_day
                cases_last_day = total_cases

            # Compute moving average in a period of seven days
            period = 7
            cases_last_seven_days.append(daily_cases)
            if len(cases_last_seven_days) == period:
                moving_avg_cases = round(sum(cases_last_seven_days) / period, 2)
                cases_last_seven_days.pop(0)

            # Compute daily healed
            daily_healed = 0
            if total_healed > healed_last_day:
                daily_healed = total_healed - healed_last_day
                healed_last_day = total_healed

            # Compute daily deaths
            daily_deaths = 0
            if total_deaths > deaths_last_day:
                daily_deaths = total_deaths - deaths_last_day
                deaths_last_day = total_deaths

            # Compute moving average in a period of seven days
            deaths_last_seven_days.append(daily_deaths)
            if len(deaths_last_seven_days) == period:
                moving_avg_deaths = round(sum(deaths_last_seven_days) / period, 2)
                deaths_last_seven_days.pop(0)

            record_id = i + 1
            row = [record_id, date, total_cases, daily_cases,
                   total_healed, daily_healed, total_deaths,
                   daily_deaths, weekday, moving_avg_cases,
                   moving_avg_deaths]

            writer.writerow(row)

            moving_avg_cases = 0
            moving_avg_deaths = 0


def get_weekday(day, month, year):
    months = {"jan": "jan", "fev": "feb", "mar": "mar", "abr": "apr", "mai": "may", "jun": "jun",
              "jul": "jul", "ago": "aug", "set": "sep", "out": "oct", "nov": "nov", "dez": "dec"}
    weekday = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
               "sexta-feira", "sabado", "domingo"]

    month = months[month]
    date = str(day) + " " + month + " " + str(year)
    day = datetime.datetime.strptime(date, "%d %b %Y").weekday()
    return weekday[day]


main()
