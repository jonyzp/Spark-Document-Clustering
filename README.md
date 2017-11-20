# Spark-Document-Clustering
## Tópicos Especiales en Telemática: Proyecto Big Data – Clústering de Documentos a partir de Métricas de Similitud
Este proyecto plantea los retos de un típico buscador en la web (Google, Facebook, Amazon, Spotify, Netflix, entre otros), en los que se necesitan sistemas de recomendación que sugieran busquedas relacionadas, en donde se requiere hacer procesamiento natural del lenguaje, etc. 
El diseño e implementación de este algoritmo ha sido pensado para ejecutarse con Spark, que es una nueva tecnologia diseñada especificamente para el tratamiento y procesamiento de gran volumen de datos.
El reto a afrontar es el clustering de un conjunto de documentos utilizando el algoritmo de k–means y una métrica de similaridad entre documentos llamada TF-IDF, cuya finalidad es encontrar la importancia o frecuencia de las palabras dentro de cada documento y luego realiza una busqueda y asignacion de importancias de cada termino dentro de todos los documentos. Luego de tener la importancia o la matriz de pesos entre documentos procedemos a aplicar el algoritmo de K-means, que primero debe de ser entrenado con un conjunto de documentos preferiblemene similares al conjunto que va ha ser analizado; hay que aclarar que ambos conjuntos deben de pasar antes por el algoritmo de similaridad TF-IDF.
Para nuestro caso el entrenamiento del K-means se realizo con un subconjunto de documentos de la base de datos Gutenberg y se realizara el agrupamiento sobre un subconjunto del mismo.

### Requisitos
* Tener Apache Apark instalado en el sistema
* Tener instalado Python 2.7 y pySpark (pip install pyspark).
* Tener un dataset: https://drive.google.com/file/d/0B2Mzhc7popBga2RkcWZNcjlRTGM/edit
* Copiar el dataset desde la máquina local al DCA:

Para Windows:
`pscp <path>\Gutenberg.zip jzapat80@192.168.10.75:/home/<usuario>`

Para Linux:
`scp <path>\Gutenberg.zip jzapat80@192.168.10.75:/home/<usuario>`

Luego de hacer esto, meterse en el DCA, descomprimir el .zip y enviar la carpeta descomprimida al hdfs:
`hdfs dfs -put -f <carpeta_descomprimida> hdfs:///user/jzapat80/gutenbergDataset`

Tenga en cuenta que ningún nombre de archivo debe contener ':' en tal caso ejecutar: `rm *:*`

### Documentación de Usuario
Para ejecutar el archivo .py se debe de pasar por parámetros: 
* La ruta donde desea guardar o cargar el modelo de K-Means previamente entrenado. Esta ruta es la dirección de un carpeta (no de un archivo). Para que el modelo sea guardado la ruta no debe de existir.
* La ruta de la carpeta donde se encuentran los archivos .txt que desean ser analizados, se debe tener en cuenta que la ruta es una carpeta.
* La ruta donde desea almacenar el archivo .txt con la agrupación de los documentos. Esta ruta no debe de existir.
* El número de clusters que el usuario desea realizar.
LOS ANTERIORES PARÁMETROS SON OBLIGATORIOS, EL SIGUIENTE SE PUEDE OMITIR CUANDO SE ESTA SEGURO DE POSEER EL MODELO.
* La ruta de la carpeta o folder donde se encuentran los documentos con los cuales desea generar el modelo de K-Means de entrenamiento. Tenga en cuenta que esta ruta no es utilizada en caso tal de que un modelo sea encontrado.

##### Modo de Ejecución:

Para  ejecutarlo de forma local:

*spark-submit <proyecto.py> <parametros(path, k, maximo de iteraciones)>*
* Ejemplo:
```
spark-submit practicaFinal5.py hdfs:///user/jzapat80/KMeansModel hdfs:///user/jzapat80/guty200 hdfs:///user/jzapat80/grupos 4 hdfs:///user/jzapat80/guty400
```

Para ejecutar el algoritmo en el cluster:

*spark-submit --master yarn --deploy-mode cluster <proyecto.py> <parametros(path, k, maximo de iteraciones)>*

* Ejemplo:

```
spark-submit practicaFinal5.py --master yarn --deploy-mode cluster hdfs:///user/jzapat80/KMeansModel hdfs:///user/jzapat80/guty200 hdfs:///user/jzapat80/grupos 4 hdfs:///user/jzapat80/guty400
```
Por diseño de la arquitectura de spark, la carpeta sobre la cual se van a guardar los clusters no debe de existir, asi que si se desean realizar varias ejecuciones y guardarlas en la misma carpeta se debe de eliminar la carpeta antes de ejecutarlo.
`hdfs dfs -rm -r /user/jzapat80/grupos*`

##### Comandos útiles:

`hdfs dfs -du -s -h /user/jzapat80/guty120*` Muestra el tamaño de la carpeta

`hdfs dfs -cp "/user/jzapat80/guty400/" "/user/jzapat80/guty120MB"` copiar una carpeta a otra en hdfs

`hdfs dfs -rm -r /user/jzapat80/KMea*` Borra el modelo que entrenamos

`hdfs dfs -rm -r /user/jzapat80/grupos*` Borra la salida después de la primera ejecución
 
### Referencias:

* [Algoritmo K-means] https://spark.apache.org/docs/latest/mllib-clustering.html#k-means
* [Algoritmo TF-IDF] https://spark.apache.org/docs/latest/mllib-feature-extraction.html#tf-idf
* [Dataset Gutenberg] https://drive.google.com/uc?id=0B_4oKjh0Qca5RWlGZkRRT1pVLU0&export=download
