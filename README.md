# Spark-Document-Clustering

## Autores:
* Mauricio Hoyos Ardila - mhoyosa2@eafit.edu.co
* Jonathan Zapata Castaño - jzapat80@eafit.edu.co

## Tópicos Especiales en Telemática: Proyecto Big Data – Clústering de Documentos a partir de Métricas de Similitud
Este proyecto plantea los retos de un típico buscador en la web (Google, Facebook, Amazon, Spotify, Netflix, entre otros), en los que se necesitan sistemas de recomendación que sugieran busquedas relacionadas, en donde se requiere hacer procesamiento natural del lenguaje, etc. 
El diseño e implementación de este algoritmo ha sido pensado para ejecutarse con Spark, que es una nueva tecnologia diseñada especificamente para el tratamiento y procesamiento de gran volumen de datos.
El reto a afrontar es el clustering de un conjunto de documentos utilizando el algoritmo de k–means y una métrica de similaridad entre documentos llamada TF-IDF, cuya finalidad es encontrar la importancia o frecuencia de las palabras dentro de cada documento y luego realiza una busqueda y asignacion de importancias de cada termino dentro de todos los documentos. Luego de tener la importancia o la matriz de pesos entre documentos procedemos a aplicar el algoritmo de K-means, que primero debe de ser entrenado con un conjunto de documentos preferiblemene similares al conjunto que va ha ser analizado; hay que aclarar que ambos conjuntos deben de pasar antes por el algoritmo de similaridad TF-IDF.
Para nuestro caso el entrenamiento del K-means se realizo con un subconjunto de documentos de la base de datos Gutenberg y se realizara el agrupamiento sobre un subconjunto del mismo.

### Requisitos
* Tener Apache Apark instalado en el sistema
* Tener instalado Python 2.7 y pySpark (pip install pyspark).
* Tener un dataset

**Pasos para obtener el dataset:**

1. Descargar un .zip con archivos .txt, puede descargar el set de datos de Gutenberg: https://drive.google.com/file/d/0B2Mzhc7popBga2RkcWZNcjlRTGM/edit
2. Copiar el dataset desde la máquina local al DCA:

Para Windows:
`pscp <path>\Gutenberg.zip <usuario>@192.168.10.75:/home/<usuario>`

Para Linux:
`scp <path>\Gutenberg.zip <usuario>@192.168.10.75:/home/<usuario>`

3. Luego de hacer esto, meterse en el DCA, descomprimir el .zip y enviar la carpeta descomprimida al hdfs:
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

Después de ejecutarlo hacer ls en hdfs a la carpeta que se ingresó como parámetro para guardar la salida del proceso. Si se ingresó como pathToOutput la carpeta `hdfs:///user/jzapat80/grupos` entonces se debe hacer lo siguiente:

```
hdfs dfs -ls grupos
hdfs dfs -cat grupos/part*
```

##### Modo de Ejecución:

Para  ejecutarlo de forma local:

*spark-submit <proyecto.py> <parametros(pathToSaveTrainModel, pathDatasetToAnalyze, pathToOutput, k, pathToDataSetToTrain)>*
* Ejemplo:
```
spark-submit practicaFinal5.py hdfs:///user/jzapat80/KMeansModel hdfs:///user/jzapat80/guty200 hdfs:///user/jzapat80/grupos 4 hdfs:///user/jzapat80/guty400
```

Para ejecutar en el clúster:

*spark-submit --master yarn --deploy-mode cluster <proyecto.py> <parametros(pathToSaveTrainModel, pathDatasetToAnalyze, pathToOutput, k, pathToDataSetToTrain)>*

* Ejemplo:

```
spark-submit practicaFinal5.py --master yarn --deploy-mode cluster hdfs:///user/jzapat80/KMeansModel hdfs:///user/jzapat80/guty200 hdfs:///user/jzapat80/grupos 4 hdfs:///user/jzapat80/guty400
```
**Nota importante:**
Por diseño de la arquitectura de spark, la carpeta sobre la cual se van a guardar los clusters no debe de existir, asi que si se desean realizar varias ejecuciones se debe de eliminar la carpeta antes de ejecutarlo.
`hdfs dfs -rm -r /user/jzapat80/grupos*`

##### Comandos útiles:

`hdfs dfs -du -s -h /user/jzapat80/guty120*` Muestra el tamaño de la carpeta

`hdfs dfs -cp "/user/jzapat80/guty400/" "/user/jzapat80/guty120MB"` copiar una carpeta a otra en hdfs

`hdfs dfs -rm -r /user/jzapat80/KMea*` Borra el modelo que entrenamos

`hdfs dfs -rm -r /user/jzapat80/grupos*` Borra la salida después de la primera ejecución

`hdfs dfs -ls grupos` Para mostrar el nombre del .txt que arrojó como salida el programa

`hdfs dfs -cat grupos/part*` Para mostrar la salida del programa
 
### Referencias:

* [Algoritmo K-means] https://spark.apache.org/docs/latest/mllib-clustering.html#k-means
* [Algoritmo TF-IDF] https://spark.apache.org/docs/latest/mllib-feature-extraction.html#tf-idf
* [Dataset Gutenberg] https://drive.google.com/uc?id=0B_4oKjh0Qca5RWlGZkRRT1pVLU0&export=download
