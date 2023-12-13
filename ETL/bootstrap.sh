#! /bin/bash
python ETL.py --help
# echo "Running demo ETL"
python ETL.py run

echo -e "\nGeting all templates on system"
python ETL.py list-all-templates

echo -e "\nGetting all ehr id on system"
python ETL.py get-all-ehr-id
# Make the bootstrap process persistent
sleep infinity

