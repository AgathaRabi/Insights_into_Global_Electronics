---A. CUSTOMER ANALYSIS

--- A.1 DEMOGRAPHIC DISTRIBUTION

--1. No. of female customers:

SELECT COUNT(Gender) AS Female_Customers
FROM customers_data
WHERE Gender = 'Female';


--2. No. of male customers:

SELECT COUNT(Gender) AS Male_Customers
FROM customers_data
WHERE Gender = 'Male';


--3. Count of genderwise customers per country(who have bought goods):

SELECT customer_gend_country_dets.country, 
	SUM(CASE WHEN customer_gend_country_dets.gender = 'Male' THEN 1 END) AS "total_male_cust",
	SUM(CASE WHEN customer_gend_country_dets.gender = 'Female' THEN 1 END) AS "total_female_cust",
	count(customer_gend_country_dets.customer_key) as "total_customers"
FROM
(SELECT "Country" AS "country", "CustomerKey" AS "customer_key", "Gender" as "gender"
	, COUNT("Order Number") AS "no_of_orders"
	FROM customer_products_sales_data
	GROUP BY "Country","CustomerKey", "Gender") AS customer_gend_country_dets
GROUP BY customer_gend_country_dets.country;


--4. Proportion of genderwise orders per country:

SELECT "Country"
	, SUM(CASE WHEN "Gender" = 'Male' THEN 1 END) AS "no_orders_men"
	, SUM(CASE WHEN "Gender" = 'Female' THEN 1 END) AS "no_orders_women"  
	, COUNT("Order Number") AS "total_orders"
FROM customer_sales_data
GROUP BY "Country";


--5.How many times a particular customer made SOME purchase:

SELECT "CustomerKey",
COUNT("CustomerKey") AS times_ordered
FROM customer_sales_data
GROUP BY "CustomerKey"
ORDER BY COUNT ("CustomerKey") DESC
LIMIT 25;


--x. list of customers who ordered more than once:

SELECT "CustomerKey",
COUNT("CustomerKey") AS times_ordered
FROM customer_sales_data
GROUP BY "CustomerKey"
HAVING COUNT("CustomerKey") > 1
ORDER BY COUNT ("CustomerKey") DESC
LIMIT 25;

--X. customer location and average order value taking exchange rates into consideration:

SELECT "State", "City"
		, ROUND(AVG("Quantity" * "Unit Price USD" * "Exchange" )) as AVG_total_sales
FROM sales_exchange_rate_analysis
GROUP BY "State", "City"
ORDER BY AVG_total_sales DESC;
LIMIT 25

--6.List of customers, purchasing products from multiple branches/ online:

SELECT "CustomerKey"	
FROM customer_sales_data
GROUP BY 1
HAVING COUNT(DISTINCT "StoreKey")>1;


---- A.2 PURCHASE PATTERNS

--7. PREFERRED PRODUCTS:

SELECT "ProductKey", "Product Name"
		,COUNT("ProductKey") AS no_times_sold 			
FROM customer_products_sales_data
GROUP BY "ProductKey", "Product Name"
ORDER BY COUNT ('no_times_sold') DESC
LIMIT 100;


-- 8. PREFERRED CATEGORY OF PRODUCTS: ## also sales by product

SELECT "Category", COUNT("Category") AS no_times_sold
FROM customer_products_sales_data
GROUP BY "Category"
ORDER BY COUNT ('no_times_sold') DESC;


-- 9. average order value:

SELECT "Year"
		,COUNT("Order Number") AS no_orders
		,ROUND(SUM("Order Value")) AS Revenue
		,ROUND(AVG("Order Value" )) AS average_order_value	
FROM customer_sales_data
GROUP BY "Year"
ORDER BY "Year" ASC;

SELECT "Year", "AgeGroup"
		,COUNT("Order Number") AS no_orders
		,ROUND(SUM("Order Value")) AS Revenue
		,ROUND(AVG("Order Value" )) AS average_order_value	
FROM customer_sales_data
GROUP BY "Year", "AgeGroup"
ORDER BY "Year" ASC;


--10. Identifying countries with higher 'over40' customers and fewer physical stores:

SELECT "Country"
		,COUNT("AgeGroup") AS "over_40"
		, COUNT(DISTINCT "StoreKey") AS "store_count"
FROM customer_products_sales_stores_data
WHERE "AgeGroup" = 'Over 40' AND "StoreKey" != '0'
GROUP BY "Country" 
ORDER BY COUNT ("StoreKey") ASC;

---------------------------------------

SELECT COUNT("AgeGroup") AS "over_40"
		, COUNT(DISTINCT "StoreKey") AS "store_count"
FROM customer_products_sales_stores_data
WHERE "AgeGroup" = 'Over 40'
ORDER BY COUNT ("StoreKey") ASC;


------------------------------------------------------------------------------
--4. No. of male and female Customers who have ordered 10 & more than 10 times:

--5. No. of male and female Customers who have ordered from 5 to 9 times:



--- B. SALES ANALYSIS:

--x. to calculate the sales in each store:

SELECT "StoreKey"
		, ROUND(SUM ("Total Product Price")) AS "total_sales_USD"
FROM customer_products_sales_data
GROUP BY "StoreKey"
ORDER BY "StoreKey" ASC;

-----------------------------------------
SELECT "StoreKey"
		,"Country"
		, ROUND(SUM ("Total Product Price")) AS "total_sales_USD"
FROM customer_products_sales_data
GROUP BY "StoreKey", "Country"
ORDER BY "total_sales_USD" DESC;

