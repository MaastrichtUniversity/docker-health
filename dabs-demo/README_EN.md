# DABS dashboard demo

Showcase: search for patient by BSN → open dossier → DABS tab → federated data from MUMC and ZIO, visualized per data type.

Runs on the Python standard library and vanilla JS. **No `pip install`, no `npm install`, no build step.**

## Starting

```bash
python3 server.py
```

Open http://localhost:8800 and search for **999990603**.

| Flag | Meaning |
|---|---|
| `--dataset faithful` | *(default)* exactly the records the federation API returns. Few measurement points. |
| `--dataset rich` | longer measurement series so the graphs show trends. Enriched demo data, labelled in the UI. |
| `--mode fixture` | *(default)* fixed responses |
| `--mode live` | real federation API, falling back to fixtures per endpoint |
| `--timeout 30` | seconds per federation call before falling back |
| `--port 8800` | port |
| `--federation-base <url>` | base URL of the federation API of your own node |
| `--key` / `--btg-key` | X‑API‑Key and break‑the‑glass key of that node |
| `--host 127.0.0.1` | `0.0.0.0` to share the demo on the network |

The last three differ per workplace and can also be supplied as environment variables: `DABS_FEDERATION_BASE`, `DABS_KEY`, `DABS_BTG_KEY`.

## Checking the environment

```bash
python3 tools/check_omgeving.py
```

The script walks through four layers – machine, federation API, your own EHRbase, the four data endpoints – and reports where something goes wrong. See `../OVERZETTEN.md` for the full step‑by‑step guide to run this project on another PC.

For a showcase with meaningful graphs:

```bash
python3 server.py --dataset rich
```

## Running the demo

1. **Search** — enter BSN `999990603`, press Enter or *Search*.
2. **Dossier** — click the found patient.
3. **DABS tab** — click DABS in the tab bar; the four endpoints are fetched in parallel.
4. **Break‑the‑glass** — toggle the switch on the right side of the federation strip.

Two switches in the federation strip:

| Switch | Effect |
|---|---|
| **Break‑the‑glass** | Turns off the informed‑consent filter. See the note below. |
| **Only source data** | Retrieves directly from the federation endpoints — no fixtures, no fallback, no derived values. If the nodes return nothing, the dashboard shows nothing. |

### Perspective: ZIO

The UI is an application for ZIO staff. They always have access to their own data; data from other care providers becomes visible only after consent or break‑the‑glass.

The fixtures follow that logic:

| State | What you see |
|---|---|
| Break‑the‑glass **off** | only ZIO — MUMC is *no consent* |
| Break‑the‑glass **on** | ZIO plus MUMC, with the number of unlocked records shown in the banner |

> **This is a demo model, not literally what the API does with these demo data.** In `test_federation_rest.py` patient 999990603 has consent = true at MUMC (line 248), which means MUMC would also appear from ZIO without break‑the‑glass; `TestZioClient` therefore uses the break‑the‑glass expectations as the normal outcome. That is an oddity of the demo dataset, not of the privacy model. For the showcase we model the general case — own node always, other nodes only after consent — because that best demonstrates the break‑the‑glass behaviour. With `--mode live` you get whatever the nodes actually return.

`Only source data` is the honesty button: everything you see with it comes directly from the nodes at that moment. If the cluster is down, this mode yields an empty screen with an explanatory message. If it is off, the demo runs on fixtures and the dashboard indicates that as well — grey `fixture` chips and a *No live data* banner.

Step 4 is the most dramatic moment. Without break‑the‑glass ZIO has *no consent* and the dashboard shows a single source. Turning the switch on brings ZIO's records, the BMI tile jumps to a value that combines weight from one source with height from another, and the source comparison shows that MUMC and ZIO disagree on seven fields — different birthdate, gender, name, etc.

You can also deep‑link: `http://localhost:8800/?bsn=999990603&tab=dabs`.

## What you see

- **Federation strip** — per node whether it delivered data, was blocked by consent, or was unreachable.
- **Patient data** — for each variable the latest value across all sources. Each field is sorted individually, so the address may come from ZIO while the name comes from MUMC: the result is a composition of both source systems. Every value carries a source badge and the modification date; if another source has a differing value it is shown with a `≠`. A source that has no value for a field is skipped, allowing an older record to fill a gap left by a newer one.
  > **Note — `_veld_gewijzigd` is modeled, not source data.** `PatientDTO2024` only carries a single timestamp (`start_time`, which for this patient equals the birthdate), so per‑field recency cannot be derived from the federation API. The fixtures therefore contain a `_veld_gewijzigd` map per source. The frontend uses it when present and otherwise falls back to `start_time` — as soon as the source provides real per‑field timestamps this works without code changes. In the *Only source data* mode this field does not exist because everything comes directly from the endpoints.
- **KPI tiles** — latest blood pressure, weight, height, plus derived BMI with source attribution.
- **Blood pressure** — time series with reference bands. One continuous line per measurement type, spanning all sources: that is the patient’s trajectory. Line style distinguishes the measurement type (solid systolic, dashed diastolic); the line itself is muted so the data points stand out.
- **Weight evolution** — likewise a single combined line over all sources.
- **Source recognition in the graphs** — each data point bears the source in shape **and** colour: a blue circle is MUMC, a brown rhombus is ZIO. This also applies to live data; new nodes get their own colour via `BRON_KLEUR` in `web/app.js`.
- **Raw response** — the normalized JSON.

## Structure

```
server.py                BFF + static server
  /api/patient/<bsn>     ?requester=&btg=&dataset=&bron=   → normalized model
                         bron=nodes: only live endpoints, no fallback
  /api/config
fixtures/                faithful set
fixtures-rich/           enriched set
tools/make_fixtures.py   generates both sets
web/                     index.html, styles.css, app.js
```

The BFF fetches the four endpoints in parallel, normalizes 200‑ and 503‑responses to the same model, flattens the per‑node lists into series with a `_source` field and determines per node the status `ok` / `consent_blocked` / `offline`. API keys remain server‑side.

## Live mode

```bash
python3 server.py --mode live
```

Queries `http://federation.zio.local.dh.unimaas.nl`. One node is sufficient: the federation API of a node queries its own EHRbase and forwards to the other nodes. `key1` belongs to MUMC; ZIO rejects it with a 401, and `btgkey1` disables the consent filter.

If an endpoint returns nothing, the BFF falls back to the fixture for that endpoint and shows the status strip *fixtures (federation unreachable)*. Thus the demo does not break if a node disappears.

**Status as of 19‑08‑2026:** the federation APIs are running, but their EHRbase pods are OOM‑killed and the ETL job has not completed, so live mode returns no records. See `../PLAN.md` §0 for the diagnosis. The fixtures are therefore the working demo route.

## Refreshing fixtures

Once the cluster provides data, you can capture the real responses:

```bash
for ep in Patient Bloeddruk Lichaamsgewicht LichaamsLengte; do
  curl -s -H "X-API-Key: btgkey1" \
    "http://federation.zio.local.dh.unimaas.nl/$ep?bsn=999990603&requester=Rolf" \
    -o "fixtures/$ep.btg.json"
done
```

Without `btg` in the filename and with `key1` for the variant that includes the consent filter.