################################################################################################
#               http://people.brunel.ac.uk/~mastjjb/jeb/orlib/mknapinfo.html                   #
################################################################################################
import os
import pickle


def parse_mknap1(path_to_file):
    results = []
    with open(path_to_file) as file:
        number_of_cases = int(file.readline())
        file.readline()
        for case in range(number_of_cases):
            item_number, ksp_number, optimal = file.readline().split(' ')
            item_number = int(item_number)
            ksp_number = int(ksp_number)
            optimal = float(optimal)
            costs = [float(cost) for cost in file.readline().split(' ')]
            weights = []
            for i in range(ksp_number):
                weights.append([int(weight) for weight in file.readline().split(' ')])
            sizes = [int(size) for size in file.readline().split(' ')]
            file.readline()
            results.append({
                'costs': costs,
                'weights': weights,
                'sizes': sizes,
                'optimal': optimal
            })
    return results


def parse_mknap2(path_to_file):
    results = []
    with open(path_to_file) as file:
        while True:
            line = file.readline()
            if line == '':
                break
            if line[0] == '#':
                continue
            ksp_number, item_number = line.split(' ')
            ksp_number = int(ksp_number)
            item_number = int(item_number)
            costs = []
            while len(costs) < item_number:
                costs += [float(cost) for cost in file.readline().split(' ')]
            sizes = []
            while len(sizes) < ksp_number:
                sizes += [float(size) for size in file.readline().split(' ')]
            weights = []
            for i in range(ksp_number):
                current_weight = []
                while len(current_weight) < item_number:
                    current_weight += [int(weight) for weight in file.readline().split(' ')]
                weights.append(current_weight)
            file.readline()
            optimal = int(file.readline())
            file.readline()
            results.append({
                'costs': costs,
                'weights': weights,
                'sizes': sizes,
                'optimal': optimal
            })
    return results


def parse_mknapcb(mknapcb_pathes, result_path):
    if os.path.isfile('resources/mknapcbs.pickle'):
        with open('resources/mknapcbs.pickle', 'rb') as out:
            return pickle.load(out)

    results = []
    with open(result_path) as file_results:
        for mknapcb_path in mknapcb_pathes:
            knapsack_chunk = []
            with open(mknapcb_path) as file_sources:
                number_of_cases = int(file_sources.readline())
                for case in range(number_of_cases):
                    _, item_number, ksp_number, _, _ = file_sources.readline().split(' ')
                    _, optimal = file_results.readline().split(' ')
                    optimal = int(optimal)
                    item_number = int(item_number)
                    ksp_number = int(ksp_number)

                    costs = []
                    while len(costs) < item_number:
                        costs += [float(cost) for cost in file_sources.readline().split(' ') if cost not in ('', '\n')]

                    weights = []
                    for i in range(ksp_number):
                        current_weight = []
                        while len(current_weight) < item_number:
                            current_weight += [int(weight) for weight in file_sources.readline().split(' ') if
                                               weight not in ('', '\n')]
                        weights.append(current_weight)

                    sizes = []
                    while len(sizes) < ksp_number:
                        sizes += [float(size) for size in file_sources.readline().split(' ') if size not in ('', '\n')]

                    knapsack_chunk.append({
                        'costs': costs,
                        'weights': weights,
                        'sizes': sizes,
                        'optimal': optimal
                    })
            results.append(knapsack_chunk)

    with open('resources/mknapcbs.pickle', 'wb') as out:
        pickle.dump(results, out)
    return results


def print_statistics(path_to_ksp_dir):
    average = 0
    ksp_stat_files = os.listdir(path_to_ksp_dir)
    n = len(ksp_stat_files)
    for ksp_path in ksp_stat_files:
        with open(path_to_ksp_dir + "/" + ksp_path, 'rb') as ksp_stat_file:
            ksp_stat = pickle.load(ksp_stat_file)
            average += ksp_stat['normalized:'] / n
    print(average)

if __name__ == '__main__':
    # pprint(parse_mknap1("./resources/mknap1.txt"))
    # pprint(parse_mknap2("./resources/mknap2.txt"))
    print_statistics("./resources/output/mknap1")
