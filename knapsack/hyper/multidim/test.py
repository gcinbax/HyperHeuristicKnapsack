import pickle

import numpy as np
from cvxpy import *

from knapsack.hyper.multidim import genetic
from knapsack.hyper.multidim import read_write_file as io

mknap1_path, mknap2_path = "./resources/mknap1.txt", "./resources/mknap2.txt"
mknapcbs_pathes = ["./resources/mknapcb1.txt", "./resources/mknapcb2.txt", "./resources/mknapcb3.txt",
                   "./resources/mknapcb4.txt",
                   "./resources/mknapcb5.txt", "./resources/mknapcb6.txt", "./resources/mknapcb7.txt",
                   "./resources/mknapcb8.txt",
                   "./resources/mknapcb9.txt"]
mknapres_path = "./resources/mkcbres.txt"


def generate_initial_knapsack(optimal, weights, costs, sizes):
    initial_knapsack = np.zeros(len(costs))

    # for item_index in list(range(len(costs))):
    #     pseudo_optimal_value = pseudo_optimal[item_index]
    #     initial_knapsack[item_index] = random.randint(0, 1) if pseudo_optimal_value == 1 else 0
    #
    # initial_fitness = problem.solve(initial_knapsack, costs, weights, sizes)
    return initial_knapsack


def solve(knapsack, attempts=50):
    optimal_fitness = knapsack["optimal"]
    result = 0
    cumulative_gap = 0
    print("Optimal_fitness:\t" + str(optimal_fitness))
    solved = []
    # TODO generate initial state using LP-relaxed solution
    for i in range(1, attempts + 1):
        start = generate_initial_knapsack(**knapsack)
        optimal_funcs, current = genetic.minimize(weights=knapsack["weights"], costs=knapsack["costs"],
                                                  sizes=knapsack["sizes"], included=start)
        current = genetic.fitness_hyper_ksp(optimal_funcs, weights=knapsack["weights"], costs=knapsack["costs"],
                                            sizes=knapsack["sizes"], included=start)
        fitness_current_diff = optimal_fitness - current
        print("Current:\t" + str(current))
        solved.append(fitness_current_diff)
        result += fitness_current_diff
        current_gap = 100 * (fitness_current_diff) / optimal_fitness
        print("Normalized:\t" + str(current_gap))
        cumulative_gap += current_gap
        print("Normed cum:\t" + str(cumulative_gap / attempts))
    return solved, cumulative_gap / attempts


def ksp_solve_lp_relaxed_convex(costs, weights, sizes):
    x = Variable(len(costs))
    weights_param = Parameter(rows=len(sizes), cols=len(costs))
    weights_param.value = np.asarray(weights)
    costs_param = Parameter(len(costs))
    costs_param.value = costs

    constr1 = [weights_param * x < sizes]
    constr2 = [x <= [1] * len(costs)]
    constr3 = [0 < x, x < 1]
    objective = Maximize(costs_param.T * x)

    solution = Problem(objective, constr1 + constr2 + constr3).solve()
    return solution


if __name__ == '__main__':
    knapsackses = io.parse_mknapcb(mknapcbs_pathes, mknapres_path)
    # knapsacks = io.parse_mknap1(mknap1_path)
    # lp_optimals = [lp.ksp_solve_lp_relaxed_greedy(**knapsack) for knapsack in knapsacks]
    optimals = []
    results = []
    ksp_number = 0
    for index, knapsacks in enumerate(knapsackses):
        for knapsack in knapsacks:
            print("KNAPSACK:")
            print("Number of constraints: " + str(len(knapsack["sizes"])))
            print("Number of items: " + str(len(knapsack["costs"])))
            print(ksp_solve_lp_relaxed_convex(knapsack["costs"], knapsack["weights"], knapsack["sizes"]))
            solved, normalized = solve(knapsack, attempts=10)
            optimals.append(normalized)
            with open("resources/output/mknapcbs/mknapcb" + str(index) + "_out_" + str(ksp_number) + ".pckl",
                      'wb') as out:
                pickle.dump({
                    "const": len(knapsack["sizes"]),
                    "items": len(knapsack["costs"]),
                    "solved": solved,
                    "normalized:": normalized
                }, out)
            ksp_number += 1
            print()
    print("CUMULATIVE GAP OVER ALL TEST DATA: " + str(optimals))
