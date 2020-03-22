# infection-prediction
## read datasource automatically and save it to your wished S3 path
architecture around is not build yet (AWS Account with S3 bucket and daily running Lambdas)

* file: data_importer.zip

run in command line:
```
python -m data_importer  --output-mode s3 --output-bucket cluno-data-raw --output-key test1/key.csv
```



## read datasource from local path and transform data
* file: model.py
* run manually and adjust pathname (line 23)
* code can be added to data_importer.zip for fully automated data preparation
