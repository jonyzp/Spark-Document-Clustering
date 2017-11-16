from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("Foo").getOrCreate()

from pyspark.sql import SQLContext 
sc = spark.sparkContext
sqlContext = SQLContext(sc)
txtFiles = sqlContext.read.text("hdfs:///datasets/gutenberg-txt-es/5*.txt")
parquetRoot = "hdfs:///user/jzapat80/parquetPract"
txtFiles.write.parquet(parquetRoot)
df = spark.read.format("parquet").load(parquetRoot)
df.cache().count()

from pyspark.ml.feature import HashingTF, IDF, Tokenizer, CountVectorizer, StopWordsRemover
tokenizer = Tokenizer(inputCol="text", outputCol="tokens")
remover = StopWordsRemover(inputCol="tokens", outputCol="stopWordsRemovedTokens")
hashingTF = HashingTF(inputCol="stopWordsRemovedTokens", outputCol="rawFeatures", numFeatures=2000)
idf = IDF(inputCol="rawFeatures", outputCol="features", minDocFreq=5)

from pyspark.ml.clustering import KMeans
kmeans = KMeans(k=20)

from pyspark.ml import Pipeline
pipeline = Pipeline(stages=[tokenizer, remover, hashingTF, idf, kmeans])

model = pipeline.fit(df)

results = model.transform(df)
results.cache()

show(results.groupBy("prediction").count())  # Note "display" is for Databricks; use show() for OSS Apache Spark

