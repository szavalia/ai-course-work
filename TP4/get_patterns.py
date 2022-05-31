from letters import alphabet
import itertools
import numpy as np
import sys

max_combins = int(sys.argv[1])
order = sys.argv[2].lower() == 'true'

flat_letters = {
    k: np.array(m).flatten() for (k, m) in alphabet.items()
    }
all_groups = itertools.combinations(flat_letters.keys(), r=4)

avg_dot_product = []
max_dot_product = []

index = 0
for g in all_groups:
    group = np.array([v for k,v in flat_letters.items() if k in g])
    orto_matrix = group.dot(group.T)
    np.fill_diagonal(orto_matrix, 0)
    row, _ = orto_matrix.shape
    avg_dot_product.append((np.abs(orto_matrix).sum()/(orto_matrix.size-row), g))
    max_dot_product.append((np.abs(orto_matrix).max(), g))
    index+=1

avg_dot_product = sorted(avg_dot_product, key=lambda x: x[0], reverse=order)

for i in range(max_combins):
    print("Patterns: {0}, Avg_dot: {1}".format(avg_dot_product[i][1],avg_dot_product[i][0]))