# Algoritmo Shunting Yard 
def shunt(infix):
    # diccionario de caracteres especiales
    especiales = {'*': 50, '.': 40, '|': 30, '+': 40, '?': 35}

    pofix = ""
    stack = ""

    for c in infix:
        if c == '(':
            stack = stack + c
        elif c == ')':
            while stack[-1] != '(':
                # agrupa los elementos
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack[:-1]
        elif c in especiales:
            while stack and especiales.get(c, 0) <= especiales.get(stack[-1], 0):
                pofix, stack = pofix + stack[-1], stack[:-1]
            stack = stack + c

        else:
            pofix = pofix + c

    while stack:
        # agrupa los elementos
        pofix, stack = pofix + stack[-1], stack[:-1]

    return pofix

class State:
    def __init__(self):
        # Cada estado tiene una lista de transiciones (para caracteres y ε-transiciones)
        self.edges = []  # pares de (carácter, siguiente estado)

class NFA:
    def __init__(self, start, accept):
        self.start = start  # Estado inicial
        self.accept = accept  # Estado de aceptación

def compile_postfix(postfix):
    """Compila una expresión regular en notación postfix en un NFA usando el algoritmo de Thompson."""
    nfa_stack = []

    for char in postfix:
        if char.isalpha():  # Si es un símbolo (a-z)
            # Crear un NFA simple para un carácter
            start = State()
            accept = State()
            start.edges.append((char, accept))
            nfa_stack.append(NFA(start, accept))
        elif char == '.':  # Concatenación
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa1.accept.edges.append((None, nfa2.start))  # Conectar el aceptador del primero con el inicio del segundo
            nfa_stack.append(NFA(nfa1.start, nfa2.accept))
        elif char == '|':  # Alternativa (unión)
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            start = State()
            accept = State()
            start.edges.append((None, nfa1.start))  # Transición vacía a ambos NFA
            start.edges.append((None, nfa2.start))
            nfa1.accept.edges.append((None, accept))
            nfa2.accept.edges.append((None, accept))
            nfa_stack.append(NFA(start, accept))
        elif char == '*':  # Cierre de Kleene
            nfa = nfa_stack.pop()
            start = State()
            accept = State()
            start.edges.append((None, nfa.start))  # Conexión ε al NFA
            start.edges.append((None, accept))  # Conexión ε directa a aceptador (0 repeticiones)
            nfa.accept.edges.append((None, nfa.start))  # Conexión del final al inicio (para repeticiones)
            nfa.accept.edges.append((None, accept))  # Conexión ε al nuevo aceptador
            nfa_stack.append(NFA(start, accept))
        elif char == '+':  # Cierre positivo (1 o más repeticiones)
            nfa = nfa_stack.pop()
            start = State()
            accept = State()
            start.edges.append((None, nfa.start))  # Primera repetición es obligatoria
            nfa.accept.edges.append((None, nfa.start))  # Conexión del final al inicio (para más repeticiones)
            nfa.accept.edges.append((None, accept))  # Conexión ε al nuevo aceptador
            nfa_stack.append(NFA(start, accept))

    # El resultado es el único NFA en la pila
    return nfa_stack.pop()

# Función para probar si una cadena es aceptada por el NFA
def follows_epsilon(state, current_states):
    """Calcula el cierre epsilon (ε) de un estado."""
    if state not in current_states:
        current_states.add(state)
        for (char, next_state) in state.edges:
            if char is None:  # ε-transición
                follows_epsilon(next_state, current_states)

def simulate_nfa(nfa, input_string):
    """Simula la ejecución del NFA en una cadena de entrada."""
    current_states = set()
    follows_epsilon(nfa.start, current_states)  # Cierre epsilon del estado inicial

    for char in input_string:
        next_states = set()
        for state in current_states:
            for (edge_char, next_state) in state.edges:
                if edge_char == char:
                    follows_epsilon(next_state, next_states)  # Calcula el cierre epsilon del siguiente estado
        current_states = next_states

    # Verifica si el estado aceptador está en los estados alcanzados
    return nfa.accept in current_states


def main():
    regex = input("Dame la expresión regular: ")
    cadenas = []
    while True:
        test = input("Ingresa una cadena para probar (o 'salir' para terminar): ")
        if test.lower() == 'salir':
            break
        cadenas.append(test)
        
    postfix_regex = shunt(regex)  # Expresión regular en notación postfix
    print(postfix_regex)
    nfa = compile_postfix(postfix_regex)

    for s in cadenas:
        resultado = simulate_nfa(nfa, s)
        print(f"¿La cadena '{s}' es aceptada? {resultado}")


main()