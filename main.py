from benchmark import Benchmark
from utils import display_csv_as_table
from solver import Solver as SolverDefault
from solverBiCG import Solver as SolverBiCG


def main(test):
    if test:
        grid_sizes = [(10, 10), (40, 40), (80, 80), (160, 160), (320, 320), (500, 500)]
        task_numbers = [1, 2, 3, 4, 5]  # Список номеров задач
        benchmark = Benchmark("benchmark_results.csv")
        benchmark.run(grid_sizes, task_numbers, max_time = 300)
        benchmark.print_results()
        benchmark.save_results()
    else:
        display_csv_as_table("benchmark_results.csv")
def get_beautiful_pictures():
    for i in range(1, 6):
        s = SolverBiCG(51, 51, i)
        s.do_all()
S = SolverBiCG(50, 50, 7)
S.init(S.p)
# S.solve()
# S.plot_heatmap()
print(S.p)
print(S.Au(S.p))
S.solve()
S.plot_heatmap()
# get_beautiful_pictures()