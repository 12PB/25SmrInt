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
[^1]: Unique identifier for each module was either individual idcode, household id 'hhid' or proxy household id 'psu' and 'hh', proxy and actual household id were both marked as hhid
