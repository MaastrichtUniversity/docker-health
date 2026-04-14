import os
import click
import pandas as pd

from src.templates.woonsituatie import generate_synthetic_woonsituatie
from src.utils import InputTemplateID, generate_bsn


@click.command()
@click.option("--template_id", required=True, type=InputTemplateID)
@click.option("--n_rows", default=1, type=int)
def main(template_id: InputTemplateID, n_rows: int):
    if template_id == InputTemplateID.WOONSITUATIE_2024:
        generator = generate_synthetic_woonsituatie

    used_bsn = []
    rows = []
    for _ in range(n_rows):
        bsn = generate_bsn(used_bsn)
        rows.append(generator(bsn))
        used_bsn.append(bsn)

    df = pd.DataFrame(rows)

    outdir = "synthetic_dataset"
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    filename = os.path.join(outdir, f"{template_id}_synthetic_n={n_rows}.csv")
    df.to_csv(filename, index=False)
    print(df.tail())


if __name__ == "__main__":
    main()
