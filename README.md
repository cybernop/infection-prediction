# Content
here you can find all code and logic that you need to update this dashboard:
https://public.tableau.com/profile/max.ehrlich#!/vizhome/InfectionDevelopment/Influencecontactrate?publish=yes

the dashboard shows a timeseries about the development of infected people in germany dependend oon Bundesland and Landkreis and dependend on reduction of our social contacts. 
it shows the strong impact on reducing social contacts on the number of infected people and the number of needed hospital beds, which will have a big influence in future over-utilization of these beds and the possibility of enough medical supply.

# How to update Dashboard
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
#### raw data
* sheet: Landkreis Einwohner
  * content: Einwohner pro Landkreis und Bundesland
  * source: https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0

* sheet: Infektionen
  * content: Anzahl Infektionen nach Meldedatum, Landkreis, Geschlecht, Altersgruppe
  * source: https://npgeo-corona-npgeo-de.hub.arcgis.com/datasets/dd4580c810204019a7b8eb3e0b329dd6_0

* sheet: dates_all
  * content: Eine Zahle pro Datum vom 2.1.2020 bis zum 31.5.2021

#### intermediate tables
* sheet: aggregated
  * content: Anzahl Infektionen aggregiert auf Meldedatum und Landkreis
  * source: sheet Infektionen

* sheet: 

#### final table for tableau upload
* sheet: tableau_landkreis
  * content: 
    * Eine Zeile pro Tag und Landkreis (manuelle Erzeugung aus sheets: dates_all und all_regions)
    * Berechnung der Anzahl gleichzeitig Infizierten in der Zukunft
    * Berechnung der Anzahl gleichzeitig Infizierten mit Krankenbettbedarf in der Zukunft
    * Berechnung der Anzahl gleichzeitig Infizierten mit Krankenbettbedarf und schwerem Verlauf in der Zukunft
    * Berechnung der Anzahl verfügbarer Krankenbetten pro Landkreis und Tag
  * source: other sheets in Calculations.xlsx

#### graphics for quick check
* sheet: results_quick_check
  * content: pivot-tables and graphics to check model prediction, before you upload files to tableau

## add data to tableau dashboard
* open sheet tableau_landkreis
* adjust parameter in cell B3 to 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100%
* for every adjustment: save table (starting in cell D9, ending in cell Q200733) in tableau_source.xlsx in sheet "x%"
* add a further column with the value of the adjusted parameter
* format columns
* save every sheet as csv file tableau_result_x.csv with x as percentage of adjusted parameter
* upload these csv-files into tableau public and union them together
