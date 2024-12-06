import os
import numpy as np
import csv

class OutToFile:
    def __init__(self, filename):
        self.filename = filename

        if not os.path.exists('out'):
            os.makedirs('out')

        self.filepath = os.path.join('out', self.filename)

    def clear_file(self):
        with open(self.filepath, 'w') as file:
            pass

    def print_string_to_file(self, content):
        with open(self.filepath, 'a') as file:
            file.write(content + "\n")

    def write_numpy_to_csv(self, array, precision=2):
        """
        Writes a numpy array to a CSV file with specified precision.

        :param array: Numpy array to write.
        :param precision: Number of decimal places to round to.
        """
        if not isinstance(array, np.ndarray):
            raise ValueError("Input must be a numpy array")

        with open(self.filepath, 'w', newline='') as file:
            writer = csv.writer(file)
            for row in array:
                rounded_row = [round(val, precision) for val in row]
                writer.writerow(rounded_row)

def round_to_significant_figures(value, significant_digits):
    """
    Округляет число до заданного количества значащих цифр.

    :param value: Число для округления.
    :param significant_digits: Количество значащих цифр.
    :return: Округленное число.
    """
    if value == 0:
        return 0
    return round(value, significant_digits - int(np.floor(np.log10(abs(value)))) - 1)

import csv

def display_csv_as_table(file_path):
    """
    Читает содержимое CSV-файла и выводит его в табличном формате.

    :param file_path: Путь к CSV-файлу для чтения.
    """
    try:
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames

            # Вывод заголовков таблицы
            header_line = "".join(f"{header:<25}" for header in headers)
            print(header_line)
            print("-" * len(header_line))

            # Вывод строк таблицы
            for row in reader:
                row_line = "".join(f"{str(row[header]):<25}" for header in headers)
                print(row_line)
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
