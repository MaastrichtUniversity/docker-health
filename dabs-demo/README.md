# DABS dashboard demo

Showcase: patiënt zoeken op BSN → dossier openen → DABS-tab → federated data uit MUMC en ZIO,
gevisualiseerd per gegevenstype.

Draait op de Python standard library en vanilla JS. **Geen `pip install`, geen `npm install`,
geen buildstap.**

## Starten

```bash
python3 server.py
```

Open http://localhost:8800 en zoek op **999990603**.

| Vlag | Betekenis |
|---|---|
| `--dataset faithful` | *(standaard)* exact de records die de federation API teruggeeft. Weinig meetpunten. |
| `--dataset rich` | langere meetreeksen zodat de grafieken verloop tonen. Aangevulde demodata, in de UI gelabeld. |
| `--mode fixture` | *(standaard)* vastgelegde responses |
| `--mode live` | echte federation API, met terugval op fixtures per endpoint |
| `--timeout 30` | seconden per federation-call voordat teruggevallen wordt |
| `--port 8800` | poort |
| `--federation-base <url>` | basis-URL van de federation API van je eigen node |
| `--key` / `--btg-key` | X-API-Key en break-the-glass key van die node |
| `--host 127.0.0.1` | `0.0.0.0` om de demo op het netwerk te delen |

De laatste drie verschillen per werkplek en kunnen ook als omgevingsvariabele:
`DABS_FEDERATION_BASE`, `DABS_KEY`, `DABS_BTG_KEY`.

## Omgeving controleren

```bash
python3 tools/check_omgeving.py
```

Loopt van binnen naar buiten door vier lagen — machine, federation API, eigen EHRbase, de
vier data-endpoints — en meldt per laag waar het misgaat. Zie `../OVERZETTEN.md` voor het
volledige stappenplan om dit project op een andere pc te draaien.

Voor een showcase met sprekende grafieken:

```bash
python3 server.py --dataset rich
```

## De demo lopen

1. **Zoeken** — BSN `999990603` invullen, Enter of *Zoeken*
2. **Dossier** — klik de gevonden patiënt aan
3. **DABS-tab** — klik op DABS in de tabbalk; de vier endpoints worden parallel opgehaald
4. **Break-the-glass** — schakelaar rechts in de federatiestrip omzetten

Twee schakelaars in de federatiestrip:

| Schakelaar | Effect |
|---|---|
| **Break-the-glass** | Zet het informed-consent-filter uit. Zie de kanttekening hieronder. |
| **Alleen brondata** | Haalt rechtstreeks bij de federation-endpoints op — geen fixtures, geen terugval, geen afgeleide waarden. Leveren de nodes niets, dan toont het dashboard niets. |

### Perspectief: ZIO

De UI is een applicatie van ZIO-medewerkers. Zij hebben altijd toegang tot hun eigen data;
gegevens van andere zorgaanbieders komen pas in beeld na toestemming of break-the-glass.
De fixtures volgen dat:

| Stand | Wat je ziet |
|---|---|
| Break-the-glass **uit** | alleen ZIO — MUMC staat op *geen toestemming* |
| Break-the-glass **aan** | ZIO plus MUMC, met het aantal ontsloten records in de banner |

> **Dit is een demomodel, niet letterlijk wat de API met déze demodata doet.** In
> `test_federation_rest.py` heeft patiënt 999990603 bij MUMC consent = true (regel 248),
> waardoor MUMC vanuit ZIO ook zónder break-the-glass zou meekomen; `TestZioClient` gebruikt
> daarom de break-the-glass-verwachtingen als gewone uitkomst. Dat is een eigenaardigheid van
> de demodataset, niet van het privacymodel. Voor de showcase modelleren we het algemene
> geval — eigen node altijd, andere nodes achter toestemming — omdat juist dat de werking
> van break-the-glass toont. Met `--mode live` telt wat de nodes echt teruggeven.

`Alleen brondata` is de eerlijkheidsknop: alles wat je daarmee ziet, is op dat moment echt
uit de nodes gekomen. Zolang het cluster plat ligt levert die stand dus een leeg scherm met
de reden erbij. Staat hij uit, dan draait de demo op fixtures en zegt het dashboard dat ook —
grijze `fixture`-chips en een *Geen live data*-banner.

Stap 4 is het sterkste moment. Zonder break-the-glass staat ZIO op *geen toestemming* en toont
het dashboard één bron. Zet je de schakelaar om, dan verschijnen ZIO's records, springt de
BMI-tegel naar een waarde die gewicht uit de ene bron met lengte uit de andere combineert, en
laat de bronvergelijking zien dat MUMC en ZIO het over zeven velden oneens zijn — andere
geboortedatum, ander geslacht, andere naam.

