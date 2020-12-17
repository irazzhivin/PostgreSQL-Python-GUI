from tkinter import *
from tkinter import messagebox
from database import carDatabase, car, factory


import datetime


NUMBER_OF_FIELDS = 4
SEARCH_BY_NAME = 0
SEARCH_BY_YEAR = 1
SEARCH_BY_RATE = 2
SEARCH_BY_ID = 3

CRED_FILENAME = 'credentials.json'
R_GEOMETRY = '800x600+450+80'
TITLE = 'Cars and Factories db'
USED_DBs = 'databases.list'
ROW_FORMAT_car = "{:>25}" * 4
ROW_FORMAT_factory = "{:>20}" * 5


def add_menu(root, car_listbox, factory_listbox, db):
    main_menu = Menu()

    file_menu = Menu()
    file_menu.add_command(label='create database', command=lambda: create_db(db))
    file_menu.add_command(label='delete database', command=lambda: drop_db(db))
    file_menu.add_command(label='open database', command=lambda: open_db(car_listbox, factory_listbox, db))

    clear_menu = Menu()
    clear_menu.add_command(label='Delete everything from current db',
                           command=lambda: clear_all(db, car_listbox, factory_listbox))
    clear_menu.add_command(label='Delete all cars from current db',
                           command=lambda: clear_cars(db, car_listbox, factory_listbox))
    clear_menu.add_command(label='Delete all factorys from current db',
                           command=lambda: clear_factorys(db, factory_listbox))

    main_menu.add_cascade(label="File", menu=file_menu)
    main_menu.add_cascade(label="Clear", menu=clear_menu)

    root.config(menu=main_menu)


def clear_all(db, car_listbox, factory_listbox):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    db.delete_all_cars(db.current_db)
    db.delete_all_factorys(db.current_db)
    db.delete_all_factorys(db.current_db)
    show_all_cars(db, car_listbox)
    show_all_factorys(db, factory_listbox)


def clear_cars(db, car_listbox, factory_listbox):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    db.delete_all_cars(db.current_db)
    show_all_cars(db, car_listbox)
    show_all_factorys(db, factory_listbox)


def clear_factorys(db, factory_listbox):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    db.delete_all_factorys(db.current_db)
    show_all_factorys(db, factory_listbox)


def _open(car_listbox, factory_listbox, chosen_db, listbox, choose_window, db):
    chosen = listbox.curselection()
    if chosen:
        chosen_db += [listbox.get(chosen)]
        db_name = chosen_db[0]
        db.make_connection(db_name)
        db.current_db = db_name
        show_all_cars(db, car_listbox)
        show_all_factorys(db, factory_listbox)
    choose_window.destroy()


def show_all_cars(db, car_listbox):
    if db.current_db:
        cars = db.select_all_cars(db.current_db)
        car_listbox.delete(0, 'end')
        for i, car in enumerate(cars):
            car_listbox.insert(i, ROW_FORMAT_car.format(*car))


def show_all_factorys(db, factory_listbox):
    if db.current_db:
        factorys = db.select_all_factorys(db.current_db)
        factory_listbox.delete(0, 'end')
        for i, factory in enumerate(factorys):
            factory_listbox.insert(i, ROW_FORMAT_factory.format(*[str(field) for field in factory]))


def open_db(car_listbox, factory_listbox, db):
    active_dbs = []
    with open(USED_DBs, 'r') as file:
        active_dbs += [line.replace('\n', '') for line in file.read().splitlines()]
    if active_dbs:
        choose_window = Toplevel()
        choose_window.geometry('400x160+850+440')
        choose_window.title('Existing databases')

        chosen_db = []
        scrollbar = Scrollbar(choose_window)
        scrollbar.place(relheight=0.8, relwidth=0.01, relx=0.96, rely=0.11)
        listbox = Listbox(choose_window, yscrollcommand=scrollbar.set)
        for i, active_db in enumerate(active_dbs):
            listbox.insert(i, active_db)
        listbox.place(relheight=0.8, relwidth=0.96, rely=0.11)
        btn_open_db = Button(choose_window, text='open',
                             command=lambda: _open(car_listbox, factory_listbox, chosen_db, listbox, choose_window,
                                                   db))
        btn_open_db.place(relheight=0.14, relwidth=0.29, relx=0.35, rely=0.75)
    else:
        messagebox.showinfo("Warning", "No databases created")


