import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('covid.db')
        self.cursor = self.connection.cursor()

    def insert(self, table, values):
        if table == "registro":
            self.__insert_total_records(values)

        elif table == "bairro":
            self.__insert_district_records(values)

        else:
            print("Table doesn't exist")

    def create(self, table):
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"SELECT count(name) FROM sqlite_master WHERE type='table' AND name='{table}';")

        table_exists = bool(self.cursor.fetchone()[0])
        if table_exists:
            self.cursor.execute(f"DROP TABLE '{table}'")

        query = ""

        if table == "registro":
            query = '''
                CREATE TABLE IF NOT EXISTS "registro" (
                    "registro_id"	INTEGER NOT NULL,
                    "registro_data"	TEXT NOT NULL,
                    "registro_dia" TEXT NOT NULL,
                    "registro_casos_confirmados"	INTEGER NOT NULL,
                    "registro_novos_casos"	INTEGER NOT NULL,
                    "registro_recuperados"	INTEGER NOT NULL,
                    "registro_novos_recuperados"	INTEGER NOT NULL,
                    "registro_obitos"	INTEGER NOT NULL,
                    "registro_novos_obitos"	INTEGER NOT NULL,
                    "registro_sintomas"	INTEGER NOT NULL,
                    PRIMARY KEY("registro_id" AUTOINCREMENT)
                );'''

        elif table == "bairro":
            query = '''
                CREATE TABLE IF NOT EXISTS "bairro" (
                    "bairro_id"	INTEGER NOT NULL,
                    "bairro_nome"	TEXT NOT NULL,
                    "bairro_casos"	INTEGER NOT NULL,
                    PRIMARY KEY("bairro_id" AUTOINCREMENT)
                );'''

        self.cursor.execute(query)

    def __insert_district_records(self, values):
        query = '''
                    INSERT INTO "bairro" (
                        "bairro_id",
                        "bairro_nome",
                        "bairro_casos"
                        ) 
                        VALUES (?, ?, ?);
                '''
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            print("An error occurred when inserting into table <bairro>:", e)

    def __insert_total_records(self, values):
        query = '''
                    INSERT INTO "registro" (
                        "registro_id",
                        "registro_data",
                        "registro_dia",
                        "registro_casos_confirmados",
                        "registro_novos_casos",
                        "registro_recuperados",
                        "registro_novos_recuperados",
                        "registro_obitos",
                        "registro_novos_obitos",
                        "registro_sintomas"
                        ) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                '''

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
        except sqlite3.OperationalError as err1:
            print("An error occurred when inserting into table <registro>:", err1)
        except sqlite3.IntegrityError as err2:
            print("Unique constraint failed:", err2)

    def update(self, table, field, value, filter_field, filter_value):
        query = f'''
                    update {table} set {field} = {value} where {filter_field} = '{filter_value}'
                '''

        try:
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            print(f"An error occurred when updating table <{table}>.", e)

    def read(self, table):
        query = f'''
                    SELECT * FROM {table}
                '''

        try:
            self.cursor.execute(query)
            self.connection.commit()
        except sqlite3.OperationalError as e:
            print(f"An error occurred when reading from table <{table}>.", e)

        return self.cursor.fetchall()

    def delete(self):
        pass