Diep linken kan ook: `http://localhost:8800/?bsn=999990603&tab=dabs`.

## Wat je ziet

- **Federatiestrip** — per node of hij leverde, niets mocht leveren (consent) of onbereikbaar was
- **Patiëntgegevens** — per variabele de waarde die het laatst is bijgewerkt, over alle bronnen
  heen. Elk veld wordt apart gesorteerd, dus het adres kan uit ZIO komen terwijl de naam uit
  MUMC komt: het resultaat is een samenstelling uit beide bronsystemen. Elke waarde draagt een
  bronbadge en de wijzigingsdatum; heeft een andere bron een afwijkende waarde, dan staat die
  erachter met `≠`. Een bron die voor een veld niets heeft wordt overgeslagen, zodat een
  ouder record een gat van een nieuwer kan vullen.

  > **Let op — `_veld_gewijzigd` is gemodelleerd, geen brondata.** De `PatientDTO2024` draagt
  > maar één tijdstempel (`start_time`, bij deze patiënt gelijk aan de geboortedatum), dus
  > per-veld-recentheid is uit de federation API niet af te leiden. De fixtures bevatten
  > daarom een `_veld_gewijzigd`-map per bron. De frontend gebruikt die wanneer hij bestaat en
  > valt anders terug op `start_time` — zodra de bron echte per-veld-tijdstempels levert werkt
  > het zonder codewijziging. In de stand *Alleen brondata* bestaat dit veld niet, want dan
  > komt alles rechtstreeks van de endpoints.
- **KPI-tegels** — laatste bloeddruk, gewicht, lengte, plus afgeleide BMI met bronvermelding
- **Bloeddruk** — tijdreeks met referentiebanden. Eén doorlopende lijn per meetwaarde, dwars
  door alle bronnen heen: dat is het verloop van de patiënt. Lijnstijl onderscheidt de
  meetwaarde (doorgetrokken systolisch, gestreept diastolisch); de lijn zelf is gedempt,
  zodat de meetpunten opvallen.
- **Gewichtsverloop** — eveneens één gecombineerde lijn over alle bronnen
- **Bronherkenning in de grafieken** — elk meetpunt draagt de bron in vorm én kleur: een
  blauwe cirkel is MUMC, een bruine ruit is ZIO. Dat geldt ook voor live data; nieuwe nodes
  krijgen een eigen kleur via `BRON_KLEUR` in `web/app.js`.
- **Ruwe response** — de genormaliseerde JSON

## Opbouw

```
server.py                BFF + statische server
  /api/patient/<bsn>     ?requester=&btg=&dataset=&bron=   → genormaliseerd model
                         bron=nodes: alleen live endpoints, geen terugval
  /api/config
fixtures/                getrouwe set
fixtures-rich/           verrijkte set
tools/make_fixtures.py   genereert beide sets
web/                     index.html, styles.css, app.js
```

De BFF haalt de vier endpoints parallel op, normaliseert 200- en 503-responses tot hetzelfde
model, plat de per-node lijsten tot reeksen met een `_source`-veld en bepaalt per node de
status `ok` / `consent_blocked` / `offline`. De API-keys blijven serverside.

## Live modus

```bash
python3 server.py --mode live
```

Bevraagt `http://federation.zio.local.dh.unimaas.nl`. Eén node volstaat: de federation API
van een node bevraagt zijn eigen EHRbase en fant uit naar de andere nodes. `key1` hoort bij
MUMC; ZIO wijst hem af met een 401, en `btgkey1` schakelt het consent-filter uit.

Levert een endpoint niets op, dan valt de BFF voor dát endpoint terug op de fixture en meldt
de statusstrip *fixtures (federatie onbereikbaar)*. Een demo valt dus niet om als een node
wegvalt.

**Stand op 19-08-2026:** de federation API's draaien, maar hun EHRbase-pods zijn OOMKilled en
de ETL-job is niet doorgelopen, dus live levert nul records. Zie `../PLAN.md` §0 voor de
diagnose. De fixtures zijn daarom de werkende demo-route.

## Fixtures verversen

Zodra het cluster wel data levert, kun je de echte responses vastleggen:

```bash
for ep in Patient Bloeddruk Lichaamsgewicht LichaamsLengte; do
  curl -s -H "X-API-Key: btgkey1" \
    "http://federation.zio.local.dh.unimaas.nl/$ep?bsn=999990603&requester=Rolf" \
    -o "fixtures/$ep.btg.json"
done
```

Zonder `btg` in de bestandsnaam en met `key1` voor de variant mét consent-filter.
