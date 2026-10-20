# DABS dashboard demo (live)

Showcase: patiënt zoeken op BSN → dossier openen → DABS-tab → federated data uit de
aangesloten nodes, gevisualiseerd per gegevenstype.

Draait op de Python standard library en vanilla JS. **Geen `pip install`, geen `npm install`,
geen buildstap.**

Deze versie is **live-only**: er zijn geen fixtures en er is geen terugval. De BFF bevraagt
altijd de echte federation API. Levert die niets, dan toont het dashboard niets en legt het
uit waarom — liever een leeg scherm met de reden dan verzonnen data.

## Starten

```bash
python3 server.py
```

Open http://localhost:8800 en zoek op **999990603**.

| Vlag | Betekenis |
|---|---|
| `--host 0.0.0.0` | luisteradres; `0.0.0.0` om de demo op het netwerk te delen |
| `--port 8800` | poort |
| `--timeout 30` | seconden per federation-call voordat deze afbreekt |
| `--federation-base <url>` | basis-URL van de federation API van je eigen node |
| `--key` / `--btg-key` | X-API-Key en break-the-glass key van die node |
| `--eigen-node <naam>` | naam van de eigen node; standaard afgeleid uit de federation-URL |

De federation-URL en de keys verschillen per werkplek en kunnen ook als omgevingsvariabele:

| Variabele | Betekenis |
|---|---|
| `DABS_FEDERATION_BASE` | basis-URL van de federation API van je eigen node |
| `DABS_KEY` | X-API-Key waarmee de eigen node wordt bevraagd |
| `DABS_BTG_KEY` | break-the-glass key die het informed-consent-filter uitzet |
| `DABS_NODES` | nodes die de federatie hoort te hebben (standaard `zio,mumc,envida,vitala`) |

Een vlag gaat vóór de bijbehorende omgevingsvariabele. **De keys worden per werkplek
aangeleverd en staan nooit in deze repository.** Ze blijven serverside: de browser ziet ze
nooit.

## Tests draaien

```bash
python3 -m unittest discover -s tests
```

De integratietests starten `server.py` tegen een mock-federation op een vrije poort; ze
raken de echte federation API niet aan.

## Omgeving controleren

```bash
python3 tools/check_omgeving.py
```

Loopt van binnen naar buiten door vier lagen — machine, federation API, eigen EHRbase, de
vier data-endpoints — en meldt per laag waar het misgaat. Het script gebruikt dezelfde
`DABS_FEDERATION_BASE`, `DABS_KEY` en `DABS_BTG_KEY` als de server, zodat je niet twee keer
hetzelfde hoeft in te vullen.

## De demo lopen

1. **Zoeken** — BSN `999990603` invullen, Enter of *Zoeken*
2. **Dossier** — klik de gevonden patiënt aan
3. **DABS-tab** — klik op DABS in de tabbalk; de vier endpoints worden parallel opgehaald
4. **Break-the-glass** — schakelaar rechts in de federatiestrip omzetten

Twee schakelaars in de federatiestrip:

| Schakelaar | Effect |
|---|---|
| **Break-the-glass** | Zet het informed-consent-filter uit: er wordt met de `--btg-key` bevraagd in plaats van met `--key`. |
| **Alleen brondata** | De app bevraagt de federation-endpoints hoe dan ook rechtstreeks; deze stand verbergt daarnaast de afgeleide BMI-tegel, zodat alleen ruwe bronwaarden overblijven. |

### Perspectief: de eigen node

De UI is een applicatie van medewerkers van de eigen node (standaard ZIO). Zij hebben altijd
toegang tot hun eigen data; gegevens van andere zorgaanbieders komen pas in beeld na
toestemming of break-the-glass. De eigen node wordt daarom zonder het informed-consent-filter
bevraagd en draagt in de strip de markering *eigen node*.

Omdat er geen fixtures meer zijn, toont de app precies wat de nodes op dat moment teruggeven:

| Stand | Wat je ziet |
|---|---|
| Break-the-glass **uit** | de eigen node levert; andere nodes zonder toestemming staan op *geen toestemming* |
| Break-the-glass **aan** | het consent-filter staat uit en alle nodes die data hebben komen mee |

> Dit is het privacy-model, niet een vastgelegde uitkomst. De demodata zijn echt: wat je
> ziet hangt af van welke nodes antwoorden en wat consent toestaat. Dat is precies de
> bedoeling van break-the-glass.

