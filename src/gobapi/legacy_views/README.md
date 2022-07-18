# Legacy views

With the migration to Azure, we are migrating to using the Amsterdam Schema within GOB. GOB-API will not be migrated
to Azure, but for as long as we are not fully migrated to Azure, we need to keep GOB running in the CloudVPS
environment. This means that we need to keep delivering our products in CloudVPS; our API and Export products.
However, these products are based on the GOB Model. To be able to migrate internally to Amsterdam Schema, but still
deliver the current products based on the legacy GOB Model, we use a `legacy` schema in the database.

The `legacy` schema is a mapping from the legacy GOB Model to the new schema's sourced from the Amsterdam Schema
repository. (Internally in GOB we still call it GOBModel, but during initialisation we fetch the Amsterdam Schema
where applicable).

GOB-API is responsible for keeping the `legacy` schema up-to-date, and is the sole user of this schema. In Azure
GOB-API won't be deployed, and hence the `legacy` schema will not exist.

GOB-API will ONLY read from the `legacy` schema in runtime.

## Initialising the legacy schema
When GOB-API starts, it walks through the separate tables of the legacy GOBModel (calling GOBModel with `legacy=True`) 
and creates a view in the `legacy` schema that matches each of these tables, so that the `legacy` schema contains
everything GOB-API needs to run.

When initialising these views, GOB-API checks for each legacy table:
- Do we have a custom view defined that translates the GOB database model in the `public` schema to the legacy GOB
Model? Custom views can be found in the directory `view_definitions` under `legacy_table_name.yaml` (replace
legacy_table_name with the name of the legacy table).
- If so, we create this custom view.
- If not, we create a `CREATE OR REPLACE VIEW legacy.table AS SELECT * FROM public.table`, basically returning the
table from the public schema.

## View definitions

### Override columns
View definitions can define the table name or specific columns. Here is an example of NAP Peilmerken, which can be
found under `view_definitions/nap_peilmerken.yaml`:

    table_name: nap_peilmerken
    override_columns:
      ligt_in_bouwblok: ligt_in_gebieden_bouwblok
      merk: |
        jsonb_build_object(
          'code', merk_code,
          'omschrijving', merk_omschrijving
        )

We have to top-level keys:
- `table_name` is the table_name as found in the public schema.
- `override_columns` are the columns to be overridden. All other columns present in the legacy GOB-Model will be
mapped as-is.

In this case, the legacy view created would be:

    CREATE OR REPLACE VIEW legacy.nap_peilmerken AS
    SELECT
        _id,
        merk,
        jaar,
        hoogte_tov_nap,
        ...,
        ligt_in_gebieden_bouwblok       AS ligt_in_bouwblok,
        json_build_object(
          'code', merk_code,
          'omschrijving', merk_omschrijving
        )                               AS merk
    FROM public.nap_peilmerken

Note that not all original columns are copied in this example, but a few (_id, merk, jaar, hoogte_tov_nap) are
provided. We see that in NAP Peilmerken the 'old' attribute `ligt_in_bouwblok` is now called
`ligt_in_gebieden_bouwblok` in GOB, but because of this view, API still exposes this attribute as `ligt_in_bouwblok`.
We see that in the Amsterdam Schema version in GOB we now have two separate fields `merk_code` and `merk_omschrijving`;
this used to be one JSON field. To keep the legacy API working, we map the two separate columns back to a JSON object.

### Rename table
In the example above we see that the `ligt_in_bouwblok` attribute, which happens to be a relation attribute, was
renamed. This means that the relation table itself was renamed as well. The old relation table was
`rel_nap_pmk_gbd_bbk_ligt_in_bouwblok`, but now this relation table is renamed to 
`rel_nap_pmk_gbd_bbk_ligt_in_gebieden_bouwblok`. To define this in a custom view, we create a file
`rel_nap_pmk_gbd_bbk_ligt_in_bouwblok.yaml` in the `view_definitions` directory. Note that the filename contains the
legacy table name. In this yaml file we define only the `table_name`:

    table_name: rel_nap_pmk_gbd_bbk_ligt_in_gebieden_bouwblok

This is the name of the relation table in the GOB database (the public schema). The custom view that will be created
from this view definition will be the following:

    CREATE OR REPLACE VIEW legacy.rel_nap_pmk_gbd_bbk_ligt_in_bouwblok AS
    SELECT * FROM public.rel_nap_pmk_gbd_bbk_ligt_in_gebieden_bouwblok

Again; API still exposes the legacy model, whilst within GOB we use the new Amsterdam Schema model.
