set -x
BASEDIR=$1

# run for base case with all modules
cd $BASEDIR/s/synthea
./run_synthea -p 100 Uusimaa
# run synthea->omop 5.3.1
cd $BASEDIR/s/ETL-Synthea-Python/python_etl
export CDM_VERSION=5.3.1
python synthea_omop.py
# run synthea->omop 6.0
export CDM_VERSION=6.0
# zip up output
cd ./output/csv
zip ../all_csv.zip *.csv
cd ../..
cd ./output/fhir
zip ../all_fhir.zip *.json
cd ../..

for filename in $BASEDIR/s/synthea/build/resources/main/modules/*.json; do
    module=$(basename "$filename" .json)
    # cleanup previous run
    rm ./output/csv/*
    rm ./output/fhir/*
    # run synthea
    ./run_synthea -p 100 -m $module Uusimaa
    # run synthea->omop 5.3.1
    cd $BASEDIR/s/ETL-Synthea-Python/python_etl
    export CDM_VERSION=531
    python synthea_omop.py
    # run synthea->omop 6
    export CDM_VERSION=6
    cd $BASEDIR/s/ETL-Synthea-Python/python_etl
    python synthea_omop.py
    # zip up output
    cd ./output/csv
    zip ../${module}_csv.zip *.csv
    cd ../..
    cd ./output/fhir
    zip ../${module}_fhir.zip *.json
    cd ../..
done
