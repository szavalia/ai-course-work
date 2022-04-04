# TP2

## 72.27 - Sistemas de Inteligencia Artificial - 2º cuatrimestre 2022

### Instituto Tecnológico de Buenos Aires (ITBA)

## Autores

- [Sicardi, Julián Nicolas](https://github.com/Jsicardi) - Legajo 60347
- [Quintairos, Juan Ignacio](https://github.com/juaniq99) - Legajo 59715
- [Zavalia Pángaro, Salustiano Jose](https://github.com/szavalia) - Legajo 60312

## Indice
- [Autores](#autores)
- [Indice](#indice)
- [Descripción](#descripcion)
- [Ejecucion](#ejecucion)
    - [Configuraciones iniciales](#configuraciones-iniciales)
        - [Parametros generales](#parametros-generales)
        - [Parametros de cruza](#parametros-de-cruza)
        - [Parametros de mutacion](#parametros-de-mutacion)
        - [Parametros de seleccion](#parametros-de-seleccion)
    - [Ejecucion del proyecto](#ejecucion-del-proyecto)
    - [Configuraciones ejemplo](#configuraciones-ejemplo)



## Descripcion

El proyecto fue desarrollado con Python, y consiste en encontrar una implementacion de la resolucion de un problema mediante un algoritmo genetico. El problema consiste en simular la reaccion de un reactivo binario frente a distintos valores de entrada, buscando obtener una funcion que aproxime correctamente los valores de este reactivo. Los valores de entrada son vectores de 3 componentes reales.La funcion en cuestion es de la forma:

![formula](https://render.githubusercontent.com/render/math?math={\color{white}\F%28W%2Cw%2Cw_%7B0%7D%2C%5Cvarepsilon_%7B%20k%7D%29%20%3D%20g%28%5Csum_%7Bj%3D1%7D%5E%7B2%7D%20W_%7Bj%7D%20g%28%5Csum_%7Bk%3D0%7D%5E%7B2%7D%20w_%7Bjk%7D%5Cvarepsilon_%7B%20k%7D%20-%20w_%7B0j%7D%29-W_%7B0%7D%29}#gh-dark-mode-only")
![formula](https://render.githubusercontent.com/render/math?math={F%28W%2Cw%2Cw_%7B0%7D%2C%5Cvarepsilon_%7B%20k%7D%29%20%3D%20g%28%5Csum_%7Bj%3D1%7D%5E%7B2%7D%20W_%7Bj%7D%20g%28%5Csum_%7Bk%3D0%7D%5E%7B2%7D%20w_%7Bjk%7D%5Cvarepsilon_%7B%20k%7D%20-%20w_%7B0j%7D%29-W_%7B0%7D%29}#gh-light-mode-only")

siendo g una funcion de la forma:

![formula](https://render.githubusercontent.com/render/math?math={\color{white}\g%28x%29%20%3D%20%20%20%5Cfrac%7Be%5E%7Bx%7D%7D%7B1%20%2B%20e%5E%7Bx%7D%7D%20%20%20}#gh-dark-mode-only")
![formula](https://render.githubusercontent.com/render/math?math={g%28x%29%20%3D%20%20%20%5Cfrac%7Be%5E%7Bx%7D%7D%7B1%20%2B%20e%5E%7Bx%7D%7D%20%20%20}#gh-light-mode-only")

Se puede definir por lo tanto una funcion de error de la forma (tomando el caso de 3 valores de entrada):

![formula](https://render.githubusercontent.com/render/math?math={\color{white}\E%28W%2Cw%2Cw_%7B0%7D%29%20%3D%20%20%5Csum_k%3D1%5E3%20%28%20%5Czeta%20%5E%7Bk%7D%20-%20F%28W%2Cw%2Cw_%7B0%7D%2C%20%5Cvarepsilon%20%5E%7Bk%7D%29%29%20}#gh-dark-mode-only)
![formula](https://render.githubusercontent.com/render/math?math={E%28W%2Cw%2Cw_%7B0%7D%29%20%3D%20%20%5Csum_k%3D1%5E3%20%28%20%5Czeta%20%5E%7Bk%7D%20-%20F%28W%2Cw%2Cw_%7B0%7D%2C%20%5Cvarepsilon%20%5E%7Bk%7D%29%29%20}#gh-light-mode-only)

El objetivo es obtener los valores de W w y w0 que minimizen el error para los datos de entrada, utilizando algoritmos geneticos con distintos metodos de mutacion,seleccion y cruza

## Requerimientos

- Python 3

## Ejecucion
### Configuraciones iniciales

Una vez clonado el proyecto en su carpeta de preferencia, para configurar los parametros iniciales se debe utilizar el archivo `config.json`. Este archivo posee una gran variedad de parametros, que se discutiran en base a los distintos tipos de parametros

#### Parametros generales

Estos parametros hacen referencia a la ejecucion en general. Los parametros son:
- "initial_values": se compone de una matriz donde se especifican los valores de entrada (siempre vectores de 3 componentes).
- "initial_results": es un vector con el valor del reactivo para cada uno de los valores de entrada (1 o 0)
- "limit_first_generation": numero real utilizado como limite para la generacion de los primeros individuos de la poblacion. Las componentes de estos individuos se obtendran como un random entre -value y +value
-"population_size": cantidad de individuos de la poblacion a utilizar en el algoritmo
- "generations": criterio de corte por cantidad de generaciones a utilizar. Este criterio es el default. En caso de no estar el campo, o de ser un numero menor a la cantidad de generaciones minimas permitidas (500), se toma este valor como criterio de corte.
- "error_threshold": criterio de corte de error. El programa finalizara al encontrar un valor de error inferior al criterio o al superar el limite de generaciones. Es un parametro opcional, en caso de no indicarse se usa como criterio el default.
- "output_path": path + nombre de archivo utilizado como output. No especificar la extension, por default es un archivo csv

#### Parametros de cruza

Para espeficiar las opciones del metodo de cruza, se utiliza el siguiente formato:
- "crossbreeding": objeto que contiene las propiedades:
    - "method": metodo de cruza a utilizar. Las opciones son
        - "simple": metodo de cruza simple
        - "multiple": metodo de cruza multiple
        - "uniform": metodo de cruza uniforme
    - "multiple_point_n": parametro para especificar la cantidad de puntos a tomar en metodo de cruza multiple. En caso de ser otro tipo de cruza, el campo es ignorado

#### Parametros de mutacion
Para espeficiar las opciones del metodo de mutacion, se utiliza el siguiente formato:
- "mutation": objeto que contiene las propiedades:
    - "method": metodo de mutacion a utilizar. Las opciones son
        - "normal": metodo de mutacion con distribucion normal
        - "uniform": metodo de mutacion con distribucion uniforme
    - "probability": probabilidad de mutacion. Usada en ambos metodos.
    - "sigma": parametro utilizado para metodo de mutacion con distribucion normal, a realizarse en el entorno (0,sigma).  Si el metodo es uniforme, este parametro es ignorado
    - "a": parametro utilizado para metodo de mutacion con distribucion uniforme, a realizarse en el entorno (-a,a). Si el metodo es normal, este parametro es ignorado

#### Parametros de seleccion
Para espeficiar las opciones del metodo de seleccion, se utiliza el siguiente formato:
- "selection": objeto que contiene las propiedades:
    - "method": metodo de seleccion a utilizar. Las opciones son
        - "elite": metodo de seleccion elite
        - "roulette": metodo de seleccion de la ruleta
        - "rank":  metodo de seleccion de ranking
        - "truncation": metodo de seleccion de truncamiento
        - "tournament_wr": metodo de seleccion de torneo con reemplazo
        - "tournament_nr": metodo de seleccion de torneo sin reemplazo
        - "boltzmann": metodo de seleccion de boltzmann
    - "truncation_k": numero de valores a descartar para metodo de truncamiento. Si el metodo de seleccion es otro, este parametro es ignorado.
    - "tournament_threshold": valor de umbral para metodo de torneo. Si el metodo de seleccion es otro, este parametro es ignorado.
    - "boltzmann_k": valor de k para metodo de boltzmann. Si el metodo de seleccion es otro, este parametro es ignorado.
    - "boltzmann_tc": valor de temperatura critica para metodo de boltzmann. Si el metodo de seleccion es otro, este parametro es ignorado.
    - "boltzmann_t0": valor de temperatura inicial para metodo de boltzmann. Si el metodo de seleccion es otro, este parametro es ignorado.

### Ejecucion del proyecto

Para correr el proyecto, una vez posicionado sobre el directorio base de este y habiendo configurado los parametros iniciales, basta con ejecutar:

```bash
$ python3 main.py
```
Al finalizar su ejecucion, el programa mostrara los parametros iniciales de ejecucion, asi como tambien los valores de W, w y w0 de la mejor solucion y los valores de la funcion F para cada valor inicial. Ademas, se muestra el valor del error para la solucion, la cantidad de generaciones realizadas y el tiempo de procesamiento. Por ultimo se genera un archivo csv con el nombre indicado en `config.json` donde se dejan los valores de fitness minimo y maximo respectivamente para cada generacion. 

### Configuraciones ejemplo

En todos los ejemplos se utilizaran los mismos 3 valores iniciales, pero pueden usarse mas o ser diferentes.

Si por ejemplo busco resolver el problema con metodo de seleccion elite, cruza simple y mutacion normal usando como criterio de corte 700 generaciones, con 50 miembros en su poblacion, se puede configurar el archivo `config.json` como:
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
Si buscase resolver el mismo problema pero con mutacion uniforme, usando ahora un metodo de seleccion de boltzmann y un criterio de corte por error de 1e-20, se puede configurar el archivo `config.json` como: 
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
Por ultimo se puede querer utilizar el metodo de cruza multiple con 2 puntos en vez del simple, y utilizar el metodo de seleccion de torneo sin reemplazo con umbral de 0.75, agregando ademas un criterio de corte por generaciones de 1000, se puede configurar el archivo `config.json` como:
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


