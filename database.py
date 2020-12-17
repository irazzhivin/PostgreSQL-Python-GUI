import json

import psycopg2


class SettingNotFoundException(Exception):
    pass


class car:
    def __init__(self, car_id: int, name: str, year: int, factory_id: int):
        self.id = car_id
        self.name = name
        self.year = year
        self.factory_id = factory_id


class factory:
    def __init__(self, factory_id: int, name: str, foundation_date: str, address: str, car_number: int = 0):
        self.id = factory_id
        self.name = name
        self.foundation_date = foundation_date
        self.address = address
        self.car_number = car_number


class carDatabase:
    def __init__(self, settings_filename: str):
        with open(settings_filename, 'r') as file:
            settings = json.load(file)
            if not settings.get('postgres', ''):
                raise SettingNotFoundException('No main fields in settings')
            postgres_settings = settings['postgres']
            if not postgres_settings.get('user', ''):
                raise SettingNotFoundException('No login in settings')
            if not postgres_settings.get('password', ''):
                raise SettingNotFoundException('No pass in settings')
            if not postgres_settings.get('host', ''):
                raise SettingNotFoundException('No host in settings')
            if not postgres_settings.get('port', ''):
                raise SettingNotFoundException('No port in settings')
            if not postgres_settings.get('db_name', ''):
                raise SettingNotFoundException('No db name in settings')
            self.postgres_settings = postgres_settings
            self.user = postgres_settings['user']
            self.password = postgres_settings['password']
            self.host = postgres_settings['host']
            self.port = postgres_settings['port']
            self.db_name = postgres_settings['db_name']
            self.open_connections = {}
            self.make_connection('postgres')
            self.current_db = ''

    def make_connection(self, db_name):
        con = psycopg2.connect(
            database=db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port)
        self.open_connections[db_name] = con

    def create_db(self, db_name):
        with self.open_connections['postgres'] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT create_db('{db_name}', '{self.user}', '{self.password}');")
        self.make_connection(db_name)
        self.read_functions(db_name)
        self._create_tables(db_name)
        con.commit()

    def read_functions(self, db_name):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(open("functions.sql", "r").read())
            con.commit()

    def drop_db(self, db_name):
        with self.open_connections['postgres'] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT drop_db('{db_name}', '{self.user}', '{self.password}');")
            con.commit()

    def _create_tables(self, db_name):
        with self.open_connections[db_name] as con:
            with self.open_connections[db_name].cursor() as cur:
                cur.execute(f"SELECT create_tables('{db_name}', '{self.user}', '{self.password}');")
            con.commit()

    def select_all_cars(self, db_name):
        with self.open_connections[db_name].cursor() as cur:
            cur.execute(f"SELECT * FROM get_cars();")
            records = cur.fetchall()
            return records

    def select_all_factorys(self, db_name):
        with self.open_connections[db_name].cursor() as cur:
            cur.execute(f"SELECT * FROM get_factorys();")
            records = cur.fetchall()
            return records

    def find_cars(self, db_name, name):
        with self.open_connections[db_name].cursor() as cur:
            cur.execute(f"SELECT * FROM find_cars('{name}');")
            records = cur.fetchall()
            return records

    def find_factorys(self, db_name, name):
        with self.open_connections[db_name].cursor() as cur:
            cur.execute(f"SELECT * FROM find_factorys('{name}');")
            records = cur.fetchall()
            return records

    def insert_car(self, db_name: str, car: car):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT insert_car('{car.id}', '{car.name}', '{car.year}', '{car.factory_id}');")
            con.commit()

    def insert_factory(self, db_name: str, factory: factory):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT insert_factory(CAST('{factory.id}' AS INTEGER), CAST('{factory.name}' AS TEXT), "
                            f"CAST('{factory.foundation_date}' AS date), CAST('{factory.address}' AS TEXT), CAST('{factory.car_number}' AS INTEGER));")
            con.commit()

    def delete_all_cars(self, db_name: str):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT delete_all_cars();")
            con.commit()

    def delete_all_factorys(self, db_name: str):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT delete_all_factorys();")
            con.commit()

    def delete_factorys_by_name(self, db_name: str, name: str):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT delete_factorys_by_name('{name}');")
            con.commit()

    def delete_cars_by_name(self, db_name: str, name: str):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT delete_cars_by_name('{name}');")
            con.commit()

    def delete_factory_by_id(self, db_name: str, factory_id: int):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT delete_factory('{factory_id}');")
            con.commit()

    def delete_car_by_id(self, db_name: str, car_id: int):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT delete_car('{car_id}');")
            con.commit()

    def update_car(self, db_name: str, car: car):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT update_car('{car.id}', '{car.name}', '{car.year}', '{car.factory_id}');")
            con.commit()

    def update_factory(self, db_name: str, factory: factory):
        with self.open_connections[db_name] as con:
            with con.cursor() as cur:
                cur.execute(f"SELECT update_factory('{factory.id}', '{factory.name}', '{factory.foundation_date}', "
                            f"'{factory.address}', '{factory.car_number}');")
            con.commit()
