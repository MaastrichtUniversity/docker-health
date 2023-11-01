# Docker-health

Main repository for the HDP project.
The current services:
- EHRbase
- ETL-demo

# Add this virtual host entry in your /etc/hosts file
```
127.0.0.1	ehrbase.local.dh.unimaas.nl
```

Go to your browser and try this:
```
http://ehrbase.local.dh.unimaas.nl/ehrbase/swagger-ui/index.html
SECURITY_AUTHUSER=user
SECURITY_AUTHPASSWORD=foobar
```
Update the credentials in `./ehrbase/.env.ehrbase`

# Run the stack
```
./rit.sh demo
```