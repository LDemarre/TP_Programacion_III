"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem
from node import Node
from random import choice
from time import time


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Crear el nodo inicial
        actual = Node(problem.init, problem.obj_val(problem.init))

        while True:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual.state)

            # Buscar las acciones que generan el  mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local
            if diff[act] <= 0:
                self.tour = actual.state
                self.value = actual.value
                end = time()
                self.time = end-start
                return

            # Sino, moverse a un nodo con el estado sucesor
            else:
                actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Guardamos las soluciones en una lista
        solution_list = []

        # Hacemos los reseteos con un valor arbitrario
        for i in range(5):
            problem.random_reset()         
            actual = Node(problem.init, problem.obj_val(problem.init))

            while True:
                # Determinar las acciones que se pueden aplicar
                # y las diferencias en valor objetivo que resultan
                diff = problem.val_diff(actual.state)

                # Buscar las acciones que generan el  mayor incremento de valor obj
                max_acts = [act for act, val in diff.items() if val == max(diff.values())]

                # Elegir una accion aleatoria
                act = choice(max_acts)

                # Retornar si estamos en un optimo local
                if diff[act] <= 0:
                    break

                # Sino, moverse a un nodo con el estado sucesor
                else:
                    actual = Node(problem.result(actual.state, act), actual.value + diff[act])
                    self.niters += 1

            # Agregamos el estado actual a la lista de soluciones
            solution_list.append(actual)

        solution = max(solution_list, key=lambda node: node.value)
        self.tour = solution.state
        self.value = solution.value
        end = time()
        self.time = end-start
        return

class Tabu(LocalSearch):
    """Clase que representa el algoritmo de búsqueda Tabú."""

    def solve(self, problem: OptProblem) -> None:
        """Resuelve un problema utilizando el algoritmo de búsqueda Tabú.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        """
        # Inicio del reloj
        start = time()

        # Configuración de parámetros
        max_iter = 1500  # número máximo de iteraciones
        tabu_size = 10  # tamaño de la lista tabú

        # Inicialización
        current_state = problem.init
        best_solution = Node(current_state, problem.obj_val(problem.init))
        tabu_list = []

        # Bucle principal
        for i in range(max_iter):
            # Generar lista de acciones candidatas
            candidate_actions = problem.actions(current_state)

            # Calcular la diferencia de valor objetivo para cada acción
            diff = problem.val_diff(current_state)

            # Filtrar acciones tabú
            candidate_actions = [i for i in candidate_actions if i not in tabu_list]

            # Seleccionar la mejor acción no tabú
            best_action = max(candidate_actions, key=lambda a: diff[a])

            # Obtener el estado sucesor y su valor objetivo
            successor_state = problem.result(current_state, best_action)
            actual = Node(successor_state, problem.obj_val(successor_state))

            # Actualizar el mejor estado y su valor objetivo si corresponde
            if actual.value > best_solution.value:
                best_solution = actual

            # Actualizar el estado actual
            current_state = list(successor_state)

            # Agregar la acción tabú a la lista tabú
            tabu_list.append(best_action)

            # Mantener el tamaño de la lista tabú
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

        # Establecer los resultados finales
        self.niters = i + 1
        self.tour = best_solution.state
        self.value = best_solution.value
        end = time()
        self.time = end-start
        return
