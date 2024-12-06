import csv
import time
import numpy as np
from solver import Solver as SolverDefault
from solverBiCG import Solver as SolverBiCG

class Benchmark:
    def __init__(self, output_file):
        self.output_file = output_file
        self.results = []

    def run(self, grid_sizes, task_numbers, tol=1e-2, max_time=10):
        """
        Запуск тестирования для различных размеров сетки и номеров задач.

        :param grid_sizes: Список кортежей (Nx, Ny) для тестирования.
        :param task_numbers: Список номеров задач для тестирования.
        :param tol: Порог сходимости для метода solve.
        :param max_time: Максимальное время выполнения в секундах для каждой сетки.
        """
        for task_number in task_numbers:
            for Nx, Ny in grid_sizes:
                print(f"Тестирование задачи {task_number} на сетке {Nx}x{Ny}...")

                # Запуск с SolverDefault
                solver_default = SolverDefault(Nx, Ny, task_num=task_number)
                start_time_default = time.time()
                solver_default.solve(tol=tol, max_time=max_time)
                elapsed_time_default = np.round(time.time() - start_time_default, 2)
                solver_default.plot_heatmap()
                residual_norm_default = solver_default.get_r_norm()

                # Запуск с SolverBiCG
                solver_bicg = SolverBiCG(Nx, Ny, task_num=task_number)
                start_time_bicg = time.time()
                solver_bicg.solve(tol=tol, max_time=max_time)
                elapsed_time_bicg = np.round(time.time() - start_time_bicg, 2)
                solver_bicg.plot_heatmap()
                residual_norm_bicg = solver_bicg.get_r_norm()

                # Вычисление соотношения времени
                time_ratio = np.round(elapsed_time_default / elapsed_time_bicg, 2) if elapsed_time_bicg > 0 else float('inf')

                self.results.append({
                    "Task Number": task_number,
                    "Nx": Nx,
                    "Ny": Ny,
                    "Time Default (s)": elapsed_time_default,
                    "Residual Norm Default": residual_norm_default,
                    "Time BiCG (s)": elapsed_time_bicg,
                    "Residual Norm BiCG": residual_norm_bicg,
                    "Time Ratio (Default/BiCG)": time_ratio
                })

    def save_results(self):
        """
        Сохранение результатов в CSV-файл.
        """
        with open(self.output_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "Task Number", "Nx", "Ny",
                "Time Default (s)", "Residual Norm Default",
                "Time BiCG (s)", "Residual Norm BiCG",
                "Time Ratio (Default/BiCG)"
            ])
            writer.writeheader()
            for result in self.results:
                writer.writerow(result)

    def print_results(self):
        """
        Вывод результатов в табличном виде.
        """
        print("\nРезультаты тестирования:")
        print(f"{'Task Number':<15}{'Nx':<10}{'Ny':<10}{'Time Default (s)':<20}{'Residual Norm Default':<25}{'Time BiCG (s)':<20}{'Residual Norm BiCG':<25}{'Time Ratio (Default/BiCG)':<25}")
        print("-" * 150)
        for result in self.results:
            print(f"{result['Task Number']:<15}{result['Nx']:<10}{result['Ny']:<10}{result['Time Default (s)']:<20.2f}{result['Residual Norm Default']:<25.2e}{result['Time BiCG (s)']:<20.2f}{result['Residual Norm BiCG']:<25.2e}{result['Time Ratio (Default/BiCG)']:<25.2f}")
