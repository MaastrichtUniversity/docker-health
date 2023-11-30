# Code generator for DataClass

## Install package(s) in a venv

```
cd data_classes
sudo apt-get install python3-virtualenv
python3 -m virtualenv --python=python3 venv3
source ./venv3/bin/activate

pip install xsdata-pydantic[cli,lxml,soap]
pip install 'datamodel-code-generator[http]'

# To exit the venv
# deactivate
```

## xsdata
```
cd data_classes

xsdata generate ../externals/hdp-models/templates/vital_signs.opt --structure-style single-package --order  --package tests.odt.models

xsdata generate ../externals/hdp-models/templates/vital_signs.t.json  --structure-style single-package --order --package tests.json.models 

xsdata generate ../ETL/data/compositions/locatable/vital_signs_20231122085528_000001_1.json --structure-style single-package  --package tests.compositions.models 
```


## datamodel-code-generator


```
cd data_classes

datamodel-codegen  --input ../hdp-models/templates/vital_signs.t.json --input-file-type json --output model_vital_signs.py

datamodel-codegen  --input ../ETL/data/composition/vital_signs_20231025075308_000001_1.json --input-file-type json --output model_compositions_vital_signs.py
```

