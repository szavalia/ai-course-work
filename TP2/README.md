# TP2

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
        - [Parámetros generales](#parámetros-generales)
        - [Parámetros de cruza](#parámetros-de-cruza)
        - [Parámetros de mutación](#parámetros-de-mutación)
        - [Parámetros de selección](#parámetros-de-selección)
    - [Ejecución del proyecto](#ejecución-del-proyecto)
    - [Configuraciones ejemplo](#configuraciones-ejemplo)
- [Experimentos](#experimentos)
    - [Experimento 1](#experimento-1)
    - [Experimento 2](#experimento-2)
    - [Experimento 3](#experimento-3)
    - [Experimento 4](#experimento-4)

## Descripción

El proyecto fue desarrollado con Python, y consiste en encontrar una implementación de la resolución de un problema mediante un algoritmo genético. El problema consiste en simular la reacción de un reactivo binario frente a distintos valores de entrada, buscando obtener una función que aproxime correctamente los valores de este reactivo. Los valores de entrada son vectores de 3 componentes reales. La función en cuestión es de la siguiente forma (donde W es un vector de 1x3, w es una matrix de 2x3, w0 es un vector de 1x2 y ξ es un valor inicial):

![formula](https://render.githubusercontent.com/render/math?math={\color{gray}\%20F%28W%2Cw%2Cw_%7B0%7D%2C%20%5Cxi%20%29%20%3D%20g%28%20%5Csum_%7Bj%3D1%7D%5E2%20W_%7Bj%7Dg%28%20%5Csum_%7Bk%3D0%7D%5E2%20w_%7Bjk%7D%20%5Cxi%20_%7Bk%7D%20-w_%7B0j%7D%20%29-W_%7B0%7D%29})

siendo g una función de la forma:

![formula](https://render.githubusercontent.com/render/math?math={\color{gray}\g%28x%29%20%3D%20%5Cfrac%7Be%5E%7Bx%7D%7D%7B1%2Be%5E%7Bx%7D%7D})

Se puede definir por lo tanto una función de error de la forma (tomando el caso de 3 valores de entrada, donde ζ es un resultado asociado a un valor inicial ξ):

![formula](https://render.githubusercontent.com/render/math?math={\color{gray}\E%28W%2Cw%2Cw_%7B0%7D%29%20%3D%20%20%5Csum_%7Bk%3D1%7D%5E3%20%28%20%5Czeta%5E%7Bk%7D%20-%20F%28W%2Cw%2Cw_%7B0%7D%2C%20%5Cxi%20%5E%7Bk%7D%29%29%5E2%20})

El objetivo es obtener los valores de W w y w0 que minimizen el error para los datos de entrada, utilizando algoritmos genéticos con distintos métodos de mutación, selección y cruza.

## Requerimientos

- Python 3

## Ejecución
### Configuraciones iniciales

Una vez clonado el proyecto en su carpeta de preferencia, para configurar los parámetros iniciales se debe utilizar el archivo `config.json`. Este archivo posee una gran variedad de parámetros, que se discutirán en base a los distintos tipos de parámetros.

#### Parámetros generales

Estos parámetros hacen referencia a la ejecución en general. Los parámetros son:
- "initial_values": se compone de una matriz donde se especifican los valores de entrada (siempre vectores de 3 componentes).
- "initial_results": es un vector con el valor del reactivo para cada uno de los valores de entrada (1 o 0).
- "limit_first_generation": número real utilizado como límite para la generación de los primeros individuos de la población. Las componentes de estos individuos se obtendrán como un random entre -value y +value.
-"population_size": cantidad de individuos de la población a utilizar en el algoritmo.
- "generations": criterio de corte por cantidad de generaciones a utilizar. Este criterio es el default. En caso de no estar el campo, o de ser un número menor a la cantidad de generaciones mínimas permitidas (500), se toma este valor como criterio de corte.
- "error_threshold": criterio de corte de error. El programa finalizará al encontrar un valor de error inferior al criterio o al superar el límite de generaciones. Es un parámetro opcional, en caso de no indicarse se usa como criterio el default.
- "output_path": path + nombre de archivo utilizado como output. No especificar la extensión, por default es un archivo csv.

#### Parámetros de cruza

Para espeficiar las opciones del método de cruza, se utiliza el siguiente formato:
- "crossbreeding": objeto que contiene las propiedades:
    - "method": método de cruza a utilizar. Las opciones son
        - "simple": método de cruza simple.
        - "multiple": método de cruza múltiple.
        - "uniform": método de cruza uniforme.
    - "multiple_point_n": parámetro para especificar la cantidad de puntos a tomar en método de cruza múltiple. En caso de ser otro tipo de cruza, el campo es ignorado.

#### Parámetros de mutación
Para espeficiar las opciones del método de mutación, se utiliza el siguiente formato:
- "mutation": objeto que contiene las propiedades:
    - "method": método de mutación a utilizar. Las opciones son
        - "normal": método de mutación con distribución normal
        - "uniform": método de mutación con distribución uniforme
    - "probability": probabilidad de mutación. Usada en ambos métodos.
    - "sigma": parámetro utilizado para método de mutación con distribución normal, a realizarse en el entorno (0,sigma).  Si el método es uniforme, este parámetro es ignorado
    - "a": parámetro utilizado para método de mutación con distribución uniforme, a realizarse en el entorno (-a,a). Si el método es normal, este parámetro es ignorado

#### Parámetros de selección
Para espeficiar las opciones del método de selección, se utiliza el siguiente formato:
- "selection": objeto que contiene las propiedades:
    - "method": método de selección a utilizar. Las opciones son
        - "elite": método de selección elite
        - "roulette": método de selección de la ruleta
        - "rank":  método de selección de ranking
        - "truncation": método de selección de truncamiento
        - "tournament_wr": método de selección de torneo con reemplazo
        - "tournament_nr": método de selección de torneo sin reemplazo
        - "boltzmann": método de selección de boltzmann
    - "truncation_k": número de valores a descartar para método de truncamiento. Si el método de selección es otro, este parámetro es ignorado.
    - "tournament_threshold": valor de umbral para método de torneo. Si el método de selección es otro, este parámetro es ignorado.
    - "boltzmann_k": valor de k para método de boltzmann. Si el método de selección es otro, este parámetro es ignorado.
    - "boltzmann_tc": valor de temperatura critica para método de boltzmann. Si el método de selección es otro, este parámetro es ignorado.
    - "boltzmann_t0": valor de temperatura inicial para método de boltzmann. Si el método de selección es otro, este parámetro es ignorado.

### Ejecución del proyecto

Para correr el proyecto, una vez posicionado sobre el directorio base de este y habiendo configurado los parámetros iniciales, basta con ejecutar:

```bash
$ python3 main.py
```
Al finalizar su ejecución, el programa mostrará los parámetros iniciales de ejecución, así como también los valores de W, w y w0 de la mejor solución y los valores de la función F para cada valor inicial. Además, se muestra el valor del error para la solución, la cantidad de generaciones realizadas y el tiempo de procesamiento. Por último se genera un archivo csv con el nombre indicado en `config.json` donde se dejan los valores de fitness mínimo y máximo respectivamente para cada generación. 

### Configuraciones ejemplo

En todos los ejemplos se utilizaran los mismos 3 valores iniciales, pero pueden usarse más o ser diferentes.

Si por ejemplo busco resolver el problema con método de selección elite, cruza simple y mutación normal usando como criterio de corte 700 generaciones, con 50 miembros en su población, se puede configurar el archivo `config.json` como:
```json
{
    "initial_values": [[4.4793,-4.0765,-4.0765],[-4.1793,-4.9218,1.7664],[-3.9429,-0.7689,4.883]],
    "initial_results": [0,1,1],
    "limit_first_generation": 10,
    "population_size": 50,
    "generations": 700,
    "output_path": "resources/output",
    "crossbreeding": {
        "method": "simple"
    },
    "mutation": {
        "method": "normal",
        "probability": 0.05,
        "sigma": 2
    },
    "selection": {
        "method": "elite"
    }
}
```
Si buscase resolver el mismo problema pero con mutación uniforme, usando ahora un método de selección de boltzmann y un criterio de corte por error de 1e-20, se puede configurar el archivo `config.json` como: 
```json
{
    "initial_values": [[4.4793,-4.0765,-4.0765],[-4.1793,-4.9218,1.7664],[-3.9429,-0.7689,4.883]],
    "initial_results": [0,1,1],
    "limit_first_generation": 10,
    "population_size": 50,
    "error_threshold": 1e-20,
    "output_path": "resources/output",
    "crossbreeding": {
        "method": "simple"
    },
    "mutation": {
        "method": "uniform",
        "probability": 0.05,
        "a": 2
    },
    "selection": {
        "method": "boltzmann",
        "boltzmann_k": 0.1,
        "boltzmann_t0": 70,
        "boltzmann_tc": 10
    }
}
```
Por último se puede querer utilizar el método de cruza múltiple con 2 puntos en vez del simple, y utilizar el método de selección de torneo sin reemplazo con umbral de 0.75, agregando además un criterio de corte por generaciones de 1000, se puede configurar el archivo `config.json` como:
```json
{
    "initial_values": [[4.4793,-4.0765,-4.0765],[-4.1793,-4.9218,1.7664],[-3.9429,-0.7689,4.883]],
    "initial_results": [0,1,1],
    "limit_first_generation": 10,
    "population_size": 50,
    "generations": 1000,
    "error_threshold": 1e-20,
    "output_path": "resources/output",
    "crossbreeding": {
        "method": "multiple",
        "multiple_point_n": 2
    },
    "mutation": {
        "method": "uniform",
        "probability": 0.8,
        "a": 2
    },
    "selection": {
       "method": "tournament_nr",
       "tournament_threshold": 0.75
    }
}
```

## Experimentos

Como adicional, para analizar diferentes configuraciones decidimos realizar una serie de experimentos que nos permitiesen obtener los datos necesarios. Todos estos experimentos utilizan nuestro algoritmo con parámetros distintos para generar diferentes corridas. Los experimentos siempre se dividen en dos partes: recopilar máximo y mínimo fitness en cada generación y recopilar cantidad de generaciones hasta llegar a cierto error. Los ejecutables de tipo experimentn_fitness.py permiten recopilar lo primero, mientras que los ejecutables de tipo experimentn_gens.py lo segundo. En ambos casos se devuelve un archivo csv con la información requerida pero con formato variable de acuerdo al experimento. En ambos casos los valores retornados se obtienen mediante promediar varias corridas del algoritmo, cantidad indicada por el usuario. Para el caso de los fitness, se promedia el fitness por paso entre las corridas realizadas y para el caso de las generaciones, se promedian las generaciones resultantes.
En todos los experimentos se toma como criterio de corte 1000 generaciones y 50 individuos por generación, con individuos iniciales de la población cuyos cromosomas son generados con distribución uniforme entre [-10,10].
A continuación se detalla cómo usar cada uno de estos para generar el dataset que utilizamos para análisis. 

### Experimento 1

El experimento 1 consiste en un análisis de los métodos de selección para intentar encontrar las variantes óptimas de estos y luego compararlos entre sí para definir cuál es el más apto. Para esto se evalúa a todos los métodos de selección utilizando cruza simple y mutación uniforme pero con distintos valores de probabilidad y a, para evaluar casos de variabilidad baja media y alta.
A continuación se detallan algunos valores utilizados en este experimento:
- mutación: se toman como probabilidad y a respectivamente los valores (0.05, 0.1), (0.1, 1), (0.2, 2)
- umbral de torneos con y sin reemplazo: se utilizan los valores 0.5, 0.65, 0.80
- k de truncación: se utilizan los valores 10,25,50
- parámetros de boltzmann: se utilizan como Tc, T0 y k respectivamente los valores (10,70,0.01),(10,140,0.01),(10,70,0.05),(10,140,0.05)
- errores: en experiment1_gens.py se utilizan los errores 1e-1,1e-10,1e-50 como criterio de corte

Para obtener los csv resultantes del experimento, se debe utilizar el siguiente comando:

```bash
$ python3 experiment1_fitness.py [total_runs] [dataset_type] [output_path] [csv_path]
```
```bash
$ python3 experiment1_gens.py [total_runs] [dataset_type] [output_path] [csv_path]
```

donde: 
- total_runs es la cantidad de ejecuciones a realizar del algoritmo por cada combinación de parámetros
- dataset_type puede tomar los valores "simple" (datos de los métodos elite, ruleta y ranking), "complex" (datos de los métodos torneo y truncamiento) y "boltzmann" (datos del método de boltzmann). Esto varía el formato del csv resultante
- output_path es el path utilizado para la generación de archivos del programa (mencionado previamente en el `config.json`)
- csv_path es nombre del archivo para recolección de datos final

### Experimento 2

El experimento 2 consiste en un análisis de los métodos de cruza para intentar encontrar las variantes óptimas de estos y luego compararlos entre si para definir cuál es el más apto. Para esto se evalúa a todos los métodos utilizando los mismos criterios de mutación del experimento anterior, y como metodo de selección el óptimo elegido en base al experimento anterior.
A continuacion se detallan algunos valores utilizados en este experimento:
- mutación: mismos valores que experimento 1
- selección: torneo sin reemplazo con umbral 0.8
- cruza múltiple: se utiliza como puntos para la cruza múltiple los valores 2 4 y 6
- errores: mismos valores utilizados para el experimento 1

Para obtener los csv resultantes del experimento, se debe utilizar el siguiente comando:

```bash
$ python3 experiment2_fitness.py [total_runs] [dataset_type] [output_path] [csv_path]
```
```bash
$ python3 experiment2_gens.py [total_runs] [dataset_type] [output_path] [csv_path]
```

donde: 
- total_runs es la cantidad de ejecuciones a realizar del algoritmo por cada combinación de parametros
- dataset_type puede tomar los valores "simple" (datos de los métodos de cruza simple y uniforme), "complex" (datos del método de cruza múltiple).  Esto varía el formato del csv resultante
- output_path es el path utilizado para la generación de archivos del programa (mencionado previamente en el `config.json`)
- csv_path es nombre del archivo para recolección de datos final
### Experimento 3

El experimento 3 consiste en un análisis de los métodos de mutación para intentar encontrar las variantes óptimas de estos y luego compararlos entre sí para definir cual es el más apto. En este experimento se varían los valores de a y sigma. Para esto se evalúa a todos los métodos utilizando como método de selección el óptimo elegido en base al experimento 1 y como método de cruza, aquel óptimo elegido en base al experimento 2.
A continuación se detallan algunos valores utilizados en este experimento:
- selección: torneo sin reemplazo con umbral 0.8
- cruza: cruza uniforme
- probabilidad: el valor utilizado es 0.1
- valores de difusión: se tomaron como valores de a y sigma los valores (0.1, 0.05), (1,0.5) ,(2,1), (4,2). Se mantiene la relación sigma = a/2 para mantener la misma amplitud entre métodos
- errores: mismos valores utilizados para el experimento 1

Para obtener los csv resultantes del experimento, se debe utilizar el siguiente comando:

```bash
$ python3 experiment3_fitness.py [total_runs] [output_path] [csv_path]
```
```bash
$ python3 experiment3_gens.py [total_runs] [output_path] [csv_path]
```

donde: 
- total_runs es la cantidad de ejecuciones a realizar del algoritmo por cada combinación de parámetros
- output_path es el path utilizado para la generación de archivos del programa (mencionado previamente en el `config.json`)
- csv_path es nombre del archivo para recolección de datos final

### Experimento 4

El experimento 4 consiste en un análisis de los métodos de mutación para intentar encontrar las variantes óptimas de estos y luego compararlos entre sí para definir cuál es el más apto. En este experimento se varía la probabilidad de mutación. Para esto se evalúa a todos los métodos utilizando como método de selección el óptimo elegido en base al experimento 1 y como método de cruza, aquel óptimo elegido en base al experimento 2.
A continuacion se detallan algunos valores utilizados en este experimento:
- selección: torneo sin reemplazo con umbral 0.8
- cruza: cruza uniforme
- valores de probabilidad: se tomaron como valores de probabilidad de mutación (para ambos métodos) los valores 0.05,0.1,0.2,0.5
- valores de difusion: se tomaron como valores de a y sigma los valores 4 y 2 respectivamente.Estos valores fueron definidos como óptimos en el experimento anterior
- errores: mismos valores utilizados para el experimento 1

Para obtener los csv resultantes del experimento, se debe utilizar el siguiente comando:

```bash
$ python3 experiment4_fitness.py [total_runs] [output_path] [csv_path]
```
```bash
$ python3 experiment4_gens.py [total_runs] [output_path] [csv_path]
```

donde: 
- total_runs es la cantidad de ejecuciones a realizar del algoritmo por cada combinación de parámetros
- output_path es el path utilizado para la generación de archivos del programa (mencionado previamente en el `config.json`)
- csv_path es nombre del archivo para recolección de datos final
