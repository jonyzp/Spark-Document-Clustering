from numpy import array
from math import sqrt
from pyspark.sql import SparkSession
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.clustering import KMeans, KMeansModel
spark = SparkSession.builder.appName("SparkDocumentClustering").getOrCreate()
sc = spark.sparkContext

# Carga los documentos con una ruta (regexp)
documents = sc.wholeTextFiles("hdfs:///user/mhoyosa2/gutenberg")
palabras = documents.values().map(lambda line: line.split(" "))
# Guarda los nombres de los documentos para poder identificarlos despues
filenames = documents.keys().collect()
hashingTF = HashingTF()
tf = hashingTF.transform(palabras)
idf = IDF().fit(tf)
# Que tan importante es cada termino
tfidf = idf.transform(tf)
# Entrena el kmeans con el set de datos
clusters = KMeans.train(tfidf, 4, maxIterations=10)
# Prueba el K-means con el mismo set de datos (puede ser otro dataset)
agrupamiento = clusters.predict(tfidf)
agrupamiento = agrupamiento.collect()
resultado = {}
for i in range(len(agrupamiento)):
    if agrupamiento[i] in resultado.keys():
        resultado[agrupamiento[i]].append(filenames[i])
    else:
        resultado[agrupamiento[i]]= [filenames[i]]

resultado = sc.parallelize(resultado.items())
resultado.coalesce(1).saveAsTextFile("hdfs:///user/mhoyosa2/grupos")
sc.stop()
