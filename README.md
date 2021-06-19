# PlasticMvmSimulation
This repository is created for the purposes of GEO1101 synthesis project from TUDelft and Noria with the objective to develop a simple simulation model that tries to predict the movement and accumulation of plastic flaoting in water bodies.

## Important information
The algorithm aims to model the movement of plastic objects using an agent-based approach with Object-Orientated programming in Python. However, due to the fact that it is modelling inanimate objects without clear interactivity between them, we assume that the agents are isolated from each other and are being affected individually only by their environment.

## Limitations
- The algorithm was developed having in mind the urban environment of South-Holland provice of the Netherlands and in particular the city of Delft area. ![City of Delft](https://www.google.com/maps/vt/data=9DSKHP38T__S9MAEQKeSlOCx5me129gsIymgTraM3w03AWQKcEJbKH1_CTmigIYVkxL1dwmQpDIFmEblLHLODxLZW-PpQTH8J11N1i6s0XB9KTd5R-7wXRuDGXSqC7uDkAfWywm_-Of8MweWAYa94d2G6jMNoqbas8Te6rwZipjETwSQgwcWuPHSLrnBTy1MOKUXvQB8r_d3xHA5ybUhmwusnfg5oDh2gsxQjvcRL1AoU18)

- The code is not dynamic in the sense that users need to manually change directory path of input or output to their liking.
- The code us heavily dependent on the input dataset format.
    The input datasets are located into the './Data' folder   
- The algorithm ovesimplifies the process of floating plastic movement. In detail, it only takes into account the wind and flow (if present) directional forces using major assumtion. These assumption are:
    - Wind velocity (constant) is 21km/h 
    - Flow speed (when present) is 0.24km/h
However, there many other natural or man-made phenomenon that can influence the accuracy of the output in reality. These can be:
    - Urban fabric: Building can pose as obstacles that create vortices changing the local wind direction. Moreover, canal or rivers could be protected with railings or walls obstracting trash falling in them
    - Fluid dynamics: In general, fluids' unstable behaviour affect greatly small floating objects in ways that need more sophisticated approaches of modelling. 
    - Weather conditions: Depending on weather, climate and seasons, waterways may be clogged with overgrowing vegetation, ice, increased flow from persipitation.
    - Cleaning operations: Results may also differ greatly due to cleaning operations in the area.
    - Vegetation: Vegetation in water bodies pose serious obstacle and natural plastic capturing bodies but is hard to document and acquire up-to-date datasets so it is not included. 

## Code information
The simulation is developed using the programming language 'Python'. The version on which it was developed is 3.8.5. Additionally, the code uses some 3rd party packages that need to be installed that may also require extra dependencies: 
- NetworkX (https://pypi.org/project/networkx/)
- Numpy (https://pypi.org/project/numpy/)
- Matplotlib (https://pypi.org/project/matplotlib/)

The code requires to include a ’Data’ directory into its own directory containing a .shp of edges and one of nodes that are the inputs of the simulation.  

The exact name of the shapefiles is currently hardcoded into a relative path.  Users that want to use  other  datasets  than  the  one already provided,  must  change  the  relative  path  from within the code itself (in main.py).

It is important for:
- the 'node' dataset to contain fields of "id", "class", and "pls_amount" (plastic amount) as this information is crucial to the code’s functions.

- the 'edges' dataset to contain fields of "has_flow" determining the existance of flow in waterways, as this information is crucial to the code’s functions.