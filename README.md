# Validador de Expresiones Regulares con Generador de Autómatas

Este proyecto es una aplicación gráfica que permite validar cadenas de texto contra expresiones regulares y visualizar el autómata finito determinista (DFA) generado a partir de estas expresiones. Es ideal para aprender sobre teoría de autómatas y expresiones regulares.

## Tabla de Contenidos

1. Manual de Usuario
    - Requisitos
    - Instalación
    - Uso
2. Documentación Técnica
    - Arquitectura del Código
    - Diseño del Código
    - Funcionalidades Clave

## Manual de Usuario

### Requisitos

**Python:** 
    3.7 o superior

#### **Bibliotecas necesarias:**
    Instalar usando pip: pip install matplotlib networkx

### Instalación

**Clona el repositorio o descarga los archivos del proyecto:**
    git clone https://github.com/anrumo03/ProyectoTLF.git

Asegúrate de tener todas las dependencias instaladas (ver sección "Requisitos").

#### **Ejecuta el archivo principal:**
    python proyecto.py

### Uso

**Inicio de la Aplicación:**
    Al ejecutar el programa, se abrirá una interfaz gráfica.

**Agregar una Expresión Regular:**
    Ingresa una expresión regular en el campo superior de la ventana.

**Agregar Cadenas:**
    Introduce una cadena en el campo "Cadena a Agregar" y presiona el botón "Agregar Cadena".

**Validar Cadenas:**
    Haz clic en "Validar Cadenas" para ver cuáles cadenas son aceptadas por la expresión regular.

**Visualizar el Autómata:**
    Presiona el botón "Generar Autómata" para ver una representación gráfica del DFA generado.

**Limpiar Todo:**
    Utiliza el botón "Limpiar" para reiniciar la entrada de datos.

## Documentación Técnica

### Arquitectura del Código

El programa está dividido en las siguientes partes principales:

#### **Clases Base:**
- **State:** Representa un estado en el autómata. Contiene una lista de transiciones (transitions) que son tuplas (carácter, estado_siguiente).

- **NFA:** Representa un autómata finito no determinista (NFA), definido por un estado inicial y un estado de aceptación.

#### **Módulos Principales:**
- **Shunting Yard:** Convierte expresiones regulares infijas a notación postfija para simplificar la construcción del autómata.

- **Compilador de NFA:** Construye un NFA a partir de una expresión en notación postfija.

- **Simulador de NFA:** Comprueba si una cadena de entrada es aceptada por un NFA.

- **Conversor NFA a DFA:** Convierte un NFA en un DFA utilizando el algoritmo de conjuntos epsilon-closure.

- **Visualizador:** Genera una visualización gráfica del DFA utilizando NetworkX y Matplotlib.

- **Interfaz Gráfica:**
    Desarrollada con Tkinter para proporcionar una experiencia de usuario sencilla e interactiva.

### Diseño del Código

El diseño sigue una estructura modular para facilitar su comprensión y mantenimiento:

#### **Separación de responsabilidades:**
Cada módulo y función tiene una responsabilidad única:

- shunt() maneja la conversión infijo → postfijo.
- compile_postfix() crea un NFA.
- simulate_nfa() realiza simulaciones sobre el NFA.
- nfa_to_dfa() realiza la conversión a DFA.
- visualize_dfa() genera el grafo del autómata.

**Uso de POO:**
    Las clases State y NFA encapsulan el comportamiento y la estructura de los autómatas.

**Interfaz gráfica (GUI):**
    El código relacionado con Tkinter se aísla en la función run_application(), lo que permite mantener una separación lógica entre la lógica del núcleo y la interfaz de usuario.

### Funcionalidades Clave

**Conversión de Expresiones Regulares a Postfijo:**
    Utiliza el algoritmo Shunting Yard para manejar prioridades de operadores (*, |, +, etc.) y agregar concatenaciones explícitas (.).

**Construcción de NFA:**
    Soporta operadores estándar (*, +, |, ?, y concatenación). Implementa transiciones epsilon para simplificar el diseño.

**Simulación de NFA:**
    Permite verificar si una cadena es aceptada por la expresión regular definida.

**Conversión de NFA a DFA:**
    Genera un DFA equivalente, eliminando ambigüedades del NFA.

**Visualización del DFA:**
    Utiliza NetworkX y Matplotlib para mostrar gráficamente el autómata, destacando estados de aceptación.