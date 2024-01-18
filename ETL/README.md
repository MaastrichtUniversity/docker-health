# Health Data Plateform -- ETL

ETL python service to communicate with the EHRbase API.

The `run [input_format]` command permits the extraction, tranformation (using a Java REST API) and loading of openEHR compositions.
Available `input_format` are csv, json, fhir, ccda and sql.

## Help function

```
python ETL.py --help
Usage: ETL.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get-all-ehr-id      Get all EHR ID on a specific openEHR instance
  list-all-templates  Print all template available on the server
  run                 Runs all ETL for a single patient.
```
