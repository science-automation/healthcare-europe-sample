set -x
BASEDIR=$1
cd $BASEDIR

# run for base case with all modules
./run_synthea -p 100 Uusimaa
cd ./output/csv
zip ../all_csv.zip *.csv
cd ../..
cd ./output/fhir
zip ../all_fhir.zip *.json
cd ../..

for filename in $BASEDIR/build/resources/main/modules/*.json; do
    module=$(basename "$filename" .json)
    rm ./output/csv/*
    rm ./output/fhir/*
    ./run_synthea -p 100 -m $module Uusimaa
    cd ./output/csv
    zip ../${module}_csv.zip *.csv
    cd ../..
    cd ./output/fhir
    zip ../${module}_fhir.zip *.json
    cd ../..
done
