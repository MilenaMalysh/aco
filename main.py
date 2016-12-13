from itertools import repeat
import random
import bisect


def main():
    def calculate_probability(ant, number_variants):
        variants = []
        counter = 0
        for j in range(number_variants):
            numerator = 0
            if nodes[ant[-1]][j] != 0 and (j not in ant):
                numerator = pow((pheromones[ant[-1]][j]), a) * pow(1 / (nodes[ant[-1]][j]), b)
                counter += numerator
            variants.append(numerator)
        for j in range(number_variants):
            variants[j] /= counter
            variants[j] += variants[j - 1] if j != 0 else 0
        return variants, variants[-1]

    a = 1
    b = 3
    t_max = 100
    ant_n = 40
    p = 0.5
    textfiles = {55: "yuzSHP55.aco", 95: "yuzSHP95.aco", 155: "yuzSHP155.aco", 6: "yuzSHP5.aco"}

    file_id = int(input("Enter id file: "))
    with open(textfiles.get(file_id)) as textFile:
        nodes = [[int(i) for i in line.split()] for line in textFile]

    pheromones = [[1 / file_id for i in repeat(None, file_id)] for j in repeat(None, file_id)]
    random.seed()

    for i in range(file_id):
        for j in range(file_id):
            pheromones[i][j] = 1.0 / file_id

    for j in range(t_max):
        ants = {key: [0] for key in range(ant_n)}
        flag_global = 1
        global_min_length = -1
        min_length = -1
        for i in range(ant_n):
            current_length = 0
            while ants[i][-1] != file_id - 1:
                current_variants, summa = calculate_probability(ants[i], file_id)
                random_value = random.uniform(0, summa)
                index_choice = bisect.bisect_left(current_variants, random_value)
                current_length += nodes[ants[i][-1]][index_choice]
                ants[i].append(index_choice)

            if min_length > current_length or min_length == -1:
                min_length = current_length
                min_path = list(ants[i])


            cbest = global_min_length if (flag_global and global_min_length != -1) else (min_length)

            ph_max = 1 / ((1 - p) * cbest)
            ph_min = ph_max / a

            for k in range(len(ants[i])):
                pheromones[ants[i][-2]][ants[i][-1]] += 1 / cbest
                if pheromones[ants[i][-2]][ants[i][-1]] < ph_min:
                    pheromones[ants[i][-2]][ants[i][-1]] = ph_min
                elif pheromones[ants[i][-2]][ants[i][-1]] > ph_max:
                    pheromones[ants[i][-2]][ants[i][-1]] = ph_max

        if global_min_length > min_length or global_min_length == -1:
            global_min_length = min_length
            global_min_path = list(min_path)

        for i in range(file_id):
            for k in range(file_id):
                pheromones[i][k] *= (1 - p)
    print('Shortest path', global_min_path, '\n Length: ', global_min_length)


if __name__ == "__main__":
    main()
