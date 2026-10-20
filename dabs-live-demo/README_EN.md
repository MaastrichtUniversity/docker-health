# DABS dashboard demo (live)

Showcase: search for patient by BSN → open dossier → DABS tab → federated data from the
connected nodes, visualized per data type.

Runs on the Python standard library and vanilla JS. **No `pip install`, no `npm install`,
no build step.**

This version is **live-only**: there are no fixtures and no fallback. The BFF always queries
the real federation API. If it returns nothing, the dashboard shows nothing and explains why
— an empty screen with a reason is preferred over invented data.

## Starting

```bash
python3 server.py
```

Open http://localhost:8800 and search for **999990603**.

| Flag | Meaning |
|---|---|
| `--host 0.0.0.0` | listen address; `0.0.0.0` to share the demo on the network |
| `--port 8800` | port |
| `--timeout 30` | seconds per federation call before it aborts |
| `--federation-base <url>` | base URL of the federation API of your own node |
| `--key` / `--btg-key` | X-API-Key and break-the-glass key of that node |
| `--eigen-node <name>` | name of the own node; by default derived from the federation URL |

The federation URL and keys differ per workplace and can also be supplied as environment
variables:

| Variable | Meaning |
|---|---|
| `DABS_FEDERATION_BASE` | base URL of the federation API of your own node |
| `DABS_KEY` | X-API-Key used to query your own node |
| `DABS_BTG_KEY` | break-the-glass key that disables the informed-consent filter |
| `DABS_NODES` | nodes the federation is supposed to have (default `zio,mumc,envida,vitala`) |

A flag takes precedence over its environment variable. **Keys are supplied per workstation and
are never committed to this repository.** They stay server-side: the browser never sees them.

## Running the tests

```bash
python3 -m unittest discover -s tests
```

The integration tests start `server.py` against a mock federation on a free port; they never
touch the real federation API.

## Checking the environment

```bash
python3 tools/check_omgeving.py
```

The script walks through four layers — machine, federation API, your own EHRbase, the four
data endpoints — and reports where something goes wrong. It uses the same
`DABS_FEDERATION_BASE`, `DABS_KEY` and `DABS_BTG_KEY` as the server, so you do not have to
fill them in twice.

## Running the demo

1. **Search** — enter BSN `999990603`, press Enter or *Search*.
2. **Dossier** — click the found patient.
3. **DABS tab** — click DABS in the tab bar; the four endpoints are fetched in parallel.
4. **Break-the-glass** — toggle the switch on the right side of the federation strip.

Two switches in the federation strip:

| Switch | Effect |
|---|---|
| **Break-the-glass** | Disables the informed-consent filter: queries with `--btg-key` instead of `--key`. |
| **Only source data** | The app always queries the federation endpoints directly; this mode additionally hides the derived BMI tile so that only raw source values remain. |

### Perspective: the own node

The UI is an application for staff of their own node (ZIO by default). They always have
access to their own data; data from other care providers becomes visible only after consent
or break-the-glass. The own node is therefore queried without the informed-consent filter and
carries the *eigen node* marker in the strip.

Because there are no fixtures anymore, the app shows exactly what the nodes return at that
moment:

| State | What you see |
|---|---|
| Break-the-glass **off** | the own node delivers; other nodes without consent show *no consent* |
| Break-the-glass **on** | the consent filter is off and every node that has data appears |

> This is the privacy model, not a fixed outcome. The data are real: what you see depends on
> which nodes answer and what consent allows. That is precisely the point of break-the-glass.

`Only source data` is the honesty button: everything you see came directly from the nodes at
that moment. Because the app is live-only, that now holds for every view. If the nodes return
nothing, the dashboard shows an empty screen with the reason — no invented series.

Step 4 is the most dramatic moment. Without break-the-glass another node may show *no
consent* and the dashboard shows only the own source. Turning the switch on brings that
node's records into view, the BMI tile can show a value that combines weight from one source
with height from another, and the source comparison shows where sources disagree.

You can also deep-link: `http://localhost:8800/?bsn=999990603&tab=dabs`.

## What you see

- **Federation strip** — per node whether it delivered, was blocked by consent, had no data,
  or was unreachable. The own node comes first and is marked.
- **Patient data** — for each variable the latest value across all sources. Each field is
  sorted individually, so the address may come from one node while the name comes from
  another: the result is a composition of several source systems. Every value carries a
  source badge and the modification date; if another source has a differing value it is shown
  with a `≠`. A source that has no value for a field is skipped, allowing an older record to
  fill a gap left by a newer one.

  > **Note — per-field dates do not come from the API.** `PatientDTO2024` carries only a
  > single timestamp (`start_time`), so per-field recency cannot be derived from the
  > federation API. The frontend therefore falls back to `start_time` and notes that a
  > source provides no per-field modification date. As soon as the source provides real
  > per-field timestamps this works without code changes.
- **KPI tiles** — latest blood pressure, weight, height, plus derived BMI with source
  attribution.
- **Blood pressure** — time series with reference bands. One continuous line per measurement
  type, spanning all sources: that is the patient's trajectory. Line style distinguishes the
  measurement type (solid systolic, dashed diastolic); the line itself is muted so the data
  points stand out.
- **Weight evolution** — likewise a single combined line over all sources.
- **Source recognition in the graphs** — each data point bears the source in shape **and**
  colour. New nodes get their own colour via `BRON_STIJL` in `web/app.js`.
- **Raw response** — the normalized JSON.

## Structure

```
server.py                 BFF + static server, live-only
  /api/patient/<bsn>      ?requester=&btg=   → normalized model
  /api/config             → {mode: live, dataset: null}
tools/check_omgeving.py   four-layer environment check
web/                      index.html, styles.css, app.js
tests/                    unittest suite (normalization + integration against mock federation)
docs/federation-samples.md  the recorded live responses (contract)
```

The BFF fetches the four endpoints in parallel, normalizes 200- and 503-responses to the same
model, flattens the per-node lists into series with a `_source` field and determines per node
the status `ok` / `consent_blocked` / `offline` / `geen_data`. API keys remain server-side.

## Live-only

There is no `--mode` and no `--dataset`: the app always queries the live federation API. One
node is sufficient — the federation API of a node queries its own EHRbase and forwards to the
other nodes.

If the federation is unreachable or an endpoint raises an error, there is no fallback. The BFF
collapses that failure into one synthetic message and the dashboard shows no data with the
reason. That way "what you see" always equals "what the nodes returned".

> **Cluster availability.** If the federation API is running but the EHRbase pods are
> unreachable, the endpoints answer with 0 records or a 503. That is not a demo bug: the strip
> shows *no data* or *unreachable* per node and the dashboard explains why it is empty.
