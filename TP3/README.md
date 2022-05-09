# TP3

## 72.27 - Sistemas de Inteligencia Artificial - 2º cuatrimestre 2022

### Instituto Tecnológico de Buenos Aires (ITBA)

## Autores

- [Sicardi, Julián Nicolas](https://github.com/Jsicardi) - Legajo 60347
- [Quintairos, Juan Ignacio](https://github.com/juaniq99) - Legajo 59715
- [Zavalia Pángaro, Salustiano Jose](https://github.com/szavalia) - Legajo 60312

## Índice
- [Autores](#autores)
- [Índice](#índice)
- [Descripción](#descripción)
- [Ejecución](#ejecución)
    - [Configuraciones iniciales](#configuraciones-iniciales)
        - [Parámetros](#parámetros)
    - [Ejecución del proyecto](#ejecución-del-proyecto)
    - [Configuraciones ejemplo](#configuraciones-ejemplo)

## Descripción

El proyecto fue desarrollado con Python, y esta centrado en la implementacion del algoritmo del perceptron simple (en sus variantes escalon, lineal y no lineal) y multicapa. El objetivo es el uso de estos perceptrones para la resolucion de problemas especificos. Los problemas a resolver por los perceptrones son:
- Perceptron escalon:
    - XOR
    - AND
- Perceptron lineal y no lineal:
    - Aproximacion de funcion en base a datasets `training_ej2.txt` y `zeta_ej2.txt`
- Perceptron multicapa:
    - XOR
    - Identificar si un numero es par tomando su imagen del dataset `training_ej3.txt` (imagenes de 5x7 pixeles)
    - Identificar un numero tomando su imagen del dataset `training_ej3.txt` (imagenes de 5x7 pixeles)

## Requerimientos

- Python 3

## Ejecución
### Configuraciones iniciales

Una vez clonado el proyecto en su carpeta de preferencia, para configurar los parámetros iniciales se debe utilizar el archivo `config.json`. Este archivo posee una cierta variedad de parámetros, que se discutiran a continuacion.

#### Parámetros
- "perceptron_type": tipo de perceptron a utilizar : 
    - "step": utiliza el perceptron simple escalon
    - "linear": utiliza el perceptron simple lineal
    - "non_linear": utiliza el perceptron simple no lineal con la sigmoidea especificada (ver "sigmoid_type")
    - "multilayer": utiliza el perceptron multicapa con las capas especificadas (ver "hidden_layers") y la sigmoidea especificada (ver "sigmoid_type")
- "hidden_layers": vector donde cada posicion especifica la cantidad de neuronas por capa (ejemplo [2,3] representa una red con 2 capas ocultas donde la primera tiene 2 neuronas y la segunda 3). La capa da salida queda definida en base al problema a resolver (ver "problem"). En caso de no utilizarse el perceptron multicapa, este parametro es ignorado
- "entry_file": path del archivo de dataset de entrada para problemas que lo requieran (ver "problem")
- "output_file": path del archivo de dataset de salida para problemas que lo requieran (ver "problem")
- "problem": problema a resolver por el perceptron:
    - "AND": problema del and logico (usar con tipo "step")
    - "XOR": problema del xor logico (usar con tipos "step" y "multilayer")
    - "odd_number": problema de identificar si un numero es par o impar (usar con tipo "multilayer")
    - "numbers": problema de identificar si un numero es un digito (usar con tipo "multilayer")
- "learning_rate": tasa de aprendizaje a utilizar por perceptron
- "max_epochs": epocas maximas a utilizar como criterio de corte por perceptron. De no especificarse se utilizan 100
- "min_error": error a utilizar como criterio de corte. De no especificarse se toma 0 (corte por epocas maximas)
- "sigmoid_type": funcion sigmoidea a utilizar (usar con tipos "multilayer" y "non_linear"):
    - "tanh": tangente hiperbolica
    - "logistic": funcion logistica
- "beta": parametro beta utilizado en funciones sigmoideas
- "alpha": parametro utilizado para constante de momentum
- "cross_validate": uso de cross validation para resolucion de problema
- "test_proportion": en caso de usar cross_validate, proporcion del conjunto a utilizar para testeo
- "softmax": uso de funcion softmax en capa de salidas (usar con tipo "multilayer")

### Ejecución del proyecto

Para correr el proyecto, una vez posicionado sobre el directorio base de este y habiendo configurado los parámetros iniciales, basta con ejecutar:

```bash
$ python3 main.py
```
Al finalizar su ejecución, el programa mostrará los parámetros iniciales de ejecución, asi como tambien el error en entrenamiento y las epocas iteradas. En caso que se use cross validation, se muestra el error de entrenamiento y el error de testeo correspondiente a los pesos optimos hallados.

### Configuraciones ejemplo

Si por ejemplo busco resolver el problema del XOR logico utilizando el perceptron simple escalon, usando como tasa de aprendizaje 0.1, con cota de error 1e-2 y 500 epocas como corte el archivo queda de la forma:

```json
{
    "perceptron_type" : "step",
    "problem": "XOR",
    "learning_rate" : 0.1,
    "max_epochs" : 500,
    "min_error": 1e-2,
}
```

Si ahora busco resolver el problema de numeros pares utilizando un perceptron multicapa usando dos capas ocultas (la primera con 2 neuronas y la segunda con 3), usando la misma tasa de aprendizaje y la cota de error del ejemplo anterior pero utilizando ahora 1000 epocas y usando cross validation con proporcion de 20% de testeo y 80% de entrenamiento. Ademas busco usar la funcion tangente hiperbolica con beta de 0.8. El archivo queda de la forma: 

```json
{
    "perceptron_type" : "multilayer",
    "hidden_layers": [2,3],
    "entry_file": "resources/training_ej3.txt",
    "problem": "odd_number",
    "learning_rate" : 0.1,
    "max_epochs" : 1000,
    "min_error": 1e-2,
    "sigmoid_type" : "tanh",
    "beta": 0.8,
    "cross_validate":"True",
    "test_proportion": 0.2,
}
```

Si quisiese resolver el mismo problema pero ahora utilizando momentum con alpha 0.8, basta con cambiar el archivo de la siguiente forma:

```json
{
    "perceptron_type" : "multilayer",
    "hidden_layers": [2,3],
    "entry_file": "resources/training_ej3.txt",
    "problem": "odd_number",
    "learning_rate" : 0.1,
    "max_epochs" : 1000,
    "min_error": 1e-2,
    "sigmoid_type" : "tanh",
    "beta": 0.8,
    "cross_validate":"True",
    "test_proportion": 0.2,
    "alpha": 0.8
}
```