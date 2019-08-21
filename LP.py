__author__ = "Mesbahi Maroua"
__email__ = "maroua.mesbahi@epita.fr"

from random import randint
import numpy
import fractions as frac
from Simplex import Simplex
import pickle
import sys

"""
    LP.py contient les classes suivantes:
        class LP: 
            * construction de l'objet LP
            * construction du dual
            * pivot
        class lp_generator:
            * construction de l'objet lp_generator qui contient l'objet LP ainsi 
                que les informations concernant l'algorithme comme speficifiee dans 
                le fichier spec_LP.md
            * construction du dictionnaire contenant les informations relatives au lp_generator
            * sauvegarde de l'objet lp_generator
            * lecture de l'objet lp_generator
    LP.py contient les methodes statiques suivantes:
        * main: gere les cas d'execution ou de test
        * init: creer l'objet lp_generator (et l'objet LP correspondant) selon si l'utilisateur
            a choisi une generation aleatoire ou en entree standard
"""

class LP:
    shape = ();
    basic_feasible = True;
    basic_vars= {};
    table_shape = ();
    table = numpy.empty(table_shape);

    """
        construit un objet LP a partir des vecteurs donnees:
            - func_vect: vecteur des coefficients de la fonction objectif
            - const_vect: matrice des contraintes d'inegalite
            - coef_vect: vecteur des coefficients constants a droite des contraintes d'inegalites
    """
    def __init__(self, func_vect, const_vect, coef_vect):
        m = len(const_vect);
        n = len(const_vect[0]);
        self.shape = (m, n+m);
        self.basic_vars = {};
        for i in range(1, m+1):
            self.basic_vars[i] = (n-1) + i;
        for j in range(0, len(coef_vect)-1):
            if coef_vect[j] < 0:
                self.basic_feasible = False;
        self.table_shape = (m+1, n+m+1);
        func_len = len(func_vect);
        table = [[0 for x in range(n+m+1)] for y in range(m+1)];
        id = [[0 for x in range(m)] for y in range(m)];
        for k in range(0, func_len):
            table[0][k] = (func_vect[k]) * (-1);

        for i in range(m):
            for j in range(m):
                if i == j:
                    id[i][j] = 1
                else:
                    id[i][j] = 0
        for i in range(0, m):
            for j in range(0, n):
                table[i+1][j] = const_vect[i][j];
                table[i+1][n+m] = coef_vect[i];

        for i in range(1,m+1):
            for k in range(n, n+m):
                table[i][k] = id[i-1][k-n]
        for i in range(m):
            table[i+1][n+m] = coef_vect[i];
        self.table = numpy.array(table);
    """
        verifie que les parametres du pivot correspondent aux specifications
    """
    def check_param(self, e, s):
        if s not in self.basic_vars.keys():
            return -1;
        if e in self.basic_vars.values():
            return -1;
        if self.table[s][e] == 0:
            return -1;
        return 0;

    """
        Applique la methode pivot
    """
    def pivot(self, e, s):
        k = self.check_param(e, s);
        if k == -1:
            return;
        self.table[s] = [x/self.table[s][e] for x in self.table[s]];
        for i, j in enumerate(self.table):
            if i != s:
                aux = [t * self.table[i][e] for t in self.table[s]];
                self.table[i] = [a - b for a, b in zip(self.table[i], aux)]
        self.basic_vars[s] = e;

    """
        Calcul le dual
    """
    def dual(self):
        m = self.shape[0]
        n = self.shape[1] - m
        func_vect = [0 for x in range(m)]
        coef_vect =    [0 for x in range(n)]
        const_vect = [[0 for x in range(n)] for y in range(m)];

        for i in range(0, n):
            coef_vect[i] = self.table[0][i] * (-1)
        
        for i in range(0, m):
            func_vect[i] = self.table[i+1][m+n]
        
        k = 0
        for i in range(m+n):
            if i not in self.basic_vars.values():    
                for j in range(1, m+1):
                    const_vect[j-1][k] = self.table[j][i]
                k = k + 1
        c = numpy.array(const_vect, dtype='f');
        d = numpy.transpose(c);
        numpy.transpose(d);        
        a = numpy.array(func_vect, dtype='f');
        numpy.transpose(a);
        b = numpy.array(coef_vect, dtype='f');
        numpy.transpose(b);
        return LP(a, d, b);

    """
        Retourne solution de base
    """
    def basic_sol(self):
        t = numpy.zeros(self.shape[1], dtype=frac.Fraction)
        for k, v in (self.basic_vars.items()):
            t[v] = self.table[k, -1]
        return t