def create_db(db):
    choose_window = Toplevel()
    choose_window.geometry('400x160+850+440')
    choose_window.title('Enter name of the database')

    user_db_name = StringVar()
    label = Label(choose_window, text='Enter filename:', font=15)
    label.place(relheight=0.3, relwidth=0.7, relx=0.11)
    entry = Entry(choose_window, textvariable=user_db_name, font=15)
    entry.place(relheight=0.2, relwidth=0.7, relx=0.11, rely=0.3)
    btn_create_db = Button(choose_window, text='create', command=lambda: _create(db, user_db_name, choose_window))
    btn_create_db.place(relheight=0.15, relwidth=0.3, relx=0.33, rely=0.75)


def _create(db, user_db_name, choose_window):
    db_name = user_db_name.get()
    if db_name:
        db.create_db(db_name)
        active_dbs = set()
        with open(USED_DBs, 'r') as file:
            for line in file:
                active_dbs.add(line.replace('\n', ''))
        active_dbs.add(db_name)
        with open(USED_DBs, 'w') as file:
            file.write('\n'.join(active_dbs))
        choose_window.destroy()
    else:
        messagebox.showerror("Error", "Database name cannot be empty")


def _drop(chosen_db, listbox, choose_window, db):
    chosen = listbox.curselection()
    if chosen:
        chosen_db += [listbox.get(chosen)]
        db_name = chosen_db[0]
        db.drop_db(db_name)
        active_dbs = set()
        with open(USED_DBs, 'r') as file:
            for line in file:
                active_dbs.add(line.replace('\n', ''))
        active_dbs.remove(db_name)
        with open(USED_DBs, 'w') as file:
            file.write('\n'.join(active_dbs))
    choose_window.destroy()


def drop_db(db):
    active_dbs = []
    with open(USED_DBs, 'r') as file:
        active_dbs += [line.replace('\n', '') for line in file.read().splitlines()]
    if active_dbs:
        choose_window = Toplevel()
        choose_window.geometry('400x160+850+440')
        choose_window.title('Existing databases')

        chosen_db = []
        scrollbar = Scrollbar(choose_window)
        scrollbar.place(relheight=0.9, relwidth=0.02, relx=0.98, rely=0.1)
        listbox = Listbox(choose_window, yscrollcommand=scrollbar.set)
        for i, active_db in enumerate(active_dbs):
            listbox.insert(i, active_db)
        listbox.place(relheight=0.9, relwidth=0.98, rely=0.1)
        btn_open_db = Button(choose_window, text='delete', command=lambda: _drop(chosen_db, listbox, choose_window, db))
        btn_open_db.place(relheight=0.15, relwidth=0.3, relx=0.35, rely=0.85)
    else:
        messagebox.showinfo("Warning", "No databases created")


def add_car(db, factory_listbox, car_listbox):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    choose_window = Toplevel()
    choose_window.geometry('400x160+850+440')
    choose_window.title('car to add')
    user_car_id = StringVar()
    user_car_name = StringVar()
    user_car_year = StringVar()
    user_car_factory_id = StringVar()

    label = Label(choose_window, text='Enter car id:', font=12)
    label.place(relheight=0.25, relwidth=0.15)
    entry = Entry(choose_window, textvariable=user_car_id, font=12)
    entry.place(relheight=0.25, relwidth=0.15, rely=0.3)

    label = Label(choose_window, text='Enter car name:', font=12)
    label.place(relheight=0.25, relwidth=0.45, relx=0.15)
    entry = Entry(choose_window, textvariable=user_car_title, font=12)
    entry.place(relheight=0.25, relwidth=0.45, relx=0.15, rely=0.3)

    label = Label(choose_window, text='Enter car year:', font=12)
    label.place(relheight=0.25, relwidth=0.2, relx=0.6)
    entry = Entry(choose_window, textvariable=user_car_year, font=12)
    entry.place(relheight=0.25, relwidth=0.2, relx=0.6, rely=0.3)

    label = Label(choose_window, text='Enter factory id:', font=12)
    label.place(relheight=0.25, relwidth=0.2, relx=0.8)
    entry = Entry(choose_window, textvariable=user_car_factory_id, font=12)
    entry.place(relheight=0.25, relwidth=0.2, relx=0.8, rely=0.3)

    btn_add = Button(choose_window, text='add',
                     command=lambda: _add_car(db, user_car_id, user_car_name, user_car_year, user_car_factory_id,
                                               choose_window, factory_listbox, car_listbox))
    btn_add.place(relheight=0.2, relwidth=0.15, relx=0.4, rely=0.7)