---------------------------------------

--x.countries and their online sales:

SELECT "StoreKey"
		,"Country"
		, ROUND(SUM ("Total Product Price")) AS "total_sales_USD"
FROM customer_products_sales_data
WHERE "StoreKey" = 0 
GROUP BY "StoreKey", "Country"
ORDER BY "total_sales_USD" DESC;

--x. countries and their offline sales:

SELECT "StoreKey"
		,"Country"
		, ROUND(SUM ("Total Product Price")) AS "total_sales_USD"
FROM customer_products_sales_data
WHERE "StoreKey" != 0 
GROUP BY "StoreKey", "Country"
ORDER BY "total_sales_USD" DESC;


--X. To calculate average sales per store PER country: # Geographical analysis

SELECT
country_sales.country, 
country_sales.store_count, 
country_sales.total_sales_usd,
ROUND(country_sales.total_sales_usd/ country_sales.store_count) AS "avg_sales_per_store"
FROM
(SELECT "Country" AS "country", COUNT (DISTINCT "StoreKey") AS "store_count",
ROUND(SUM ("Total Product Price")) AS "total_sales_usd"
FROM customer_products_sales_data
GROUP BY "country"
ORDER BY COUNT ("StoreKey") DESC) AS country_sales;


--x. No of Online purchases/ orders in each country:

SELECT "Country"
		, COUNT(DISTINCT "CustomerKey") AS "customer_count"
FROM customer_products_sales_stores_data
WHERE "StoreKey" = '0'
GROUP BY "Country" 
ORDER BY COUNT ("CustomerKey") DESC;

--x. No. of OFFLINE purchases/ orders in each country:

SELECT "Country"
		, COUNT(DISTINCT "CustomerKey") AS "customer_count"
FROM customer_products_sales_stores_data
WHERE "StoreKey" != '0'
GROUP BY "Country" 
ORDER BY COUNT ("CustomerKey") DESC;


--x. no. of offline and online PURCHASES in each country:

SELECT mode_purchase_dets.country, 
	SUM(CASE WHEN mode_purchase_dets.storekey != '0' THEN 1 END) AS "total_offline_purchases",
	SUM(CASE WHEN mode_purchase_dets.storekey = '0' THEN 1 END) AS "total_online_purchases",
	COUNT(mode_purchase_dets.customer_key) as "total_purchases"
FROM
(SELECT "Country" AS "country", "CustomerKey" AS "customer_key", "StoreKey" as "storekey"
	FROM customer_products_sales_stores_data
	GROUP BY "Country","CustomerKey", "StoreKey") AS mode_purchase_dets
GROUP BY mode_purchase_dets.country;

--x. stores without sales:





--X. To calculate frequency of purchase:







--x. having identified one country

--- D. STORES ANALYSIS:

--x. the stores without any sales

SELECT "StoreKey", "Order Value"
FROM stores_sales_data
GROUP BY "StoreKey", "Order Value"
HAVING "Order Value" = '0';


--X. To calculate no. of stores per country:

SELECT "Country", COUNT (DISTINCT "StoreKey") AS "store_count",
ROUND(SUM ("Total Product Price")) AS "total_sales_USD"
FROM customer_products_sales_data
GROUP BY "Country"
ORDER BY COUNT ("StoreKey") DESC;


--x. to calculate the sales in each store:

SELECT "StoreKey"
		, ROUND(SUM ("Total Product Price")) AS "total_sales_USD"
FROM customer_products_sales_data
GROUP BY "StoreKey"
ORDER BY "StoreKey" ASC;

--X. To calculate average sales per store PER country: # Geographical analysis

SELECT
country_sales.country, 
country_sales.store_count, 
country_sales.total_sales_usd,
ROUND(country_sales.total_sales_usd/ country_sales.store_count) AS "avg_sales_per_store"
FROM
(SELECT "Country" AS "country", COUNT (DISTINCT "StoreKey") AS "store_count",
ROUND(SUM ("Total Product Price")) AS "total_sales_usd"
FROM customer_products_sales_data
GROUP BY "country"
ORDER BY COUNT ("StoreKey") DESC) AS country_sales;

--x. no. of customers visiting each stores:

SELECT "Country"
		,"StoreKey"
		,COUNT(DISTINCT "CustomerKey") AS "customer_count"
FROM customer_products_sales_data
GROUP BY "Country", "StoreKey"
ORDER BY "StoreKey" ASC;

--x. List of customers purchasing from multiple stores/ online:(?????)

SELECT "CustomerKey"	
FROM customer_sales_data
GROUP BY 1
HAVING COUNT(DISTINCT "StoreKey")>1;

--x. Count of customers purchasing from multiple stores/ online: (????)

SELECT COUNT (repetitive_customer_data.rep_customers)
FROM (SELECT "CustomerKey"	AS "rep_customers"
	FROM customer_sales_data
	GROUP BY "rep_customers" 
	HAVING COUNT(DISTINCT "StoreKey")>1) AS repetitive_customer_data;


--X. no. of customers who havent made any purchase:

SELECT COUNT("CustomerKey")
FROM nil_purchase_customers
WHERE "Order Number" = '0';

--x. currency and sales:

SELECT "Country"
		, COUNT(DISTINCT "CustomerKey") AS "no of customers"
		, COUNT(DISTINCT "ProductKey") AS "no of products"
		,"Currency Code"
FROM customer_products_sales_stores_data
GROUP BY "Country", "Currency Code"
ORDER BY "no of products" DESC;