class lp_generator:
    name = ""
    lp = None
    heuristique = ""
    feasible = False
    dual_basic_feasible = False
    bounded = True

    """
        Initialisation de l'objet lp_generator:
            - b : debut de l'interval
            - e : fin de l'interval
                un nombre aleatoire x est choisi parmi l'interval et un programme aleatoire
                de la taille x est cree
            - name : nom du programme lineaire
            - heuristique : nom de l'heuristique
            - lp : dans le cas ou les coefficients du programme lineaire sont donnees en entree
            - file : dans le cas ou on lance un programme lineaire enregistree au prealable
    """
    def __init__(self, b, e, name, heur, lp=None, file=None):
        if not file == None:
            return self.load(file)
        if lp == None:
            m = randint(b, e)
            n = randint(b, e)
            func_vect = [0 for x in range(n)]
            coef_vect =    [0 for x in range(m)]
            const_vect = [[0 for x in range(0, n)] for y in range(0, m)];
            for i in range(0, m):
                coef_vect[i] = frac.Fraction(randint(0, 100), randint(1, 100))

            for i in range(0, n):
                func_vect[i] = frac.Fraction(randint(0, 100), randint(1, 100))

            for i in range(0, m):
                for j in range(0, n):
                    const_vect[i][j] = frac.Fraction(randint(0, 100), randint(1, 100))

            lp = LP(func_vect, const_vect, coef_vect)
        self.name = name
        self.heuristique = heur
        self.dual_basic_feasible = lp.basic_feasible
        self.lp = lp
    """
        Creer un dictionnaire contenant les informations relatives au generateur
    """
    def get_dict(self):
        dict = {}
        dict['name'] = self.name
        dict['heuristique'] = self.name
        dict['LP'] = self.lp
        dict['feasible'] = self.feasible
        dict['basic_feasible'] = self.lp.basic_feasible
        dict['dual_basic_feasible'] = self.dual_basic_feasible
        dict['bounded'] = self.bounded
        return dict
    """
        Sauvegarde le generateur
    """
    def save(self, file):
        out = open(file, "wb")
        pickle.dump(self, out)
        out.close()

    """
        Creer un objet lp_generator a partir d'un fichier de serialization
    """
    def load(self, file):
        file_in = open(file, "rb")
        aux = pickle.load(file_in)
        self.name = aux.name
        self.lp = aux.lp
        self.heuristique = aux.heuristique
        self.feasible = aux.feasible
        self.dual_basic_feasible = aux.dual_basic_feasible
        self.bounded = aux.bounded


"""
    Verifie les entrees utilisateurs
"""
def check_entries(coeff_func, coeff_cst, A):
    m = len(A)
    n = len(A[0])
    if len(coeff_func) != n:
        return False
    if len(coeff_cst) != m:
        return False
    return True

"""
    Remplis les vecteurs selon l'entree utilisateur
"""
def fill_array(str):
    aux = str.split(" ")
    res = []
    for n in aux:
        try:
            num, den = n.split('/')
            res.append(frac.Fraction(int(num), int(den)))
        except:
            res.append(frac.Fraction(int(n), 1))
    return res

"""
    Initialisation du programme:
        Un objet lp_generator est creer selon les entrees des utilisateurs:
            - aleatoirement
            - specifique
            - lecture fichier
"""
def init():
    try:
        choice = input("Charger un programme lineaire existant [Y/n] ")
        if choice == 'n':
            name = input("Entrer un nom pour identifier le programme: ")
            heur = input("Entrer un nom pour l'heuristique: ")
            print("[1] Generer un programme lineaire aleatoire")
            print("[2] Entrer un programme lineaire")
            choice = int(input("[1]/[2]? "))
            if choice == 2:
                cf = input("Entrer les coefficients de la fonction objectif: ")
                cc = input("Entrer les coefficients constants a droite des contraintes d'inegalite: ")
                func_vect = fill_array(cf)
                coeff_cst = fill_array(cc)

                print("Entrer la matrice des contraintes d'inegalite: ")
                R = int(input("Entrer nombre de lignes: "))
                C = int(input("Entrer nombre de colonnes: "))
                A = []
                print("Entrer les coefficients dans l'ordre des lignes de la matrice (Un coefficent/ligne): ")
                for i in range(R):
                    aux =[]
                    for j in range(C):
                        res = input()
                        try:
                            num, den = res.split('/')
                            aux.append(frac.Fraction(int(num), int(den)))
                        except:
                            aux.append(frac.Fraction(int(res), 1))
                    A.append(aux)

                if not check_entries(func_vect, coeff_cst, A):
                    raise ValueError("Wrong Entries")

                lp = LP(func_vect, A, coeff_cst)
                return lp_generator(0, 0, name, heur, lp)
            if choice == 1:
                interval = input("Entrer un interval pour le choix de la taille du programme lineaire sous la forme: beggining/end: ")
                size = interval.split("/")
                return lp_generator(int(size[0]), int(size[1]), name, heur)
        if choice == ' ' or choice == 'Y':
            file = input("Entrer le nom du fichier contenant la serialization du programme lineaire: ")
            return lp_generator(0, 0, "", "", None, file)
    except:
        raise ValueError("[Simplex Algorithm] : Wrong Entries")

"""
    Entree du programme
"""
def __main__():
    solver = Simplex()
    if len(sys.argv) == 4:
        if sys.argv[1] == '-gen':
            b = int(sys.argv[2])
            e = int(sys.argv[3])
            lp_gen = lp_generator(b, e, 'test', 'test', None, None)
            res = solver(lp_gen.lp, lp_gen)
            exit(res)
    else:
        lp_gen = init()
        res = solver(lp_gen.lp, lp_gen)
        dict = lp_gen.get_dict()
        print(dict)
        choice = input("Voulez-vous enregistrer le programme lineaire? [Y/n] ")
        if choice == 'Y' or choice == ' ':
            file = input("Entrer un nom pour le fichier: ")
            lp_gen.save(file)
    return res

__main__()


