# Pre-steps (Not required)

- Downloaded Vital Signs template from https://ckm.openehr.org/ckm/templates/1013.26.380

    Rename file to `vital_signs.opt`


-   Generate example composition trough https://github.com/ppazos/openEHR-OPT

    `./opt.sh ingen vital_signs.opt . 1 json`

-   Generate synthea sample set for single patient
    ```
    exporter.hospital.fhir.export = false
    exporter.practitioner.fhir.export = false
    exporter.csv.export = true
    exporter.fhir.export = false
    generate.default_population =  1
    generate.only_alive_patients = true
    exporter.csv.folder_per_run = true
    exporter.baseDirectory = /tmp/synthea_output
    ```

# Python
Packages required
```
requests
pandas
matplotlib
```
