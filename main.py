from extract_records import *
from Database import *
import datetime


def main():
    db = Database()

    cases, healed, deaths = extract_total_records()
    insert_total_records(db, cases, healed, deaths)

    district_records = extract_district_records()
    insert_district_records(db, district_records)

def insert_district_records(db, district_records):
    table = "bairro"
    records_by_district = {}

    record_id = 0
    for record in district_records:
        record_id += 1
        district = re.search("\w+.*-", record).group().rstrip(" -")
        cases_number = int(re.search("-\s.*\s", record).group().lstrip("- ").rstrip(" Casos").replace(".", ""))
        records_by_district[district] = cases_number
        values = [record_id, district, cases_number]
        db.insert(table, values)


def insert_total_records(db, cases, healed, deaths):
    table = "registro"

    cases_last_day = 0
    healed_last_day = 0
    deaths_last_day = 0
    total_records = len(cases)

    for i in range(total_records):
        month = re.search(r"\s[a-zA-Z]{3}", cases[i]).group().strip(" ").lower()
        day = re.search(r"\s[0-9]{2}", cases[i]).group().strip(" ")
        year = re.search(r"\s[0-9]{4}\s", cases[i]).group().strip(" ")
        date = f"{day}-{month}-{year}"
        weekday = get_weekday(day, month, year)

        total_cases = cases[i][cases[i].find(year) + 5:]
        total_cases = int(re.sub(",", "", total_cases))

        total_healed = healed[i][healed[i].find(year) + 5:]
        total_healed = int(re.sub(",", "", total_healed))

        total_deaths = deaths[i][deaths[i].find(year) + 5:]
        total_deaths = int(re.sub(",", "", total_deaths))

        daily_cases = 0
        if total_cases > cases_last_day:
            daily_cases = total_cases - cases_last_day
            cases_last_day = total_cases

        daily_healed = 0
        if total_healed > healed_last_day:
            daily_healed = total_healed - healed_last_day
            healed_last_day = total_healed

        daily_deaths = 0
        if total_deaths > deaths_last_day:
            daily_deaths = total_deaths - deaths_last_day
            deaths_last_day = total_deaths

        record_id = i + 1
        values = [record_id, date, weekday, total_cases, daily_cases, total_healed,
                  daily_healed, total_deaths, daily_deaths, 0]
        db.insert(table, values)


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

#
# for record in records_list:
#     district = re.search("\w+.*-", record).group().rstrip(" -")
#     cases_number = int(re.search("-\s.*\s", record).group().lstrip("- ").rstrip(" Casos").replace(".", ""))
#     records_by_district[district] = cases_number
#
#
# print(records_by_district)


