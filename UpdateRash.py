import tkinter as tk
from tkinter import filedialog
import pandas as pd
import sqlite3

##############################
# Запрс имени файла через меню
##############################

# Создаем скрытое главное окно
root = tk.Tk()
root.withdraw()

# Открываем диалог выбора файла
file_path = filedialog.askopenfilename(
    title="Выберите Excel файл",
    filetypes=[("Excel files", "*.xls?"), ("All files", "*.*")]
)
# Закрываем главное окно
root.destroy()

################################################
# Загружаем данные из Excel и меняем структуру
################################################

# Загружаем выбранный Excel
df = pd.read_excel(file_path, sheet_name="Сборная",
                   usecols=['Плата', 'Дата', 'Сумма', 'Категория2', 'Источник', 'Комментарий'],
                   dtype={
                       'Плата': int,
                       'Сумма': float,
                       'Категория2': str, 
                       'Источник': str, 
                       'Комментарий': str
                   }                   
)

# Переименовываем как в БД
df.columns=['payment', 'date', 'amount', 'category', 'source', 'comment']
# Убираем подъёбку с датами отсекая миллисекунды
df.date = df.date.dt.floor('s')
#######################################
# Записываем в БД только новые записи
#######################################

# Подключение к базе данных Sqlite
conn = sqlite3.connect('./data/finance.lite')

# Максимальная дата в таблице
v_max_date = pd.read_sql('SELECT MAX(date) FROM trans_all', conn).iloc[0, 0]

# Если в таблице есть записи, то отбираем только новые, иначе загружаем всё
if pd.notna(v_max_date):
    df_new = df.loc[df.date > v_max_date]
else:
    df_new = df

# Добавление записей в существующую таблицу trans_all базы данных finance.lite
df_new.to_sql('trans_all', conn, if_exists='append', index=False)

# закрытие соединения с базой данных
conn.close()

print(df_new.head(100))