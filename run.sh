set -x
BASEDIR=$1
cd $BASEDIR

mkdir -p $BASEDIR/output/csv
mkdir -p $BASEDIR/output/fhir

# run for base case with all modules
./run_synthea -p 100 "Uusimma"
cd ./output/csv
zip ../all_csv.zip *.csv
cd ../..
cd ./output/fhir
zip ../all_fhir.zip *.json
cd ../..

mkdir -p $BASEDIR/output/csv
mkdir -p $BASEDIR/output/fhir
for filename in $BASEDIR/build/resources/main/modules/*.json; do
    module=$(basename "$filename" .json)
    pwd
    rm ./output/csv/*
    rm ./output/fhir/*
    ./run_synthea -p 100 -m $module "Uusimma"
    cd ./output/csv
    zip ../${module}_csv.zip *.csv
    cd ../..
    cd ./output/fhir
    zip ../${module}_fhir.zip *.json
    cd ../..
done
