-- Ingestion brute des logements depuis S3
SELECT * FROM read_csv_auto(
    'https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/listings.csv'
)