def _add_car(db, user_car_id, user_car_name, user_car_year,
              user_car_factory_id, choose_window, factory_listbox, car_listbox):
    if db.current_db:
        car_id = user_car_id.get()
        car_name = user_car_name.get()
        car_year = user_car_year.get()
        car_p_id = user_car_factory_id.get()
        car_factory_id = user_car_factory_id.get()
        if car_id and car_name and car_year and car_factory_id:
            errors_in_data = check_car_data(car_id, car_year, car_p_id)
            if errors_in_data:
                messagebox.showerror("Error", errors_in_data)
                return
            db.insert_car(db.current_db, car(car_id, car_name, car_year, car_p_id))
            show_all_cars(db, car_listbox)
            show_all_factorys(db, factory_listbox)
        else:
            messagebox.showerror("Error", "Fields cannot be empty")
    else:
        messagebox.showerror("Error", "Open database before inserting")
    choose_window.destroy()


def check_car_data(car_id, car_year, car_p_id):
    error_msg = ''
    try:
        int(car_id)
    except Exception:
        error_msg += 'Incorrect car id\n'
    try:
        f_year = int(car_year)
        if len(car_year) != 4:
            error_msg += 'year should consist of 4 digits\n'
    except Exception:
        error_msg += 'Incorrect car year\n'
    try:
        int(car_p_id)
    except Exception:
        error_msg += 'Incorrect factory id'
    return error_msg


def check_factory_data(p_id, p_foundation_date):
    error_msg = ''
    try:
        int(p_id)
    except Exception:
        error_msg += 'Incorrect factory id\n'
    try:
        bd = datetime.datetime.strptime(p_foundation_date, "%Y-%m-%d")
    except Exception as e:
        error_msg += 'foundation date must be in format: yyyy-mm-dd'
    return error_msg


def add_factory(db, factory_listbox, car_listbox):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    choose_window = Toplevel()
    choose_window.geometry('400x160+850+440')
    choose_window.title('factory to add')
    user_factory_id = StringVar()
    user_factory_name = StringVar()
    user_factory_foundation_date = StringVar()
    user_factory_address = StringVar()

    label = Label(choose_window, text='Id:', font=12)
    label.place(relheight=0.25, relwidth=0.15)
    entry = Entry(choose_window, textvariable=user_factory_id, font=12)
    entry.place(relheight=0.25, relwidth=0.15, rely=0.3)

    label = Label(choose_window, text='Name:', font=12)
    label.place(relheight=0.25, relwidth=0.45, relx=0.15)
    entry = Entry(choose_window, textvariable=user_factory_name, font=12)
    entry.place(relheight=0.25, relwidth=0.45, relx=0.15, rely=0.3)

    label = Label(choose_window, text='foundation_date:', font=12)
    label.place(relheight=0.25, relwidth=0.2, relx=0.6)
    entry = Entry(choose_window, textvariable=user_factory_foundation_date, font=12)
    entry.place(relheight=0.25, relwidth=0.2, relx=0.6, rely=0.3)

    label = Label(choose_window, text='Address:', font=12)
    label.place(relheight=0.25, relwidth=0.2, relx=0.8)
    entry = Entry(choose_window, textvariable=user_factory_address, font=12)
    entry.place(relheight=0.25, relwidth=0.2, relx=0.8, rely=0.3)

    btn_add = Button(choose_window, text='add',
                     command=lambda: _add_factory(db, user_factory_id, user_factory_name,
                                                   user_factory_foundation_date, user_factory_address,
                                                   choose_window, factory_listbox, car_listbox))
    btn_add.place(relheight=0.2, relwidth=0.15, relx=0.4, rely=0.7)


def _add_factory(db, user_factory_id, user_factory_name, user_factory_foundation_date,
                  user_factory_address, choose_window, factory_listbox, car_listbox):
    if db.current_db:
        factory_id = user_factory_id.get()
        factory_name = user_factory_name.get()
        factory_bd = user_factory_foundation_date.get()
        factory_address = user_factory_address.get()
        if factory_id and factory_name and factory_bd and factory_address:
            data_errors = check_factory_data(factory_id, factory_bd)
            if data_errors:
                messagebox.showerror("Error", data_errors)
                return
            db.insert_factory(db.current_db, factory(factory_id, factory_name, factory_bd, factory_address, 0))
            show_all_factorys(db, factory_listbox)
        else:
            messagebox.showerror("Error", "Fields cannot be empty")
    else:
        messagebox.showerror("Error", "Open database before inserting")
    choose_window.destroy()


