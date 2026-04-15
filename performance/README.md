# Performance

## Generate synthetic datasets

1. Change folder
```bash
cd performance/generate_synthetic_data
```

2. Build the docker image and run the docker container
```bash
docker build . -t generate_synthetic-data
docker run --name run_generate_synthetic_data -it generate_synthetic-data bash
```

3. Generate synthetic datasets

Run the command-line python script with the following options:
- `template_id`: identifies the template used to generate the data.\
Currently supported templates are: `woonsituatie_2024`, `polsfrequentie_2024`
- `n_patient`: the number of patients (bsn number) to generate
- `n_rows_per_patient`: the number of row to generate per patient
- `random_seed`: If provided, sets the seed for random value generation to ensure reproducibility

```bash
python generate_synthetic_data.py --template_id="woonsituatie_2024" --n_patients=1000 --n_rows_per_patient=1 --random_seed=42
```

4. Exit the container: `Ctrl+D`

5. Copy the `synthetic_dataset` directory into the local folder
```bash
docker cp run_generate_synthetic_data:/code/synthetic_dataset ./synthetic_dataset
```

6. Delete the container if necessary
```bash
docker rm run_generate_synthetic_data
```

## Run the ETL stack with synthetic data

1. In `docker-health`, place a synthetic dataset file in `data/test-demo-data/csv/demo-data`
and replace it with the original file (e.g., `woonsituatie_2024.csv`)

2. Disable templates that are not required for the performance run in the `TEMPLATE_IDS` config variable (`deploy/base/openehr-nodes/test/etl-zib/etl-config/config.yaml`)

3. Tip: Use elk to monitor data loading
```bash
./dh.sh apply local/ops
```

4. Run the ETL stack of the `test` node
```bash
./dh.sh apply -s local/node-test
```
