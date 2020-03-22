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

## train model
* file: Calculations.xlsx, sheet: model training
* import new dataset in line 3
* adjust model parameters in column E, so that the model still fits to latest developments (check model fit in graphic in cell I44)

## create dataset with predicted values (datasource for tableau dashboard)
* file: Calculations.xlsx
### raw data
* sheet: Landkreis Einwohner
* content: Einwohner pro Landkreis und Bundesland
* source: https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0

* sheet: Infektionen
* content: Anzahl Infektionen nach Meldedatum und Landkreis
* source: https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0

## add data to tableau dashboard
