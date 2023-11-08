# Docker-health

Main repository for the HDP project.
The current services:
- EHRbase
- ETL-demo

# Add this virtual host entry in your /etc/hosts file
```
127.0.0.1	ehrbase.local.dh.unimaas.nl
127.0.0.1	jupyter.local.dh.unimaas.nl
```

Go to your browser and try this:
```
http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html
SECURITY_AUTHUSER=user
SECURITY_AUTHPASSWORD=foobar
```
Update the credentials in `./ehrbase/.env.ehrbase`

# Run the stack

## Clone the external repositories

```
./rit.sh externals clone
```

## Create the synthetic dataset

```
./rit.sh data
```

## Run ETL demo

**WIP**

```
./rit.sh demo
```

# Specified command-lines
```
docker exec -it hdp-etl-demo-1 bash
```

```
python ETL.py --help
Usage: ETL.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get-all-ehr-id      Get all EHR ID on a specific openEHR instance
  list-all-templates  Print all template available on the server
  run                 Runs all ETL from default hard coded values
```
