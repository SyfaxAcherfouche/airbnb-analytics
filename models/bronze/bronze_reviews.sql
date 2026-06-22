-- Ingestion brute des avis clients depuis S3
SELECT * FROM read_csv_auto(
    'https://logbrain-datasets.s3.eu-west-1.amazonaws.com/airbnb/reviews.csv'
)