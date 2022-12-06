# Dump

The GOB-API supports dumping collections to csv or to another database.

## Example

To dump gebieden stadsdelen from the acceptance environment you can use:

### Dump to CSV

Dumps the collection in CSV format:
- field separation character: ";"
- quotation character: '"'

```
https://acc.api.data.amsterdam.nl/gob/dump/gebieden/stadsdelen/?format=csv
```
