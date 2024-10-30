# Algoritmo Shunting Yard para convertir una expresión regular infix a postfix
def shunt(infix_expression):
    # Define la precedencia de operadores especiales en la expresión regular
    precedence = {'*': 50, '.': 40, '|': 30, '+': 40, '?': 35}

    postfix_expression = ""
    operator_stack = ""

    for char in infix_expression:
        # Si es un paréntesis izquierdo, lo agrega al stack
        if char == '(':
            operator_stack += char
        # Si es un paréntesis derecho, vacía el stack hasta encontrar el paréntesis izquierdo
        elif char == ')':
            while operator_stack[-1] != '(':
                postfix_expression += operator_stack[-1]
                operator_stack = operator_stack[:-1]
            operator_stack = operator_stack[:-1]  # Elimina el paréntesis izquierdo
        # Si es un operador, aplica la precedencia
        elif char in precedence:
            while operator_stack and precedence.get(char, 0) <= precedence.get(operator_stack[-1], 0):
                postfix_expression += operator_stack[-1]
                operator_stack = operator_stack[:-1]
            operator_stack += char
        else:
            # Si es un carácter regular, lo agrega directamente a la expresión postfix
            postfix_expression += char

    # Vacía el stack de operadores restantes
    while operator_stack:
        postfix_expression += operator_stack[-1]
        operator_stack = operator_stack[:-1]

    return postfix_expression


class State:
    """Clase que representa un estado en el Autómata Finito No Determinista (NFA)."""

    def __init__(self):
        # Cada estado tiene una lista de transiciones con pares (carácter, siguiente estado)
        self.transitions = []  # Lista de transiciones


class NFA:
    """Clase que representa un NFA con un estado inicial y un estado de aceptación."""

    def __init__(self, start_state, accept_state):
        self.start_state = start_state  # Estado inicial del NFA
        self.accept_state = accept_state  # Estado de aceptación del NFA


def compile_postfix(postfix_expression):
    """Compila una expresión regular en notación postfix en un NFA usando el algoritmo de Thompson."""
    nfa_stack = []

    for char in postfix_expression:
        # Si el carácter es un símbolo alfabético, crea un NFA simple
        if char.isalpha():
            start_state = State()
            accept_state = State()
            start_state.transitions.append((char, accept_state))
            nfa_stack.append(NFA(start_state, accept_state))
        # Operador de concatenación
        elif char == '.':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa1.accept_state.transitions.append((None, nfa2.start_state))
            nfa_stack.append(NFA(nfa1.start_state, nfa2.accept_state))
        # Operador de unión (alternativa)
        elif char == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            start_state = State()
            accept_state = State()
            start_state.transitions.extend([(None, nfa1.start_state), (None, nfa2.start_state)])
            nfa1.accept_state.transitions.append((None, accept_state))
            nfa2.accept_state.transitions.append((None, accept_state))
            nfa_stack.append(NFA(start_state, accept_state))
        # Cierre de Kleene (cero o más repeticiones)
        elif char == '*':
            nfa = nfa_stack.pop()
            start_state = State()
            accept_state = State()
            start_state.transitions.extend([(None, nfa.start_state), (None, accept_state)])
            nfa.accept_state.transitions.extend([(None, nfa.start_state), (None, accept_state)])
            nfa_stack.append(NFA(start_state, accept_state))
        # Cierre positivo (uno o más repeticiones)
        elif char == '+':
            nfa = nfa_stack.pop()
            start_state = State()
            accept_state = State()
            start_state.transitions.append((None, nfa.start_state))
            nfa.accept_state.transitions.extend([(None, nfa.start_state), (None, accept_state)])
            nfa_stack.append(NFA(start_state, accept_state))

    # Devuelve el único NFA en la pila como el resultado final
    return nfa_stack.pop()


def follows_epsilon(state, reachable_states):
    """Calcula el cierre epsilon (ε) de un estado."""
    if state not in reachable_states:
        reachable_states.add(state)
        for (transition_char, next_state) in state.transitions:
            if transition_char is None:  # Transición ε
                follows_epsilon(next_state, reachable_states)


def simulate_nfa(nfa, input_string):
    """Simula la ejecución del NFA en una cadena de entrada."""
    current_states = set()
    follows_epsilon(nfa.start_state, current_states)  # Cierre epsilon del estado inicial

    # Procesa cada carácter de la cadena de entrada
    for char in input_string:
        next_states = set()
        for state in current_states:
            for (transition_char, next_state) in state.transitions:
                if transition_char == char:
                    follows_epsilon(next_state, next_states)
        current_states = next_states

    # Verifica si el estado de aceptación es alcanzable
    return nfa.accept_state in current_states


def main():
    # Solicita al usuario ingresar la expresión regular y las cadenas de prueba
    regex = input("Dame la expresión regular: ")
    test_strings = []
    while True:
        test = input("Ingresa una cadena para probar (o 'salir' para terminar): ")
        if test.lower() == 'salir':
            break
        test_strings.append(test)

    # Convierte la expresión regular infix a postfix
    postfix_regex = shunt(regex)
    print("Expresión en notación postfix:", postfix_regex)

    # Compila el postfix en un NFA
    nfa = compile_postfix(postfix_regex)

    # Prueba cada cadena y muestra si es aceptada o no
    for s in test_strings:
        result = simulate_nfa(nfa, s)
        print(f"¿La cadena '{s}' es aceptada? {'Sí' if result else 'No'}")


# Ejecuta la función principal
main()
