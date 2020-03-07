import os
from os import listdir
from os.path import isdir, isfile, join
import sys

if len(sys.argv) <2:
    print("BASEDIR should be set")
    exit(1)
basedir = sys.argv[1]
path = basedir + "/s/synthea/build/resources/main/modules/"
files = [f for f in listdir(path) if isfile(join(path, f))]
# add some extra running types
modules=[]
#modules.append('*')
#modules.append('cancer*')
for file in files:
    modules.append(os.path.splitext(file)[0])
print(modules)    

for module in modules:
    # cleanup previous run
    os.chdir(basedir + '/s/synthea')
    if (isdir('output')):
        filesToRemove = [f for f in os.listdir('output')]
        for f in filesToRemove:
            os.remove(os.path.join(BASE_OUTPUT_DIRECTORY, f))
    # run synthea
    os.system("./run_synthea -p 100 -m " + module + ' Uusimaa')
    # run synthea->omop 5.3.1
    os.chdir(basedir + '/s/ETL-Synthea-Python/python_etl')
    #export CDM_VERSION=531
    os.system("python synthea_omop.py")
    # run synthea->omop 6
    #export CDM_VERSION=6
    #cd $BASEDIR/s/ETL-Synthea-Python/python_etl
    #python synthea_omop.py
    # zip up omop output
    os.chdir(basedir + '/s/ETL-Synthea-Python/output')
    os.system("zip ../" + module + "_531.zip *.csv")
    # zip up synthea output
    os.chdir(basedir + '/s/synthea/output/csv')
    os.system("zip ../" + module + "_csv.zip *.csv")
    os.chdir(basedir + '/s/synthea/output/fhir')
    os.system("zip ../" + module + "_fhir.zip *.csv")
