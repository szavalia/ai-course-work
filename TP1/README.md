# TP1

## 72.27 - Sistemas de Inteligencia Artificial - 2º cuatrimestre 2022

### Instituto Tecnológico de Buenos Aires (ITBA)

## Autores

- [Sicardi, Julián Nicolas](https://github.com/Jsicardi) - Legajo 60347
- [Quintarios, Juan Ignacio](https://github.com/juaniq99) - Legajo 59715
- [Zavalia Pángaro, Salustiano Jose](https://github.com/szavalia) - Legajo 60312

## Indice
- [Autores](#autores)
- [Indice](#indice)
- [Descripción](#descripcion)
- [Requerimientos](#requerimientos)
- [Ejecucion](#ejecucion)
    - [Configuraciones iniciales](#configuraciones-iniciales)
    - [Ejecucion del proyecto](#ejecucion-del-proyecto)
    - [Configuraciones ejemplo](#configuraciones-ejemplo)

## Descripcion

El proyecto fue desarrollado con Python, y consiste en encontrar una solucion para el juego del rompecabezas de numeros (8-puzzle game, (https://en.wikipedia.org/wiki/15_puzzle)).Esta version del juego se compone de un tablero con 9 casilleros, 8 con numeros del 1 al 8 y uno vacio. El objetivo es lograr que los numeros queden ordenados en orden ascedente en el tablero, moviendo los casilleros aprovechando el espacio libre para reordenarlos. Para resolver este problema, el proyecto utiliza distintos metodos de busqueda tanto informados como desinformados.

## Requerimientos

- Python 3

## Ejecucion

### Configuraciones iniciales

Una vez clonado el proyecto en su carpeta de preferencia, para configurar los parametros iniciales se debe utilizar el archivo `config.json`. Este archivo posee los siguientes parametros:

- "puzzle_layout": este es el estado inicial del tablero, se compone de una matriz con las posiciones de los numeros en el tablero, marcando con un 0 el espacio vacio (ejemplo [ [2,1,5],[3,6,4],[0,7,8] ])
- "algorithm": algoritmo a utilizar para la resolucion del juego ("BFS", "DFS", "VDFS", "HEUR_LOCAL", "HEUR_GLOBAL", "A*")
- "heuristic": heuristica a utilizar para los metodos de busqueda informados. Si el metodo ingresado es no informado, este parametro sera ignorado en ejecucion. Los tipos de heuristica son:
    - "total_squares": esta heuristica utiliza como criterio la cantidad de numeros que no se encuentran en la posicion correcta en el tablero
    - "total_manhattan": esta heuristica utiliza la distancia de Manhattan para medir cuan lejos se encuentra un numero de su posicion correcta en el tablero
    - "total_removing_obstacles": esta heurística tambien utiliza la de distancia de Manhattan pero considera que si hubieran números ocupando algunas de las casillas a recorrer, se deberían gastar movimientos en correrlos para "abrirle paso" al número que estamos analizando y lograr que llegue a su posicion final en el tablero. 
- "starting_depth": profundidad inicial que utiliza el algoritmo VDFS. En caso que el algoritmo no sea ese, el parametro es ignorado en ejecucion

### Ejecucion del proyecto

Para correr el proyecto, una vez posicionado sobre el directorio base de este y habiendo configurado los parametros iniciales, basta con ejecutar:

```bash
$ python3 main.py
```
Al finalizar su ejecucion, el programa mostrara los parametros iniciales de ejecucion, asi como tambien el status (si pudo o no encontrar solucion), los nodos expandidos, los nodos restantes en la frontera y el tiempo de ejecucion. En caso de haber encontrado solucion, se muestra ademas la profundidad de esta y, dentro del archivo `solution.txt`, los pasos para resolver el tablero.

### Configuraciones ejemplo

Busqueda DFS para tablero [ [2,1,5],[3,6,4],[0,7,8] ]
```json
{
    "puzzle_layout": [[2,1,5],[3,6,4],[0,7,8]],
    "algorithm": "DFS",
}
```
Busqueda A* usando la heuristica total_manhattan para tablero [ [2,1,5],[3,6,4],[0,7,8] ]
```json
{
    "puzzle_layout": [[2,1,5],[3,6,4],[0,7,8]],
    "algorithm": "A*",
    "heuristics": "total_manhattan",
}
```
Busqueda VDFS con profundidad inicial 20 para tablero [ [2,1,5],[3,6,4],[0,7,8] ]
```json
{
    "puzzle_layout": [[2,1,5],[3,6,4],[0,7,8]],
    "algorithm": "VDFS",
    "starting_depth": 20
}
```