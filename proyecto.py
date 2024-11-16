import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx

# Clase para los estados en el NFA
class State:
    def __init__(self):
        self.transitions = []  # Lista de transiciones (carácter, siguiente estado)

# Clase para el NFA
class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state

# Función para convertir infix a postfix (Shunting Yard)
def shunt(infix_expression):
    precedence = {'*': 50, '.': 40, '|': 30, '+': 40, '?': 35}
    valid_chars = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789|*+?.()")  # Caracteres válidos
    postfix_expression = ""
    operator_stack = ""

    # Agregar concatenación explícita
    infix_with_concat = ""
    for i, char in enumerate(infix_expression):
        infix_with_concat += char
        if i < len(infix_expression) - 1:
            next_char = infix_expression[i + 1]
            if (char.isalnum() or char in "*+?)") and (next_char.isalnum() or next_char == '('):
                infix_with_concat += "."

    for char in infix_with_concat:
        if char == '(':
            operator_stack += char
        elif char == ')':
            while operator_stack and operator_stack[-1] != '(':
                postfix_expression += operator_stack[-1]
                operator_stack = operator_stack[:-1]
            if not operator_stack or operator_stack[-1] != '(':
                raise ValueError("Paréntesis desbalanceados en la expresión.")
            operator_stack = operator_stack[:-1]  # Elimina '('
        elif char in precedence:
            while (operator_stack and precedence.get(char, 0) <=
                   precedence.get(operator_stack[-1], 0)):
                postfix_expression += operator_stack[-1]
                operator_stack = operator_stack[:-1]
            operator_stack += char
        else:
            postfix_expression += char

    while operator_stack:
        if operator_stack[-1] == '(':
            raise ValueError("Paréntesis desbalanceados en la expresión.")
        postfix_expression += operator_stack[-1]
        operator_stack = operator_stack[:-1]

    return postfix_expression


# Función para compilar postfix a NFA
def compile_postfix(postfix_expression):
    nfa_stack = []
    for char in postfix_expression:
        if char.isalnum():
            start_state = State()
            accept_state = State()
            start_state.transitions.append((char, accept_state))
            nfa_stack.append(NFA(start_state, accept_state))
        elif char == '.':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            nfa1.accept_state.transitions.append((None, nfa2.start_state))
            nfa_stack.append(NFA(nfa1.start_state, nfa2.accept_state))
        elif char == '|':
            nfa2 = nfa_stack.pop()
            nfa1 = nfa_stack.pop()
            start_state = State()
            accept_state = State()
            start_state.transitions.extend([(None, nfa1.start_state), (None, nfa2.start_state)])
            nfa1.accept_state.transitions.append((None, accept_state))
            nfa2.accept_state.transitions.append((None, accept_state))
            nfa_stack.append(NFA(start_state, accept_state))
        elif char == '*':
            nfa = nfa_stack.pop()
            start_state = State()
            accept_state = State()
            start_state.transitions.extend([(None, nfa.start_state), (None, accept_state)])
            nfa.accept_state.transitions.extend([(None, nfa.start_state), (None, accept_state)])
            nfa_stack.append(NFA(start_state, accept_state))
        elif char == '+':
            nfa = nfa_stack.pop()
            start_state = State()
            accept_state = State()
            start_state.transitions.append((None, nfa.start_state))
            nfa.accept_state.transitions.extend([(None, nfa.start_state), (None, accept_state)])
            nfa_stack.append(NFA(start_state, accept_state))
        elif char == '?':
            nfa = nfa_stack.pop()
            start_state = State()
            accept_state = State()
            start_state.transitions.extend([(None, nfa.start_state), (None, accept_state)])
            nfa.accept_state.transitions.append((None, accept_state))
            nfa_stack.append(NFA(start_state, accept_state))
    return nfa_stack.pop()


# Función para el cierre epsilon
def follows_epsilon(state, reachable_states):
    if state not in reachable_states:
        reachable_states.add(state)
        for (transition_char, next_state) in state.transitions:
            if transition_char is None:
                follows_epsilon(next_state, reachable_states)

def simulate_nfa(nfa, input_string):
    current_states = set()
    follows_epsilon(nfa.start_state, current_states)

    for char in input_string:
        next_states = set()
        for state in current_states:
            for transition_char, next_state in state.transitions:
                if transition_char == char:
                    follows_epsilon(next_state, next_states)

        current_states = next_states  # Update current_states directly

    return any(state == nfa.accept_state for state in current_states)


