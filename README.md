# Actividad_2.1

### Caso 1: Memorizar una Expresión Lógica con Perceptrón y Adaline

![alt text](https://www.planttext.com/api/plantuml/png/xL9B2W8n3DtFAR9KT2xWGlG6tg34JXm3DLFIZ1_4krkbYYCA7i0kIlEIzv8-iaY6QlqkL3vWIh0YzHHDEu5p1VdKS21kjvPcWAfuAk2QCIERqA7TaGaunyBct4ZwNNx6_aPXiN79epVUez7eaRlBZOSYVMnoYIijXwLJ8DLE2s4AWL25fNMQAGLzD3D5bdTw_cbBB_4dWTmaTdux73qgDUpjo-INgdYtR32mqD-uturxMRUwdZyTd04TZQH9rIBVj-sy0W00)

#### Clase Perceptrón:

- **Método `__init__(self, num_inputs)`**: Inicializa el Perceptrón con pesos aleatorios y un sesgo.
- **Método `activate(self, inputs)`**: Calcula la activación del Perceptrón dados los pesos y las entradas.
- **Método `update_weights(self, inputs, error, learning_rate)`**: Actualiza los pesos del Perceptrón en función del error y la tasa de aprendizaje.
- **Método `train(self, inputs, targets, learning_rate, epochs)`**: Entrena el Perceptrón utilizando el algoritmo de aprendizaje de regla delta.
- **Método `predict(self, inputs)`**: Realiza una predicción utilizando el Perceptrón entrenado.

#### Clase Adaline:

- **Método `__init__(self, num_inputs)`**: Inicializa Adaline con pesos aleatorios y un sesgo.
- **Método `activate(self, inputs)`**: Calcula la activación de Adaline dados los pesos y las entradas.
- **Método `update_weights(self, inputs, error, learning_rate)`**: Actualiza los pesos de Adaline en función del error y la tasa de aprendizaje.
- **Método `train(self, inputs, targets, learning_rate, epochs)`**: Entrena Adaline utilizando el algoritmo de aprendizaje de regla delta mejorado.
- **Método `predict(self, inputs)`**: Realiza una predicción utilizando Adaline entrenado.

#### Función `generate_logical_expression_data()`:

- **Genera un conjunto de datos de una expresión lógica**: Crea un conjunto de datos de entrada y salida basado en una expresión lógica específica con cuatro variables.

#### Función `test_model()`:

- **Prueba el modelo**: Utiliza un conjunto de datos de prueba para evaluar el rendimiento del Perceptrón o Adaline entrenado.

### Caso 2: Predecir el Mapa Logístico con Adaline


![alt text](https://www.planttext.com/api/plantuml/png/TL3D2i8m3BxtAS9Ecsu7hnv4dwJ4hRf0pKgQAIA-kztea87c5BxVa6DK51rlthGUOuHJXvxOmSj0cWOUZgwznZsW23upU2PCoCKFg3Eo1Mk9IQqjURobDOoJXLYhp6EhT4TrvSBDSTKwP0nTajXSkPRMu4G6oOOQl4DXugkLPCdeKgQ2n6L0LIVy3VXbIR5XQFlriK5SHwt-kVLjpFAaObT0qnoWs1ImXnuZBANcwBYRlle1)

#### Clase Adaline:

- **Método `__init__(self, num_features)`**: Inicializa Adaline con pesos aleatorios.
- **Método `activate(self, inputs)`**: Calcula la activación de Adaline dados los pesos y las entradas.
- **Método `update_weights(self, inputs, error, learning_rate)`**: Actualiza los pesos de Adaline en función del error y la tasa de aprendizaje.
- **Método `train(self, patterns, learning_rate, epochs)`**: Entrena Adaline utilizando un conjunto de patrones.
- **Método `predict(self, inputs)`**: Realiza una predicción utilizando Adaline entrenado.

#### Función `generate_logistic_map_data()`:

- **Genera un conjunto de datos del mapa logístico**: Crea un conjunto de datos de entrenamiento y prueba basado en el mapa logístico.

#### Función `create_patterns()`:

- **Crea patrones para el entrenamiento y prueba**: Genera patrones de entrada y salida para entrenar y probar Adaline en la predicción del mapa logístico.

#### Función `test_adaline()`:

- **Prueba Adaline**: Utiliza un conjunto de datos de prueba para evaluar el rendimiento de Adaline en la predicción del siguiente término del mapa logístico.
