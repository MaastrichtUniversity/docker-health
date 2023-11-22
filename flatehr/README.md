# Intro

Ticket [DHHDP-55](https://mumc.atlassian.net/browse/DHHDP-55) is an exploration ticket on the usage of package flatEHR and ECIS REST end point

flatEHR is a low-code python tool creating openEHR composition from XML or JSON souces. Generated compositions are formated on flat format (easier format for understanding and development).

## ECIS REST workflow testing

ECIS rest endpoint was previously known as EhrScape API and then functionality ported into ehrbase. This endpoint works mainly with flat format simSDT.

**Let OP !!**
**Attention!!** The rit.sh will create a new local ehrbase, with a **docker compose up and then at end a docker compose down**

```bash
./rit.sh
```
