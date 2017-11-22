from __future__ import print_function

# $example on$
from numpy import array
from math import sqrt
# $example off$

from pyspark import SparkContext
# $example on$
from pyspark.mllib.clustering import KMeans, KMeansModel
# $example off$

if __name__ == "__main__":
    sc = SparkContext(appName="KMeansExample")  # SparkContext

    # $example on$
    # Load and parse the data
    data = sc.textFile("hdfs:///datasets/gutenberg-txt-es/5*.txt")
    parsedData = data.map(lambda line: array([x for x in line.split(' ')]))
    # Build the model (cluster the data)
    clusters = KMeans.train(parsedData, 2, maxIterations=10, initializationMode="random")

    # Evaluate clustering by computing Within Set Sum of Squared Errors
    def error(point):
        center = clusters.centers[clusters.predict(point)]
        return sqrt(sum([x**2 for x in (point - center)]))

    WSSSE = parsedData.map(lambda point: error(point)).reduce(lambda x, y: x + y)
    print("Within Set Sum of Squared Error = " + str(WSSSE))

    # Save and load model
    clusters.save(sc, "~/practFinal/pruebas")
    sameModel = KMeansModel.load(sc, "~/practFinal/pruebasModel")
    # $example off$

    sc.stop()