def search_car(db, car_listbox, car_name_to_find):
    if db.current_db:
        name_to_find = car_name_to_find.get()
        if name_to_find:
            cars = db.find_cars(db.current_db, name_to_find)
            car_listbox.delete(0, 'end')
            for i, car in enumerate(cars):
                car_listbox.insert(i, ROW_FORMAT_car.format(*car))
        else:
            messagebox.showinfo("Error", "Enter a name before search")
    else:
        messagebox.showerror("Error", "Open database before search")


def search_factory(db, factory_listbox, factory_name_to_find):
    if db.current_db:
        name_to_find = factory_name_to_find.get()
        if name_to_find:
            factorys = db.find_factorys(db.current_db, name_to_find)
            factory_listbox.delete(0, 'end')
            for i, factory in enumerate(factorys):
                factory_listbox.insert(i, ROW_FORMAT_car.format(*[str(field) for field in factory]))
        else:
            messagebox.showinfo("Error", "Enter a name before search")
    else:
        messagebox.showerror("Error", "Open database before search")


def _update_car(db, car_listbox, factory_listbox, car_id: int, user_car_name, user_car_year,
                 user_car_factory_id, choose_window):
    car_name = user_car_name.get()
    car_year = user_car_year.get()
    car_factory_id = user_car_factory_id.get()
    if car_id and car_name and car_year and car_factory_id:
        errors_in_data = check_car_data(car_id, car_year, car_factory_id)
        if errors_in_data:
            messagebox.showerror("Error", errors_in_data)
            return
        db.update_car(db.current_db, car(car_id, car_name, car_year, car_factory_id))
        show_all_cars(db, car_listbox)
        show_all_factorys(db, factory_listbox)
    else:
        messagebox.showerror("Error", "Fields cannot be empty")
    choose_window.destroy()


def update_car(db, car_listbox, factory_listbox):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    chosen_car = car_listbox.curselection()
    if not chosen_car:
        messagebox.showerror("Error", "No cars picked out")
        return
    choose_window = Toplevel()
    choose_window.geometry('400x160+850+440')
    choose_window.title('car to update')
    user_car_id = StringVar()
    user_car_name = StringVar()
    user_car_year = StringVar()
    user_car_factory_id = StringVar()

    chosen_car = car_listbox.get(chosen_car)
    fields = [field for field in re.split(r'\s{2,}', chosen_car) if field]
    # print(fields)
    # print(chosen_car)
    if len(fields) == 4:
        user_car_id.set(fields[0])
        user_car_name.set(fields[1])
        user_car_year.set(fields[2])
        user_car_factory_id.set(fields[3])
    else:
        return

    label = Label(choose_window, text='Id:', font=12)
    label.place(relheight=0.25, relwidth=0.15)
    label = Label(choose_window, textvariable=user_car_id, font=12)
    label.place(relheight=0.25, relwidth=0.15, rely=0.3)

    label = Label(choose_window, text='name:', font=12)
    label.place(relheight=0.25, relwidth=0.45, relx=0.15)
    entry = Entry(choose_window, textvariable=user_car_name, font=12)
    entry.place(relheight=0.25, relwidth=0.45, relx=0.15, rely=0.3)

    label = Label(choose_window, text='Year:', font=12)
    label.place(relheight=0.25, relwidth=0.2, relx=0.6)
    entry = Entry(choose_window, textvariable=user_car_year, font=12)
    entry.place(relheight=0.25, relwidth=0.2, relx=0.6, rely=0.3)

    label = Label(choose_window, text='factory id:', font=12)
    label.place(relheight=0.25, relwidth=0.2, relx=0.8)
    entry = Entry(choose_window, textvariable=user_car_factory_id, font=12)
    entry.place(relheight=0.25, relwidth=0.2, relx=0.8, rely=0.3)

    btn_add = Button(choose_window, text='Update',
                     command=lambda: _update_car(db, car_listbox, factory_listbox, user_car_id.get(),
                                                  user_car_name, user_car_year,
                                                  user_car_factory_id, choose_window))
    btn_add.place(relheight=0.2, relwidth=0.15, relx=0.4, rely=0.7)


