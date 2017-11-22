from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Foo").getOrCreate()

sc = spark.sparkContext

text_file = sc.textFile("hdfs:///datasets/gutenberg-txt-es/5*.txt")
counts = text_file.flatMap(lambda line: line.split(" ")) \
                 .map(lambda word: (word, 1)) \
                 .reduceByKey(lambda a, b: a + b)
counts.coalesce(1).saveAsTextFile("hdfs:///user/jzapat80/jzpoutfoo")
spark.stop()