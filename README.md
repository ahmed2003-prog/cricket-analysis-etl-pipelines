1. Data Configuration
Download Dataset
Source: Kaggle
Dataset Name: "ODI Cricket Match ESPN Data (Jan 2020 - March 2025)"
Download and extract the dataset files.
Perform Preprocessing on Dataset Files
Clean missing values
Convert data types if needed
Ensure consistency across different CSV files
Create an Amazon S3 Bucket and Upload CSV Files
Navigate to AWS S3 Console
Create a new bucket: cricket-bucket
Upload dataset files into respective directories:
s3://cricket-bucket/batting_data/
s3://cricket-bucket/bowling_data/
s3://cricket-bucket/fielding_data/
s3://cricket-bucket/squads/

2. Setup Athena
Set Up an S3 Bucket for Athena Query Results
Go to AWS S3
Create a new bucket: cricket-athena-results
Configure settings:
Region: Same as cricket-bucket
Block Public Access: Enabled
Versioning: Optional
Encryption: Enabled
Click Create bucket
Create an AWS Glue Crawler
Go to AWS Glue Console
Navigate to AWS Glue > Crawlers
Click "Add Crawler"
Enter Crawler Name: cricket-crawler
Choose Data Source:
Select S3
Enter bucket path: s3://cricket-bucket/
Set IAM Role:
Choose Create New Role (AWS will generate required permissions)
Configure Output Database:
Select existing cricket-db or create a new database cricket-db
(Optional) Schedule Crawler: On-demand or periodic
Click Create, then Run Crawler

3. Data Integration & Transformation
Create Tables & Views in Athena
Run SQL queries to create tables:
Batting Data Table
Bowling Data Table
Fielding Data Table
Unified Views combining these datasets
Create a Unified Cricket Performance Table
Join Batting & Bowling Data for Player Performance
Join Player Performance with Fielding Data
Create a Match-Wise Performance View
Partitioning & Exporting to S3
Store data efficiently in Parquet format
Save processed data to: s3://cricket-bucket/cricket_performance_partitioned/
Partition by year to improve Athena query performance

4. Automate S3 Export for New Data
Create an IAM Role with Permissions
AWSLambdaBasicExecutionRole
AmazonS3FullAccess
AmazonAthenaFullAccess
Deploy Lambda Function for Automatic Data Updates
Triggered when new data lands in S3
Runs MSCK REPAIR TABLE to detect new partitions
Refreshes Athena metadata using CALL system.refresh_metadata()
Ensures queries always use the latest data
Increase Lambda Timeout
Navigate to AWS Lambda → Select your function
Go to Configuration → General Configuration
Increase timeout to 60 seconds (or more)
Click Save changes
Create an EventBridge Rule (S3 to Lambda Trigger)
Go to AWS EventBridge
Create a new rule: S3_New_Data_Trigger
Configure Event Source:
Type: S3
Detail Type: Object Created
Bucket: cricket-bucket
Set Target to your Lambda function
Click Create

5. Build Streamlit Dashboard for Cricket Insights
Install Required Libraries
pip install streamlit boto3 pandas pyathena

Set Up Streamlit Environment
Create a new file: dashboard.py
Create a new IAM user with:
AmazonAthenaFullAccess
AmazonS3FullAccess (restrict to s3://cricket-athena-results/ if needed)
AWSGlueConsoleFullAccess (if using Glue Data Catalog)
Copy Access Key & Secret Key
Run aws configure and enter credentials
Implement Key Analytics and Insights
Top Performers Leaderboard
Player Comparison Tool
Batting Performance Analysis
Bowling Performance Analysis
Fielding Insights (Dismissals - Catches, Stumpings, etc.)
Match Outcome Predictions using Machine Learning

6. Complete Documentation
Summary of Progress
Successfully set up a structured data pipeline using AWS S3, Glue, and Athena
Automated the ingestion of new cricket match data with AWS Lambda & EventBridge
Built a real-time dashboard using Streamlit for interactive data visualization
Next Steps
Optimize query performance by fine-tuning partitions and indexing
Enhance visualizations with Power BI / Streamlit for advanced insights
Expand ML models for player and team performance predictions

End of Documentation

