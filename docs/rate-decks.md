# Ratedecks
## Rates CSV
### Example file format
```csv
"rate_cost","description","name","prefix"
"0.1","BRONZE","BRONZE","1503"
"0.2","SILVER","SILVER","150"
"0.3","GOLD","GOLD","15"
"0.4","PLATINUM","PLATINUM","1"
```

### Fields
Name | Description | Required
---- | ----------- | --------
`account_id`|reseller's account (see **Note 1** below)|
`description`|description for rate|
`direction`|direction of call leg ("inbound", "outbound"), if not set - rate matches both directions|
`iso_country_code`|[ISO 3166-1](https://en.wikipedia.org/wiki/ISO_3166-1#Officially_assigned_code_elements) code for prefix's country|
`prefix`|prefix for match DID number| `true`
`pvt_rate_cost`|internal rate cost, used for `weight` calculation|
`pvt_rate_surcharge`|internal rate surcharge|
`rate_cost`|per minute cost| `true`
`rate_increment`|billing "steps" for rate|
`rate_minimum`|minimum call duration|
`rate_name`|short name for rate, if this field not set it will be generated from `prefix`, `iso_country_code` and `direction` fields|
`rate_nocharge_time`|"free" call time, if call duration less then this value (seconds), then call not charged|
`rate_surcharge`|charge amount on connect (answer)|
`rate_version`|rate version|
`ratedeck_id`| ratedeck name, assigned to account via service plan|
`weight`|when found several rates with same prefix, used rate with higher weight. If not set - calculated from `prefix` length and `rate_cost` (`pvt_rate_cost`)|

### Notes
* CSV files for all actions use the same list of fields. Names of fields match the names of keys in the CouchDB [rate document](https://github.com/2600hz/kazoo/blob/master/applications/crossbar/doc/rates.md#schema).
* For `import` & `delete` actions, value of `account_id` from CSV file will be ignored, value for this field is taken from task Account-ID .
* `routes` and `options` fields can not be defined via CSV file (because their values are lists).
`routes` is automatically generated from `prefix`. Example: `prefix` 380 generates `routes` - `["^\\+?380.+$"]`.


## References:
* [2600hz/blog/understanding-rates](https://github.com/2600hz/kazoo/blob/master/doc/blog/understanding_rates.md)
* [2600hz/blog/understanding-rates/csv-format](https://github.com/2600hz/kazoo/blob/master/doc/blog/understanding_rates.md#csv-format)
* [2600hz/tasks/rates](https://github.com/2600hz/kazoo/blob/master/applications/tasks/doc/rates.md)
* [2600hz/crossbar/rates](https://github.com/2600hz/kazoo/blob/master/applications/crossbar/doc/rates.md)
