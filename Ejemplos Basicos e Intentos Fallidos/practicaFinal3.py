from __future__ import print_function

from pyspark import SparkContext
# $example on$
from pyspark.mllib.feature import HashingTF, IDF
# $example off$

if __name__ == "__main__":
    sc = SparkContext(appName="TFIDFExample")  # SparkContext

    # $example on$
    # Load documents (one per line).
    documents = sc.textFile("hdfs:///datasets/gutenberg-txt-es/5*.txt").map(lambda line: line.split(" "))

    hashingTF = HashingTF()
    #tf = hashingTF.transform(documents)
    tfVectors = hashingTF.transform(documents).cache()
    # While applying HashingTF only needs a single pass to the data, applying IDF needs two passes:
    # First to compute the IDF vector and second to scale the term frequencies by IDF.
    tf.cache()
    #idf = IDF().fit(tf)
    idf = IDF(inputCol="rawFeatures", outputCol="features", minDocFreq=5)
    idfModel = idf.fit(tfVectors)
    tfidf = idf.transform(tf)
    idfModel = idf.fit(tfVectors)

    tfIdfVectors = idfModel.transform(tfVectors).cache()

    from pyspark.ml.feature import Normalizer
    from pyspark.ml.linalg import Vectors

    normalizer = Normalizer(inputCol="features", outputCol="normFeatures")
    l2NormData = normalizer.transform(tfIdfVectors)

    from pyspark.ml.clustering import KMeans

    # Trains a KMeans model.
    kmeans = KMeans().setK(6).setMaxIter(20)
    km_model = kmeans.fit(l2NormData)

    clustersTable = km_model.transform(l2NormData)

    # spark.mllib's IDF implementation provides an option for ignoring terms
    # which occur in less than a minimum number of documents.
    # In such cases, the IDF for these terms is set to 0.
    # This feature can be used by passing the minDocFreq value to the IDF constructor.
    idfIgnore = IDF(minDocFreq=2).fit(tf)
    tfidfIgnore = idfIgnore.transform(tf)
    # $example off$

    print("tfidf:")
    for each in tfidf.collect():
        print(each)

    print("tfidfIgnore:")
    for each in tfidfIgnore.collect():
        print(each)

    sc.stop()