def visualize_nfa(nfa):
    graph = nx.DiGraph()
    node_count = 0
    node_map = {}

    def add_state(state):
        nonlocal node_count
        if state not in node_map:
            node_map[state] = f"q{node_count}"
            node_count += 1
            if state == nfa.accept_state:
                graph.add_node(node_map[state], shape='doublecircle')
            else:
                graph.add_node(node_map[state])
        return node_map[state]

    queue = [nfa.start_state]
    visited = set()

    while queue:
        current_state = queue.pop(0)
        if current_state in visited:
            continue
        visited.add(current_state)

        current_node = add_state(current_state)

        for char, next_state in current_state.transitions:
            next_node = add_state(next_state)
            graph.add_edge(current_node, next_node, label=char if char is not None else "ε")
            if next_state not in visited:
                queue.append(next_state)

    pos = nx.spring_layout(graph)  # Alternative: try using graphviz_layout(graph)
    labels = nx.get_edge_attributes(graph, 'label')
    nx.draw(graph, pos, with_labels=True, node_size=500, node_color="skyblue", node_shape='o')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    plt.show()

def run_application():
    def validate_inputs():
        regex = regex_entry.get()

        if not regex:
            messagebox.showerror("Error", "Por favor, ingresa una expresión regular.")
            return

        try:
            postfix_regex = shunt(regex)
            nfa = compile_postfix(postfix_regex)

            results = []
            for test_string in test_strings_list:
                result = simulate_nfa(nfa, test_string)
                results.append((test_string, result))

            results_listbox.delete(0, tk.END)
            for string, result in results:
                results_listbox.insert(tk.END, f"'{string}': {'Aceptada' if result else 'Rechazada'}")

        except ValueError as ve:
            messagebox.showerror("Error de expresión regular", str(ve))
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error: {e}")

    def add_string():
        new_string = test_entry.get()
        if new_string:
            test_strings_list.append(new_string)
            strings_listbox.insert(tk.END, new_string)
            test_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa una cadena antes de agregar.")

    def clear_all():
        regex_entry.delete(0, tk.END)
        test_entry.delete(0, tk.END)
        test_strings_list.clear()
        strings_listbox.delete(0, tk.END)
        results_listbox.delete(0, tk.END)

    def generate_automata():
        regex = regex_entry.get()

        if not regex:
            messagebox.showerror("Error", "Por favor, ingresa una expresión regular.")
            return
        try:
            postfix_regex = shunt(regex)
            nfa = compile_postfix(postfix_regex)
            visualize_nfa(nfa)
        except ValueError as ve:
            messagebox.showerror("Error de expresión regular", str(ve))
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error: {e}")

    def center_window(window):
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f"{width}x{height}+{x}+{y}")

    window = tk.Tk()
    window.title("Validador de Expresiones Regulares")

    test_strings_list = []

    tk.Label(window, text="Expresión Regular:").grid(row=0, column=0, padx=5, pady=5)
    regex_entry = tk.Entry(window, width=40)
    regex_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(window, text="Cadena a Agregar:").grid(row=1, column=0, padx=5, pady=5)
    test_entry = tk.Entry(window, width=40)
    test_entry.grid(row=1, column=1, padx=5, pady=5)


    button_frame = tk.Frame(window)
    button_frame.grid(row=2, column=0, columnspan=2, pady=(10, 5))

    add_button = tk.Button(button_frame, text="Agregar Cadena", command=add_string, width=15, relief=tk.RAISED, bd=3)
    add_button.pack(side=tk.LEFT, padx=5)

    validate_button = tk.Button(button_frame, text="Validar Cadenas", command=validate_inputs, width=15, relief=tk.RAISED, bd=3)
    validate_button.pack(side=tk.LEFT, padx=5)

    generate_button = tk.Button(button_frame, text="Generar Autómata", command=generate_automata, width=15, relief=tk.RAISED, bd=3)
    generate_button.pack(side=tk.LEFT, padx=5)

    clear_button = tk.Button(button_frame, text="Limpiar", command=clear_all, width=15, relief=tk.RAISED, bd=3)
    clear_button.pack(side=tk.LEFT, padx=5)


    tk.Label(window, text="Cadenas Ingresadas:").grid(row=3, column=0, columnspan=2, pady=5)
    strings_listbox = tk.Listbox(window, height=6, width=60)
    strings_listbox.grid(row=4, column=0, columnspan=2, pady=5)

    tk.Label(window, text="Resultados:").grid(row=5, column=0, columnspan=2, pady=5)
    results_listbox = tk.Listbox(window, height=6, width=60)
    results_listbox.grid(row=6, column=0, columnspan=2, pady=5)

    center_window(window)

    window.mainloop()


if __name__ == "__main__":
    run_application()