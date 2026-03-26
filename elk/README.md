# ELK configuration

## Docker stage/target

There are 2 stages for the ELK docker image:
 * base → Security and authentication enabled
 * development → Security and authentication disabled

## How to set the page "Configure Elastic to get started"

First time going to "http://elk.local.dh.unimaas.nl/":
 * Click on "Configure manually"
 * Keep the address at "https://localhost:9200" & click on "Check address"
 * Put the password for the user "kibana_system" (Check the secret "kibana-password")
 * Click on "I recognize and trust this certificate:"
 * Check the ELk logs for the log line "Print kibana-verification-code" and enter the code on the next line
 * Wait for setup to finish (maybe refresh the page, if the redirection doesn't work)
 * Log in as the elastic user (Check the secret "elastic-password")
