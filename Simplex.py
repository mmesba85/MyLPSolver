__author__ = "Mesbahi Maroua"
__email__ = "maroua.mesbahi@epita.fr"

import numpy as np
import fractions as frac
from time import time

"""
    Simplex.py contient les classes suivantes:
        - _Simplex: choix des variables entrantes pour le pivot, appel a pivot
        - Simplex: fait appel a _Simplex apres application des modifications necessaires a
            l'instance de LP
"""

class _Simplex:

    """
        Initialisation de l'objet _Simplex:
            affectation/construction des fonctions entering et leaving
    """
    def __init__(self, leaving_index=None, entering_index=None):
        if not leaving_index:
            def func_l(l):
                m = 0
                while not l[m] and m < len(l):
                    m += 1
                if m == len(l):
                    return 0
                for i in range(len(l)):
                    if l[i] and l[m] > l[i]:
                        m = i
                return m;
            leaving_index = func_l

        if not entering_index:
            def func_e(l):
                a = l.table
                entering_choices = [i for i in map(lambda x: 0 if x > 0 else x, a[0, :-1])]
                return entering_choices.index(min(entering_choices))
            entering_index = func_e

        self.entering_index = entering_index
        self.leaving_index = leaving_index

    """
        Resolution du programme lineaire
    """
    def __call__(self, lp, lp_gen, recursion_limit=100):
        n = 0
        a = lp.table
        s = _Simplex()
        while any(a[0, :-1] < 0) and n < recursion_limit:
            e = s.entering_index(lp)
            leaving_choices = [None]*lp.shape[0]
            for i in range(lp.shape[0]):
                if a[i+1, e] > 0:
                    leaving_choices[i] = (a[i+1, -1]/a[i+1, e])
            if not [i for i in leaving_choices if i]:
                lp_gen.bounded = False
                raise OverflowError("Programme lineaire non bornee")
            else:
                l = 1 + s.leaving_index(leaving_choices)
            lp.pivot(e, l)
            n += 1

        form = "Solutions de base = " + \
               "(" + "{}, " * (lp.shape[1] - 1) + "{})" + \
               " Valeur Objective = {}."
        print(form.format(*lp.basic_sol(), lp.table[0, -1]))
        form = "Nomnbre de recursions: {}"
        print(form.format(n))
        return lp.basic_sol(), lp.table[0, -1]

"""
    Recupere la cle correspondant a une valeur dans un dictionnaire (basic_vars)
"""
def get_key(basic_vars, val):
    for k, v in basic_vars.items():
        if v == val:
            return k
    return 0


class Simplex:

    """
        Traitement de l'instance LP selon si elle a une solution de base admissible ou non
    """
    def _phase_one(self, lp):
        if lp.basic_feasible:
            return True

        gain_fun = np.copy(lp.table[0])
        lp.shape = (lp.shape[0], lp.shape[1] + 1)
        lp.table = np.insert(lp.table, 0, frac.Fraction(-1, 1), axis=1)
        lp.table[0] = np.hstack((np.ones(1, dtype=frac.Fraction),
                                    np.zeros(lp.shape[1], dtype=frac.Fraction)))
        m = lp.shape[0]
        for i in range(1, m+1):
            lp.basic_vars[i] = lp.basic_vars[i] + 1
        l = 1 + np.argmin(lp.table[1:, -1])
        lp.pivot(0, l)
        if _Simplex.__call__(self, lp)[1] == 0:
            if 0 in lp.basic_vars.values():
                l = get_key(lp.basic_vars, 0)
                e = 0
                while e < lp.shape and lp.table[l, e] == 0:
                    e += 1
                lp.pivot(e, l)

            for i in range(1, m+1):
                lp.basic_vars[i] = lp.basic_vars[i] - 1
            lp.table = lp.table[:, 1:]
            lp.shape = (lp.shape[0], lp.shape[1] - 1)

            lp.table[0] = gain_fun
            for i in lp.basic_vars.values():
                k = get_key(lp.basic_vars, i) - 1
                lp.table[0, :] = lp.table[0, :] - \
                                      lp.table[0, i] * \
                                      lp.table[1 + k, :]
            lp.table[0, -1] = -lp.table[0, -1]
            return True
        else:
            return False

    """
        Entree de l'algorithme du simplex
    """
    def __call__(self, lp, lp_gen):
        t0 = time()
        l = lp
        if not self._phase_one(l):
            dual = l.dual()
            if self._phase_one(dual):
                lp_gen.dual_basic_feasible = True
                return _Simplex(dual)
            else:
                self._phase_one(lp)
                s = _Simplex()
                s(lp)
        else:
            lp_gen.feasible = True
            s = _Simplex()
            s(lp, lp_gen)
        t1 = time()
        form = "Temps de resolution: {} "
        print(form.format(t1-t0))
