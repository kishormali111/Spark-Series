# Spark Installation in Google Colab with ngrok UI

# This notebook demonstrates how to install and configure Apache Spark
# in Google Colab with ngrok for accessing Spark UI from anywhere

## Step 1: Install Java (Required for Spark)
!apt-get update
!apt-get install -y openjdk-8-jdk-headless -qq > /dev/null

## Verify Java installation
!java -version

## Step 2: Install Spark
!wget -q https://archive.apache.org/dist/spark/spark-3.5.0/spark-3.5.0-bin-hadoop3.tgz
!tar xf spark-3.5.0-bin-hadoop3.tgz
!pip install -q findspark

## Step 3: Set up environment variables
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-3.5.0-bin-hadoop3"

## Step 4: Install ngrok
!pip install -q pyngrok

## Step 5: Configure ngrok
from pyngrok import ngrok

# You need an ngrok authtoken - get it from https://dashboard.ngrok.com/auth/your-authtoken
# Replace YOUR_AUTHTOKEN with your actual token
ngrok.set_auth_token("YOUR_AUTHTOKEN")

## Step 6: Initialize Spark Session
import findspark
findspark.init()

from pyspark.sql import SparkSession

# Create Spark session with UI accessible via ngrok
spark = SparkSession.builder \
    .appName("Colab-Spark-App") \
    .config("spark.ui.port", "4040") \
    .config("spark.driver.bindAddress", "127.0.0.1") \
    .getOrCreate()

print("Spark Session Created Successfully!")
print(f"Spark Version: {spark.version}")

## Step 7: Expose Spark UI using ngrok
# Open ngrok tunnel to Spark UI
public_url = ngrok.connect(4040, "http")
print(f"\n✅ Spark UI is accessible at: {public_url}")

## Step 8: Test Spark with Sample Data
# Create a sample DataFrame
data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
columns = ["Name", "Age"]

df = spark.createDataFrame(data, schema=columns)
df.show()

print("\n✅ Spark is working correctly in Google Colab!")
print("📊 Access your Spark UI from the ngrok URL above")

## Step 9: Stop ngrok tunnel (when done)
# ngrok.disconnect()
# spark.stop()

## Notes:
# 1. Free ngrok account gives you a random URL that changes each time
# 2. For persistent URLs, upgrade to ngrok paid plan
# 3. Keep the ngrok tunnel active to access Spark UI
# 4. The Spark UI will show you:
#    - Jobs and their stages
#    - Task execution details
#    - Storage/Cache information
#    - Executor information
#    - Environment settings

## Useful Spark Commands:
# - View Spark configuration: spark.sparkContext.getConf().getAll()
# - Check number of partitions: df.rdd.getNumPartitions()
# - Show DataFrame schema: df.printSchema()
# - Describe DataFrame: df.describe().show()
