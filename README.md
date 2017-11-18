# Spark-Document-Clustering
## Tópicos Especiales en Telemática: Proyecto 4 – Clústering de Documentos a partir de Métricas de Similitud
Este proyecto plantea los retos de un típico buscador en la web (Google, Facebook, Amazon, Spotify, Netflix, entre otros), en los que se necesitan sistemas de recomendación que sugieran busquedas relacionadas, en donde se requiere hacer procesamiento natural del lenguaje, etc. 
El diseño e implementación de este algoritmo ha sido pensado para ejecutarse con Spark, que es una nueva tecnologia diseñada especificamente para el tratamiento y procesamiento de gran volumen de datos.
El reto a afrontar es el clustering de un conjunto de documentos utilizando el algoritmo de k–means y una métrica de similaridad entre documentos llamada TF-IDF, cuya finalidad es encontrar la importancia o frecuencia de las palabras dentro de cada documento y luego realiza una busqueda y asignacion de importancias de cada termino dentro de todos los documentos. Luego de tener la importancia o la matriz de pesos entre documentos procedemos a aplicar el algoritmo de K-means, que primero debe de ser entrenado con un conjunto de documentos preferiblemene similares al conjunto que va ha ser analizado; hay que aclarar que ambos conjuntos deben de pasar antes por el algoritmo de similaridad TF-IDF.
Para nuestro caso el entrenamiento del K-means se realizo con un subconjunto de documentos de la base de datos Gutenberg y se realizara el agrupamiento sobre un subconjunto del mismo.

### Documentación de Usuario
Para ejecutar el archivo .PY se deben de pasar por parametros: 
* la ruta de la carpeta donde se encuentran los archivos .txt que desean ser analizados, se debe de tener en cuenta que la ruta es una carpeta.
* La ruta sobre la cual se buscara la carpeta con el modelo entrenado y en caso tal que no exista entrenamiento o corridas previas del software ahi mismo se guardara el modelo entrenado
* el numero de clusters que el usuario desea realizar.

Por diseño de la arquitectura de spark, la carpeta sobre la cual se van a guardar los clusters no debe de existir, asi que si se desean realizar varias ejecuciones y guardarlas en la misma carpeta se debe de eliminar la carpeta antes de ejecutarlo.

##### Requisitos
* tener apache spark instalado en el sistema
* Tener instalado Python 2.7 y pySpark configurado con el python (pip install pyspark).
* Tener un dataset: https://drive.google.com/file/d/0B2Mzhc7popBga2RkcWZNcjlRTGM/edit
* Copiar el dataset desde la maquina local al DCA:
Para Windows:
`pscp <path>\Gutenberg.zip jzapat80@192.168.10.75:/home/<usuario>`
Para Linux:
`scp <path>\Gutenberg.zip jzapat80@192.168.10.75:/home/<usuario>`

##### Ejecucion

Para ejecutar el algoritmo desde el un cluster:
spark-submit --master yarn --deploy-mode cluster --executor-memory 2G --num-executors 4 <proyecto.py> <parametros(path, k, maximo de iteraciones)>

Para  ejecutarlo de forma local
spark-submit <proyecto.py> <parametros(path, k, maximo de iteraciones)>

### Referencias:

* [Algoritmo K-means] https://spark.apache.org/docs/latest/mllib-clustering.html#k-means
* [Algoritmo TF-IDF] https://spark.apache.org/docs/latest/mllib-feature-extraction.html#tf-idf
* [Dataset Gutenberg] https://drive.google.com/uc?id=0B_4oKjh0Qca5RWlGZkRRT1pVLU0&export=download
