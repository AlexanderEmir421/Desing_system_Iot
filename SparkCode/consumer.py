from pyspark.sql import SparkSession
from pyspark.sql.functions import split, col
import pymysql

spark = SparkSession.builder \
    .appName("StructuredNetworkWordCount") \
    .config("spark.driver.host", "localhost") \
    .getOrCreate()

# Create DataFrame representing the stream of input lines from Kafka
df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "connect-custom") \
    .load()

# Convert value column to string and split by ';'
df = df.withColumn("value", df["value"].cast("string"))
df = df.withColumn("words", split(df["value"], ";"))

# Add columns from the split words
df = df.withColumn("Dato", df["words"].getItem(0))
df = df.withColumn("IdUsuario", df["words"].getItem(1))
df = df.withColumn("IdDispositivo", df["words"].getItem(2))
df = df.withColumn("IdTopico", df["words"].getItem(3))

# Function to obtain topic details from the database
def obtener_detalles_topico(id_topico):
    connection = pymysql.connect(host='db',
                                 user='db_user',
                                 password='db_user_pass',
                                 db='app_db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM topicos WHERE id_topico = %s"
            cursor.execute(sql, (id_topico,))
            result = cursor.fetchone()
            return result
    finally:
        connection.close()

# Function to process each batch
def foreach_batch_function(df, epoch_id):
    for row in df.collect():
        dato = row["Dato"]
        id_usuario = row["IdUsuario"]
        id_dispositivo = row["IdDispositivo"]
        id_topico = row["IdTopico"]
        
        detalles_topico = obtener_detalles_topico(id_topico)
        
        if detalles_topico:
            # Guardar el dato en el historiador
            connection = pymysql.connect(host='db',
                                 user='db_user',
                                 password='db_user_pass',
                                 db='app_db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
            try:
                with connection.cursor() as cursor:
                    sql = "INSERT INTO historiador (id_topico, dato, fechayhora) VALUES (%s, %s, NOW())"
                    cursor.execute(sql, (id_topico, dato))
                connection.commit()
            finally:
                connection.close()
        else:
            print("No se encontraron detalles para el tópico:", id_topico)

query = df \
    .writeStream \
    .outputMode("append") \
    .foreachBatch(foreach_batch_function) \
    .start()

query.awaitTermination()
