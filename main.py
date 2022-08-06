from extract_records import *
from Database import *
import datetime


def main():

    db = Database()

    total_records, district_records, symptoms_records = extract_data()
    cases, healed, deaths = total_records

    insert_total_records(db, cases, healed, deaths)
    insert_district_records(db, district_records)
    insert_symptoms_records(db, symptoms_records)


def insert_symptoms_records(db, symptoms_records):

    for i in range(len(symptoms_records)):
        month = re.search(r"\s[a-zA-Z]{3}", symptoms_records[i]).group().strip(" ").lower()
        day = re.search(r"\s[0-9]{2},", symptoms_records[i]).group().lstrip(" ").rstrip(",")
        year = re.search(r",\s[0-9]{4}\s", symptoms_records[i]).group().lstrip(", ").rstrip(" ")
        symptoms_number = int(symptoms_records[i][symptoms_records[i].find(year) + 5:].replace(",", ""))
        date = f'{day}-{month}-{year}'

        field = "registro_sintomas"
        value = symptoms_number
        filter_field = "registro_data"
        filter_value = date

        db.update("registro", field, value, filter_field, filter_value)


def insert_district_records(db, district_records):
    table = "bairro"
    db.create(table)

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
    db.create(table)

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
