from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import to_date, col, month, count, avg

spark = SparkSession.builder \
    .appName("ecommerce Analytics") \
    .master("yarn") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")

#step 2: Read Data in PySpark
orders = spark.read.csv(
                "hdfs://localhost:9000/ecommerce/raw/olist_orders_dataset.csv", 
                 header = True,
                 inferSchema = True
                         )
order_items = spark.read.csv(
                "hdfs://localhost:9000/ecommerce/raw/olist_order_items_dataset.csv",
                header = True,
                inferSchema = True
)

orders.printSchema()
order_items.printSchema()

orders.count()
order_items.count()

#step 3:Join data
joined_df = orders.join(
    order_items,
    on="order_id",
    how="inner"
)

joined_df = joined_df.dropna()

joined_df = joined_df.withColumn("order_approved_at", to_date(col("order_approved_at"), "yyyy-MM-dd"))\
                     .withColumn("order_delivered_carrier_date", to_date(col("order_delivered_carrier_date"), "yyyy-MM-dd"))\
                     .withColumn("order_delivered_customer_date", to_date(col("order_delivered_customer_date"), "yyyy-MM-dd"))\
                     .withColumn("order_estimated_delivery_date", to_date(col("order_estimated_delivery_date"), "yyyy-MM-dd"))\
                     .withColumn("shipping_limit_date", to_date(col("shipping_limit_date"), "yyyy-MM-dd"))

# Step 4: Perform Analytics
#Calculate total revenue

total_revenue = joined_df.select(sum("price").alias("Total_revenue"))
total_revenue.show()

#Revenue per month
monthly_revenue = joined_df.groupBy(
    month("order_date").alias("month").sum("price").alias("Monthly_revenue")
)

#Top 5 selling products
top_products = joined_df.groupBy("product_id")\
                .agg(count("*").alias("total_sales"))\
                .orderBy("total_sales", ascending = False)\
                .limit(5)
top_products.show()

#Average order value
average_order = joined_df.groupBy("order_id")\
                .sum("price").alias("total_price")\
                .agg(avg("total_price")).alias("average_order_value")
average_order.show()

#step 5
hdfs_path = "hdfs://localhost:9000/ecommerce/analytics/total_revenue.parquet"
total_revenue.write.mode("overwrite").parquet(hdfs_path)

hdfs_path = "hdfs://localhost:9000/ecommerce/analytics/monthly_revenue.parquet"
monthly_revenue.write.mode("overwrite").parquet(hdfs_path)

hdfs_path = "hdfs://localhost:9000/ecommerce/analytics/top_five.parquet"
top_products.write.mode("overwrite").parquet(hdfs_path)

hdfs_path = "hdfs://localhost:9000/ecommerce/analytics/average_order.parquet"
average_order.write.mode("overwrite").parquet(hdfs_path)
            






