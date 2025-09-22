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
df = pd.read_excel(file_path, sheet_name="Сборная")

# Оставляем нужные столбцы и переименовываем как в БД
df = df[['Плата', 'Дата', 'Сумма', 'Категория2', 'Источник']]
df.columns=['payment', 'date', 'amount', 'category', 'source']
# Убираем подъёбку с датами отсекая миллисекунды
df.date = df.date.dt.floor('s')
#######################################
# Записываем в БД только новые записи
#######################################

# Подключение к базе данных Sqlite
conn = sqlite3.connect('./data/finance.lite')

# Максимальная дата в таблице
v_max_date = pd.read_sql('SELECT MAX(date) FROM trans_all', conn).iloc[0, 0]

# Добавление записей в существующую таблицу trans_all базы данных finance.lite
df_new = df.loc[df.date > v_max_date]
df_new.to_sql('trans_all', conn, if_exists='append', index=False)

# закрытие соединения с базой данных
conn.close()

print(df_new.head(100))