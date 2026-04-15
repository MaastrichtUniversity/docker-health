import os
import time
import click
import pandas as pd
from faker import Faker
from numpy.random import seed
from datetime import datetime, timedelta

from src.templates.polsfrequentie import generate_synthetic_polsfrequentie
from src.templates.woonsituatie import generate_synthetic_woonsituatie
from src.utils import InputTemplateID, generate_bsn, generate_random_full_date


@click.command()
@click.option("--template_id", required=True, type=InputTemplateID)
@click.option("--n_patients", default=1, type=int)
@click.option("--n_rows_per_patient", default=1, type=int)
@click.option("--random_seed", type=int)
def main(template_id: InputTemplateID, n_patients: int, n_rows_per_patient: int, random_seed: int):

    execution_start_time = time.perf_counter()

    print(f"Generate dataset for: template_id={template_id}, n_patients={n_patients}, n_rows_per_patient={n_rows_per_patient}, random_seed={random_seed}")

    if random_seed:
        seed(random_seed)
        Faker.seed(random_seed)

    global generator
    if template_id == InputTemplateID.WOONSITUATIE_2024:
        generator = generate_synthetic_woonsituatie
    elif template_id == InputTemplateID.POLSFREQUENTIE_2024:
        generator = generate_synthetic_polsfrequentie

    used_bsn = []
    rows = []
    for _ in range(n_patients):
        bsn = generate_bsn(used_bsn)
        used_bsn.append(bsn)
        date_time_list = []
        for _ in range(n_rows_per_patient):
            if not date_time_list:
                date_time = generate_random_full_date()
            else:
                # A new row must have a more recent date_time value
                date_time = generate_random_full_date(
                    start_date=date_time_list[-1], end_date=date_time_list[-1] + timedelta(days=1)
                )
            date_time_list.append(datetime.fromisoformat(date_time))
            rows.append(generator(bsn, date_time))

    df = pd.DataFrame(rows)

    outdir = "synthetic_dataset"
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    filename = os.path.join(outdir, f"{template_id}_synthetic_p={n_patients}_n={n_rows_per_patient}_s={random_seed}.csv")
    df.to_csv(filename, index=False)

    print(df.tail())

    execution_end_time = time.perf_counter()
    print(f"\nTotal execution time: {execution_end_time - execution_start_time:.4f} seconds\n\n")


if __name__ == "__main__":
    main()
