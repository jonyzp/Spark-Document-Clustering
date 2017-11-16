from numpy import array
from math import sqrt
from pyspark.sql import SparkSession
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.clustering import KMeans, KMeansModel
spark = SparkSession.builder.appName("WordCount").getOrCreate()
sc = spark.sparkContext

# Load documents (one per line).
documents = sc.wholeTextFiles("hdfs:///user/mhoyosa2/gutenberg")
palabras = documents.values().map(lambda line: line.split(" "))
archivos = documents.keys().collect()
hashingTF = HashingTF()
tf = hashingTF.transform(palabras)
idf = IDF().fit(tf)
tfidf = idf.transform(tf)

clusters = KMeans.train(tfidf, 4, maxIterations=10)

agrupamiento = clusters.predict(tfidf)
agrupamiento = agrupamiento.collect()
resultado = {}
for i in range(len(agrupamiento)):
    if agrupamiento[i] in resultado.keys():
        resultado[agrupamiento[i]].append(archivos[i])
    else:
        resultado[agrupamiento[i]]= [archivos[i]]

resultado = sc.parallelize(resultado.items())
resultado.coalesce(1).saveAsTextFile("hdfs:///user/mhoyosa2/grupos")
sc.stop()
