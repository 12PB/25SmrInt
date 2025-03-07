# Albania LSMS data scraping  
Python-based web-scraping and data cleaning code

## Breakdown of Output data

### Metadata table: Collects all available variables 
Breakdown of data fields:
- “variable_name”:  Field name (normalized - please ensure the field name formats are consistent)
- “variable_description”: Readable and complete description of the variable in English
- “module_name”: Survey module that variable belongs to
- “module_description”: Description of the survey module.
- “data_type”: Data type (numeric, categorical, free data entry i.e. string, etc).
- “unique_id”: hhid/id for per-household data/ individual data [^1]
[^1]: Each household has a household id 'hhid', but it can also be identified using a combination of the "primary selection unit", 'psu' variable and "household no", 'hh' which map uniquely to the 6671 households in the study. All entries lacking hhid were given a hhid based on this mapping of hhid-psu+hh. When individual identifiers were present, the data was marked as per-individual data, and per-household otherwise.
