hdfs dfs -mkdir -p /user/$(whoami)
wget https://github.com/AFAgarap/ecommerce-reviews-analysis/raw/master/Womens%20Clothing%20E-Commerce%20Reviews.csv  --output-document=reviews.csv
sed -i "s/,Clothing ID,/recNo,Clothing ID,/" reviews.csv
hdfs dfs -put -f "reviews.csv"
