from numpy import array
from math import sqrt
from pyspark.sql import SparkSession
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.clustering import KMeans, KMeansModel
spark = SparkSession.builder.appName("WordCount").getOrCreate()
sc = spark.sparkContext

# Load documents (one per line).
documents = sc.textFile("hdfs:///datasets/gutenberg-txt-es/5*.txt").map(lambda line: line.split(" "))

hashingTF = HashingTF()
tf = hashingTF.transform(documents)
idf = IDF().fit(tf)
tfidf = idf.transform(tf)

#collectedTFIDF = tfidf.collect()
print("tfidf listo========================#########################************************************====================================")
clusters = KMeans.train(tfidf, 4, maxIterations=10, initializationMode="random")

print("Predict")
agrupamiento = clusters.predict(tfidf).collect()
print("===============================================================")
print(agrupamiento)

sc.stop()