def _update_factory(db, factory_listbox, factory_id: int, user_factory_name,
                     user_factory_foundation_date, user_factory_address, choose_window):
    factory_name = user_factory_name.get()
    factory_db = user_factory_foundation_date.get()
    factory_address = user_factory_address.get()
    if factory_id and factory_name and factory_db and factory_address:
        db.update_factory(db.current_db, factory(factory_id, factory_name, factory_db, factory_address))
        show_all_factorys(db, factory_listbox)
    else:
        messagebox.showerror("Error", "Fields cannot be empty")
    choose_window.destroy()


def update_factory(db, factory_listbox):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    chosen_factory = factory_listbox.curselection()
    if not chosen_factory:
        messagebox.showerror("Error", "No factorys picked out")
        return
    choose_window = Toplevel()
    choose_window.geometry('800x150+750+450')
    choose_window.title('car to update')
    choose_window.title('factory to add')

    user_factory_id = StringVar()
    user_factory_name = StringVar()
    user_factory_foundation_date = StringVar()
    user_factory_address = StringVar()

    chosen_factory = factory_listbox.get(chosen_factory)
    fields = [field for field in re.split(r'\s{2,}', chosen_factory) if field]

    if len(fields) != 5:
        return

    user_factory_id.set(fields[0])
    user_factory_name.set(fields[1])
    user_factory_foundation_date.set(fields[2])
    user_factory_address.set(fields[3])

    label = Label(choose_window, text='Id:', font=12)
    label.place(relheight=0.25, relwidth=0.15)
    label = Label(choose_window, textvariable=user_factory_id, font=12)
    label.place(relheight=0.25, relwidth=0.15, rely=0.3)

    label = Label(choose_window, text='Name:', font=12)
    label.place(relheight=0.25, relwidth=0.45, relx=0.15)
    entry = Entry(choose_window, textvariable=user_factory_name, font=12)
    entry.place(relheight=0.25, relwidth=0.45, relx=0.15, rely=0.3)

    label = Label(choose_window, text='foundation_date:', font=12)
    label.place(relheight=0.25, relwidth=0.2, relx=0.6)
    entry = Entry(choose_window, textvariable=user_factory_foundation_date, font=12)
    entry.place(relheight=0.25, relwidth=0.2, relx=0.6, rely=0.3)

    label = Label(choose_window, text='Address:', font=12)
    label.place(relheight=0.25, relwidth=0.2, relx=0.8)
    entry = Entry(choose_window, textvariable=user_factory_address, font=12)
    entry.place(relheight=0.25, relwidth=0.2, relx=0.8, rely=0.3)

    btn_add = Button(choose_window, text='Update',
                     command=lambda: _update_factory(db, factory_listbox, user_factory_id.get(), user_factory_name,
                                                      user_factory_foundation_date, user_factory_address, choose_window))
    btn_add.place(relheight=0.2, relwidth=0.15, relx=0.4, rely=0.7)


def drop_car(db, car_listbox, factory_listbox):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    chosen_car = car_listbox.curselection()
    if not chosen_car:
        messagebox.showerror("Error", "No cars picked out")
        return
    chosen_car = car_listbox.get(chosen_car)
    fields = [field for field in re.split(r'\s{2,}', chosen_car) if field]
    if len(fields) == 4:
        car_id = fields[0]
        db.delete_car_by_id(db.current_db, car_id)
        show_all_cars(db, car_listbox)
        show_all_factorys(db, factory_listbox)
    else:
        return


def drop_factory(db, factory_listbox):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    chosen_factory = factory_listbox.curselection()
    if not chosen_factory:
        messagebox.showerror("Error", "No factorys picked out")
        return
    chosen_factory = factory_listbox.get(chosen_factory)
    fields = [field for field in re.split(r'\s{2,}', chosen_factory) if field]
    if len(fields) == 5:
        factory_id = fields[0]
        db.delete_factory_by_id(db.current_db, factory_id)
        show_all_factorys(db, factory_listbox)
    else:
        return


def delete_cars_by_name(db, car_listbox, factory_listbox, car_name_to_find):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    name_to_find = car_name_to_find.get()
    if not name_to_find:
        return
    db.delete_cars_by_name(db.current_db, name_to_find)
    show_all_cars(db, car_listbox)
    show_all_factorys(db, factory_listbox)


def delete_factorys_by_name(db, factory_listbox, factory_name_to_find):
    if not db.current_db:
        messagebox.showerror("Error", "No database opened")
        return
    name_to_find = factory_name_to_find.get()
    if not name_to_find:
        return
    db.delete_factorys_by_name(db.current_db, name_to_find)
    show_all_factorys(db, factory_listbox)


