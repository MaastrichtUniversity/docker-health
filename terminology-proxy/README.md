# POC Terminology reverse proxy 

EHRBase doesn't support basic authentication toward a terminology server, only Two-Way SSL and OAuth2.
The terminology-proxy serves as an endpoint for EHRbase to redirect the validation request toward http://terminology.dh.local by adding the basic authentication header.

## How to test the terminology validation

1. Create an account on the Terminology Server (https://nictiz.nl/app/uploads/2024/07/NTS-Manual-for-New-Users-12-03-2024.pdf)
2. Update the env variables: `TERMINOLOGY_USERNAME` & `TERMINOLOGY_PASSWORD` in `docker-compose.yml`
3. Update `/etc/hosts` file with:  `127.0.0.1	terminology.local.dh.unimaas.nl`
4. Run `./dh.sh up -d --build terminology-proxy`
   1.  You can check if the reverse proxy is correctly set up with this link: http://terminology.local.dh.unimaas.nl/ValueSet?url=http://decor.nictiz.nl/fhir/ValueSet/2.16.840.1.113883.2.4.3.11.60.40.2.7.9.1--20171231000000
5. Run `./dh.sh etl`
   1. Check the logs `./dh.sh logs test-etl-zib`
   2. Copy one of the EHR id for the postman configuration 
6. Import the postman collection `terminology_validation.postman_collection.json`
   1. Paste the EHR id in the collection `Terminology validation` -> tab `Variables`
7. Run the `DataHub-BurgerlijkeStaat-2017-terminology` request (expect: 201)
8. Run the composition requests:
   1. `Valid composition` request (expect: 201)
   2. `Invalid compoition` requests (expect: 400)