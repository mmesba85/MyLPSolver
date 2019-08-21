__author__ = "Mesbahi Maroua"
__email__ = "maroua.mesbahi@epita.fr"

import matplotlib.pyplot as plt
import os
import sys

"""
    Script de test pour les programme LP SOLVER
    Execution: python3 test.py [arg] value
        [arg] : -rec / -time
        value: taille maximale du programme lineaire generee
"""

if len(sys.argv) == 3:
    type = sys.argv[1]
    if type != '-rec' and type != '-time':
        print("USE: python3 test.py -rec/-time [size]")
        exit(1)
    max = int(sys.argv[2])
    aux = int(max/10)
    step = 1
    if aux == 0:
        step = 1
    if aux <= 5 and aux > 0:
        step = 5
    if aux > 5 and aux <= 10:
        step = 10
    if aux > 10:
        step = 50
    size = int(max/step)
    sizes = [None] * size
    val = step
    for i in range(0, size):
        sizes[i] = val
        val += step

    form = "Execution de l'algorithme du Simplex pour des programmes lineaires inclus dans : {}"
    print(form.format(sizes))
    print("PROCESSING...")

    x = [None] * len(sizes)
    i = 0
    for n in sizes:
        form = 'python3 LP.py -gen {} {}'
        res = os.popen(form.format(str(n), str(n))).read()
        if type == '-rec':
            aux = res.split("Nomnbre de recursions: ")
        else:
            aux = res.split("Temps de resolution: ")
        n = aux[1].strip()
        x[i] = n
        i+=1

    plt.plot(sizes, x)
    if type == '-rec':
        plt.ylabel('Nombre de recursions')
    else:
        plt.ylabel("Temps d'execution")
    plt.xlabel('Size')
    plt.show()

else:
    print("USE: python3 test.py -rec/-time [size]")
