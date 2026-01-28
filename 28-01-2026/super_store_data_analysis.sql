-- Write a query to fetch all orders where sales are greater than the overall average sales.
SELECT 
Order_ID
FROM order_data1
WHERE Sales > (Select AVG(Sales) FROM order_data1)

-- Write a query to retrieve the top 5 cities by total sales, ordered from highest to lowest.
SELECT TOP 5
    City,
    SUM(Sales) AS TotalSales
FROM
    order_data1
GROUP BY
    City
ORDER BY
    TotalSales DESC

-- Write a query to find customers who have placed more than 5 orders, along with their total sales.
SELECT 
Customer_ID,
customer_name,
SUM(Sales) AS Total_Sales
FROM order_data1
GROUP BY Customer_ID, Customer_Name
HAVING COUNT(order_id) > 5

--Write a query to calculate total sales and total number of orders for each segment, sorted by total sales.
SELECT 
SUM(Sales) AS Total_Sales,
COUNT(order_id) AS Total_Orders, 
Segment
FROM order_data1
GROUP BY Segment
ORDER BY SUM(Sales) ASC

--Write a query to rank cities within each country based on total sales using a window function. 
SELECT 
City,
country,
SUM(Sales) AS total_sales,
RANK() OVER (PARTITION BY country ORDER BY SUM(Sales)) AS Rank
FROM order_data1
GROUP BY Country, City

--Write a query to identify orders where the shipping duration exceeds 4 days
SELECT 
    order_id,
    order_date, 
    Ship_Date
FROM order_data1
WHERE DATEDIFF(day, Order_Date, Ship_Date) > 4

-- Write a query to calculate the number of orders per month, grouped by year and month using Order_Date.
SELECT
  YEAR(Order_date) AS Year,
  DATENAME(month,Order_date) AS Month, 
  COUNT(order_id) AS total_orders
FROM order_data1
GROUP BY YEAR(order_date), DATENAME(month,order_date)

-- Write a query to identify orders where the ship date is earlier than the order date.
SELECT
    Order_ID,
    Order_date,
    Ship_Date
FROM order_data1
WHERE Ship_Date < Order_Date

--Write a query to calculate the percentage contribution of each ship mode based on the total number.
SELECT 
    Ship_Mode,
    COUNT(order_id) AS total_orders,
    CAST(COUNT(order_id) * 100.0 / SUM(COUNT(order_id)) OVER() AS DECIMAL(5,2)) AS percentage_contribution
FROM order_data1
GROUP BY Ship_Mode
ORDER BY percentage_contribution DESC;



        




