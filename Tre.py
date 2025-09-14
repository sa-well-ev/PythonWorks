import pandas as pd

file_path = input("Введите путь к CSV файлу: ")

if file_path:
    df = pd.read_csv(file_path, encoding='utf-8')
    # DataFrame df теперь содержит данные из файла
else:
    print("Файл не выбран.")
