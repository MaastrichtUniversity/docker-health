# Data Encryption

The ETL expects the input data to be encrypted for some source system (e.g: SAP_ZIBDOCDATA).

## How to encrypt a file for the ETL

While running the following command, a prompt will ask for a passphrase. 
For development, use `foobar`. Or match the current value defined in the secret `etl-data-encryption-passphrase`

```
gpg --symmetric --cipher-algo AES256 ${filename}
gpg --symmetric --cipher-algo AES256 tabak_gebruik.csv
```

The command will generate an encrypted file at the current location with the same name plus the extension `.gpg`.
Keep the original input file for convenience.