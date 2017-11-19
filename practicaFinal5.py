import sys
from numpy import array
from math import sqrt
from pyspark.sql import SparkSession
from pyspark.mllib.feature import HashingTF, IDF
from pyspark.mllib.clustering import KMeans, KMeansModel
spark = SparkSession.builder.appName("SparkDocumentClustering").getOrCreate()
sc = spark.sparkContext
# Guarda los nombres de los documentos para poder identificarlos despues
hashingTF = HashingTF()
try:
    clusters = None
    clusters = KMeansModel.load(sc, str(sys.argv[1]))
    #clusters = KMeansModel.load(sc, "hdfs:///user/jzapat80/KMeansModel")#ruta que se tiene que pedir por los argumentos
except Exception as err:
    print ("el directorio de entrenamiento no fue encontrado =) =) =) =) =) =) #) #) #) #) #) #) #)")
    print("entrenando el modelo con la ruta de entrenamiento ingresada")#ruta que se pide por argumentos
    # Carga los documentos con una ruta (regexp)
    #trainDataset = sc.wholeTextFiles("hdfs:///user/jzapat80/gutenbergDataset/txt")
    #trainDataset = sc.wholeTextFiles("hdfs:///user/jzapat80/guty4x4")
    trainDataset = sc.wholeTextFiles(str(sys.argv[5]))
    #trainDataset = sc.wholeTextFiles("hdfs:///user/jzapat80/guty400")# es la que se pide arriba en el print
    palabras = trainDataset.values().map(lambda line: line.split(" "))
    tf = hashingTF.transform(palabras)
    idf = IDF().fit(tf)
    # Que tan importante es cada termino
    tfidf = idf.transform(tf)
    # Entrena el kmeans con el set de datos
    clusters = KMeans.train(tfidf, int(sys.argv[4]), maxIterations=10)

    # Guardar el modelo entrenado:
    clusters.save(sc, str(sys.argv[1]))#la misma ruta que se ingreso para tratar de cargar el modelo
    #clusters.save(sc, "hdfs:///user/jzapat80/KMeansModel")
    #sameModel = KMeansModel.load(sc, "target/org/apache/spark/PythonKMeansExample/KMeansModel")

#testDataset = sc.wholeTextFiles("hdfs:///user/jzapat80/guty4x4")
testDataset = sc.wholeTextFiles(str(sys.argv[2]))
#testDataset = sc.wholeTextFiles("hdfs:///user/jzapat80/guty400")#ruta que se pide para realizar el agrupamiento, esta es diferente a las anterioriores
testWords = testDataset.values().map(lambda line: line.split(" "))
#print(testWords)
filenames = testDataset.keys().collect()
test_tf = hashingTF.transform(testWords)
test_idf = IDF().fit(test_tf)
# Que tan importante es cada termino
test_tfidf = test_idf.transform(test_tf)
# Prueba el K-means con el mismo set de datos (puede ser otro dataset)
agrupamiento = clusters.predict(test_tfidf)
agrupamiento = agrupamiento.collect()
resultado = {}
for i in range(len(agrupamiento)):
    if agrupamiento[i] in resultado.keys():
        resultado[agrupamiento[i]].append(filenames[i])
    else:
        resultado[agrupamiento[i]]= [filenames[i]]

resultado = sc.parallelize(resultado.items())
resultado.coalesce(1).saveAsTextFile(str(sys.argv[3]))
#resultado.coalesce(1).saveAsTextFile("hdfs:///user/jzapat80/grupos")#ruta donde se almacenara los cluster finales
sc.stop()