`Alleen brondata` is de eerlijkheidsknop: alles wat je ziet is op dat moment echt uit de
nodes gekomen. Omdat de app live-only is, geldt dat nu voor élke weergave. Leveren de nodes
niets, dan toont het dashboard een leeg scherm met de reden erbij — geen verzonnen reeks.

Stap 4 is het sterkste moment. Zonder break-the-glass kan een andere node op *geen
toestemming* staan en toont het dashboard alleen de eigen bron. Zet je de schakelaar om, dan
verschijnen de records van die nodes, kan de BMI-tegel een waarde tonen die gewicht uit de
ene bron met lengte uit de andere combineert, en laat de bronvergelijking zien waar bronnen
het oneens zijn.

Diep linken kan ook: `http://localhost:8800/?bsn=999990603&tab=dabs`.

## Wat je ziet

- **Federatiestrip** — per node of hij leverde, niets mocht leveren (consent), geen gegevens
  had of onbereikbaar was. De eigen node staat vooraan en is gemarkeerd.
- **Patiëntgegevens** — per variabele de waarde die het laatst is bijgewerkt, over alle
  bronnen heen. Elk veld wordt apart gesorteerd, dus het adres kan uit de ene node komen
  terwijl de naam uit een andere komt: het resultaat is een samenstelling uit meerdere
  bronsystemen. Elke waarde draagt een bronbadge en de wijzigingsdatum; heeft een andere
  bron een afwijkende waarde, dan staat die erachter met `≠`. Een bron die voor een veld
  niets heeft wordt overgeslagen, zodat een ouder record een gat van een nieuwer kan vullen.

  > **Let op — per-veld-datums komen niet uit de API.** De `PatientDTO2024` draagt maar één
  > tijdstempel (`start_time`), dus per-veld-recentheid is uit de federation API niet af te
  > leiden. De frontend valt daarom terug op `start_time` en vermeldt dat een bron geen
  > wijzigingsdatum per veld levert. Zodra de bron echte per-veld-tijdstempels gaat leveren,
  > werkt dat zonder codewijziging.
- **KPI-tegels** — laatste bloeddruk, gewicht, lengte, plus afgeleide BMI met bronvermelding.
- **Bloeddruk** — tijdreeks met referentiebanden. Eén doorlopende lijn per meetwaarde,
  dwars door alle bronnen heen: dat is het verloop van de patiënt. Lijnstijl onderscheidt de
  meetwaarde (doorgetrokken systolisch, gestreept diastolisch); de lijn zelf is gedempt,
  zodat de meetpunten opvallen.
- **Gewichtsverloop** — eveneens één gecombineerde lijn over alle bronnen.
- **Bronherkenning in de grafieken** — elk meetpunt draagt de bron in vorm én kleur. Nieuwe
  nodes krijgen een eigen kleur via `BRON_STIJL` in `web/app.js`.
- **Ruwe response** — de genormaliseerde JSON.

## Opbouw

```
server.py                 BFF + statische server, live-only
  /api/patient/<bsn>      ?requester=&btg=   → genormaliseerd model
  /api/config             → {mode: live, dataset: null}
tools/check_omgeving.py   omgevingscontrole in vier lagen
web/                      index.html, styles.css, app.js
tests/                    unittest-suite (normalisatie + integratie tegen mock-federation)
docs/federation-samples.md  de vastgelegde live responses (contract)
```

De BFF haalt de vier endpoints parallel op, normaliseert 200- en 503-responses tot hetzelfde
model, plat de per-node lijsten tot reeksen met een `_source`-veld en bepaalt per node de
status `ok` / `consent_blocked` / `offline` / `geen_data`. De API-keys blijven serverside.

## Live-only

Er is geen `--mode` en geen `--dataset`: de app bevraagt altijd de live federation API.
Eén node volstaat — de federation API van een node bevraagt zijn eigen EHRbase en fant uit
naar de andere nodes.

Is de federatie onbereikbaar of gooit een endpoint een fout, dan is er geen terugval. De BFF
maakt van die fout één synthetische melding en het dashboard toont geen data met de reden
erbij. Zo blijft "wat je ziet" altijd gelijk aan "wat de nodes teruggaven".

> **Beschikbaarheid van het cluster.** Draait de federation API wel maar zijn de
> EHRbase-pods onbereikbaar, dan antwoorden de endpoints met 0 records of een 503. Dat is
> geen fout van de demo: de strip laat per node *geen gegevens* of *niet bereikbaar* zien en
> het dashboard legt uit waarom het leeg is.
