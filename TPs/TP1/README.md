# TP1
## Scripts
- ```runner.sh```: Este script es el que utiliza el grupo para poder crear la VM de Google Cloud.
- ```iniciar_contenedores.sh```: Este script clona este repositorio y corre todos los contenedores relacionados a todos los HITs. Antes de ejecutar este script, la máquina debería tener las imágenes correspondientes, para poder crear los contenedores. (Este script está pensado para probar los HITs de forma local).
- ```script.sh```: Este script hace lo mismo que ```iniciar_contenedores.sh```, y además, instala python y docker, y hace pull de las imágenes desde el repositorio de Docker Hub del grupo. (Este script está pensado para ejecutarse desde la VM de Google Cloud).

## Comentarios para la corrección:
- H1, H2 y H3 están desplegados en la nube, escuchando en sus determinados puertos. (Revisar el README.md de cada uno).
- H4, H5, H6 y H7 se encuentran en la nube, pero los clientes o servidores de cada uno están en redes de docker, y se ejecutan con compose, por lo que para poder corregirse se deben probar de forma local, bajandose las imágenes desde Docker Hub. (Revisar los README.md de cada uno).