def main():
    root = Tk()
    root.title(TITLE)
    root.geometry(R_GEOMETRY)
    db = carDatabase(CRED_FILENAME)

    # TODO close all connections
    car_scrollbar = Scrollbar(root)
    car_scrollbar.place(relheight=0.9, relwidth=0.02, relx=0.48, rely=0.2)

    factory_scrollbar = Scrollbar(root)
    factory_scrollbar.place(relheight=0.9, relwidth=0.02, relx=0.98, rely=0.2)

    car_listbox = Listbox(root, yscrollcommand=car_scrollbar.set)
    factory_listbox = Listbox(root, yscrollcommand=factory_scrollbar.set)

    car_listbox.place(relheight=0.7, relwidth=0.48, rely=0.2)

    factory_listbox.place(relheight=0.7, relwidth=0.48, rely=0.2, relx=0.5)

    add_menu(root, car_listbox, factory_listbox, db)

    add_car_button = Button(root, text='Add car', command=lambda: add_car(db, factory_listbox, car_listbox))
    add_car_button.place(relheight=0.05, relwidth=0.1, relx=0.65, rely=0.9)

    add_factory_button = Button(root, text='Add factory',
                                 command=lambda: add_factory(db, factory_listbox, car_listbox))
    add_factory_button.place(relheight=0.05, relwidth=0.1, relx=0.85, rely=0.9)

    update_car_button = Button(root, text='Update car',
                                command=lambda: update_car(db, car_listbox, factory_listbox))
    update_car_button.place(relheight=0.05, relwidth=0.1, rely=0.9)

    update_factory_button = Button(root, text='Update factory', command=lambda: update_factory(db, factory_listbox))
    update_factory_button.place(relheight=0.05, relwidth=0.1, relx=0.15, rely=0.9)

    delete_car_button = Button(root, text='Delete car', command=lambda: drop_car(db, car_listbox, factory_listbox))
    delete_car_button.place(relheight=0.05, relwidth=0.1, relx=0.3, rely=0.9)

    delete_factory_button = Button(root, text='Delete factory', command=lambda: drop_factory(db, factory_listbox))
    delete_factory_button.place(relheight=0.05, relwidth=0.1, relx=0.45, rely=0.9)

    car_name_to_find = StringVar()
    label = Label(root, text='Name:', font=10)
    label.place(relheight=0.05, relwidth=0.4)
    entry = Entry(root, textvariable=car_name_to_find, font=10)
    entry.place(relheight=0.05, relwidth=0.4, rely=0.05)
    search_car_button = Button(root, text='Search', command=lambda: search_car(db, car_listbox, car_name_to_find))
    search_car_button.place(relheight=0.05, relwidth=0.07, relx=0.4, rely=0.05)
    delete_car_by_name_button = Button(root, text='Delete',
                                        command=lambda: delete_cars_by_name(db, car_listbox, factory_listbox,
                                                                             car_name_to_find))
    delete_car_by_name_button.place(relheight=0.05, relwidth=0.07, relx=0.4, rely=0.1)

    factory_name_to_find = StringVar()
    label = Label(root, text='Name:', font=10)
    label.place(relheight=0.05, relwidth=0.4, relx=0.5)
    entry = Entry(root, textvariable=factory_name_to_find, font=10)
    entry.place(relheight=0.05, relwidth=0.4, relx=0.5, rely=0.05)
    search_car_button = Button(root, text='Search',
                                command=lambda: search_factory(db, factory_listbox, factory_name_to_find))
    search_car_button.place(relheight=0.05, relwidth=0.07, relx=0.9, rely=0.05)
    delete_factory_by_name_button = Button(root, text='Delete',
                                            command=lambda: delete_factorys_by_name(db, factory_listbox,
                                                                                     factory_name_to_find))
    delete_factory_by_name_button.place(relheight=0.05, relwidth=0.07, relx=0.9, rely=0.1)

    show_all_car_button = Button(root, text='Show all cars', command=lambda: show_all_cars(db, car_listbox))
    show_all_car_button.place(relheight=0.05, relwidth=0.4, relx=0.0, rely=0.1)
    show_all_factorys_button = Button(root, text='Show all factorys',
                                       command=lambda: show_all_factorys(db, factory_listbox))
    show_all_factorys_button.place(relheight=0.05, relwidth=0.4, relx=0.5, rely=0.1)

    root.mainloop()


if __name__ == '__main__':
    main()
