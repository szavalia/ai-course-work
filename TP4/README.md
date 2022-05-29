# TP4

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

El proyecto fue desarrollado con Python, y esta centrado en la implementacion de algoritmos de aprendizaje no supervisado para resolver diversos tipos de problemas. En concreto se realiza una implementacion de una red de Kohonen (problemas de agrupacion), una red de Hopfield discreta (problema de asociacion) y una red que utiliza la regla de aprendizaje de Oja. Los problemas a resolver son:
- Red de Kohonen: clasificacion de paises de Europa en base a sus caracteristicas socioeconomicas, utilizando el dataset `europe.csv` presente en la carpeta `resources`
- Red de Hopfield: dado patrones que representan letras del alfabeto de 5x5 pixeles, asociacion de variantes de los patrones utilizados con ruido con el patron original 
- Red con aprendizaje de Oja: utilizando el mismo dataset que la red de Kohonen, obtener la primer componente principal para hacer analisis

## Requerimientos

- Python 3

## Ejecución
### Configuraciones iniciales

Una vez clonado el proyecto en su carpeta de preferencia, para configurar los parámetros iniciales se debe utilizar el archivo `config.json`. Este archivo posee una cierta variedad de parámetros, que se discutiran a continuacion.

#### Parámetros
- "method": metodo a utilizar para resolver un problema especifico. Su valor puede ser: 
    - "kohonen": utiliza la red de Kohonen
    - "hopfield": utiliza la red de Hopfield
    - "oja": utiliza la red con aprendizaje de Oja
- "kohonen_props": objeto con propiedades a utilizar por la red de Kohonen para resolver el problema indicado. Si el campo "method" no tiene el valor asociado, este campo es ignorado. Sus campos son:
    - "dataset_path": path al archivo `europe.csv`
    - "eta": tasa de aprendizaje inicial
    - "k": dimension de la red a utilizar (una grilla rectangular de kxk neuronas)
    - "r": radio inicial
    - "epochs": limite de epocas a iterar
- "hopfield_props": objeto con propiedades a utilizar por la red de Hopfield para resolver el problema indicado. Si el campo "method" no tiene el valor asociado, este campo es ignorado. Sus campos son:
    - "patterns": vector de letras a utilizar como patrones almacenados.
    - "noise_prob": probabilidad de ruido
- "oja_props": objeto con propiedades a utilizar por la red con aprendizaje de Oja para resolver el problema indicado. Si el campo "method" no tiene el valor asociado, este campo es ignorado. Sus campos son:
    - "dataset_path": path al archivo `europe.csv`
    - "eta": tasa de aprendizaje
    - "epochs": limite de epocas a iterar

### Ejecución del proyecto

Para correr el proyecto, una vez posicionado sobre el directorio base de este y habiendo configurado los parámetros iniciales, basta con ejecutar:

```bash
$ python3 main.py
```
Al finalizar su ejecución, el programa mostrará los parámetros iniciales de ejecución, y creara una serie de archivos distintos en base al problema requerido. Para el caso de la red de Kohonen, se crean los archivos `classifications.csv` (que indica en que neurona se encuentra cada valor de entrada, pensado como ubicacion en grilla en funcion de su fila y columna), `u_matrix.csv` (valores de la matriz U asociada) y `weights_matrix.csv` (los pesos correspondientes a las neuronas de la red). Para el caso de la red de Hopfield, se crean los archivos `hopfield_n.txt` (donde n es una de las letras de los patrones usados, muestra los pasos que hace la red desde el patron inicial con ruido hasta el patron de convergencia), `energies.csv` (energia en cada iteracion para cada uno de los patrones ruidosos) y `hopfield_results.csv` (para cada patron ruidoso, se muestra el porcentaje de pixeles correctos del patron de convergencia comparando contra el patron original utilizado). Para la red con aprendizaje de Oja se generan los archivos `loadings.csv` (pesos finales de la red) y `components.csv` (valores de la primera componente para cada dato perteneciente al dataset de entrada)

Ademas para el caso de la red de Hopfield, se adjunta un clasificador de combinaciones de patrones de 4 letras en base a su "ortogonalidad". Este revise dos parametros: la cantidad de combinaciones a listar y el orden del listado (siendo false si es orden de menor a mayor y true viceversa). Se ejecuta como:

```bash
$ python3 get_patterns.py 15 true
```

### Configuraciones ejemplo

Si por ejemplo busco usar la red de Hopfield con los patrones "K","N","S","V" para asociar patrones ruidosos de estos con probabilidad de ruido 0.2 la configuracion del archivo es:

```json
{
    "method" : "hopfield",
    "hopfield_props": {
        "patterns": ["K", "N", "S", "V"],
        "noise_prob": 0.2
    }
}
```

Si ahora busco usar una red de Kohonen de 4x4 neuronas, con tasa de aprendizaje 0.1, radio inicial 4 y que itere por 1001 epocas la configuracion del archivo es: 

```json
{
    "method" : "kohonen",
    "kohonen_props":{
        "dataset_path" : "resources/europe.csv",
        "eta" : 0.1,
        "k" : 4,
        "r" : 4,
        "epochs" : 1001
    }
}
```

Por ultimo, para utilizar la red con aprendizaje de Oja con tasa de aprendizaje 0.01 y que itere por 1000 epocas la configuracion del archivo es:

```json
{
    "method" : "oja",
    "oja_props":{
        "dataset_path" : "resources/europe.csv",
        "eta" : 0.01,
        "epochs": 1000
    }
}
```