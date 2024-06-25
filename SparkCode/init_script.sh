#!/bin/bash

# Instalar pymysql
pip install pymysql

# Ejecutar el script Python
exec spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0 /spark/consumer.py
