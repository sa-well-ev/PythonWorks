import tkinter as tk
from tkinter import filedialog
import pandas as pd

# Создаем скрытое главное окно
root = tk.Tk()
root.withdraw()

# Открываем диалог выбора файла
file_path = filedialog.askopenfilename(
    title="Выберите CSV файл",
    filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
)

if file_path:
    df = pd.read_csv(file_path, encoding='utf-8')
    # DataFrame df теперь содержит данные из файла
else:
    print("Файл не выбран.")

# Закрываем главное окно
root.destroy()