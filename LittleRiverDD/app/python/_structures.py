null = None

FIELDS = ['OBJECTID', 'OWNER_CODE', 'PARCEL_ID', 'OWNER', 'ASSESSED_ACRES', 'TOT_BENEFIT',
          'TOT_ADMIN_FEE', 'AMOUNT_PAID', 'PENALTY', 'EXCESS', 'DATE_PAID',
          'COUNTY', 'YEAR', 'PIN', 'SEC_TWN_RNG', 'PAID']

FIELD_ALIASES = {
  "OWNER2": "OWNER 2",
  "SECTION": "SECTION",
  "PAID": "PAID",
  "SEC_TWN_RNG": "SEC-TWN-RNG",
  "EXCESS": "EXCESS",
  "PIN": "PIN",
  "AMOUNT_PAID": "AMOUNT PAID",
  "TOT_ASSESSMENT": "ASSESSMENT",
  "OBJECTID": "OBJECTID",
  "SEQUENCE": "SEQUENCE",
  "PENALTY": "PENALTY",
  "FLAG": "FLAG",
  "TOT_BENEFIT": "BENEFIT",
  "YEAR": "YEAR",
  "TOWNSHIP": "TOWNSHIP",
  "COUNTY": "COUNTY",
  "ASSESSED_ACRES": "ASSESSED ACRES",
  "PARCEL_ID": "PARCEL ID",
  "RANGE": "RANGE",
  "DATE_PAID": "DATE PAID",
  "OWNER_CODE": "OWNER CODE",
  "OWNER": "OWNER",
  "TOT_ADMIN_FEE": "ADMIN FEE"
}

FIELD_OBJECTS = [
  {
    "alias": "OBJECTID",
    "domain": null,
    "type": "esriFieldTypeOID",
    "name": "OBJECTID"
  },
  {
    "alias": "OWNER CODE",
    "length": 50,
    "type": "esriFieldTypeString",
    "name": "OWNER_CODE",
    "domain": null
  },
  {
    "alias": "PARCEL ID",
    "length": 50,
    "type": "esriFieldTypeString",
    "name": "PARCEL_ID",
    "domain": null
  },
  {
    "alias": "OWNER",
    "length": 255,
    "type": "esriFieldTypeString",
    "name": "OWNER",
    "domain": null
  },
  {
    "alias": "ASSESSED ACRES",
    "domain": null,
    "type": "esriFieldTypeDouble",
    "name": "ASSESSED_ACRES"
  },
  {
    "alias": "BENEFIT",
    "domain": null,
    "type": "esriFieldTypeSingle",
    "name": "TOT_BENEFIT"
  },
  {
    "alias": "ADMIN FEE",
    "domain": null,
    "type": "esriFieldTypeSingle",
    "name": "TOT_ADMIN_FEE"
  },
  {
    "alias": "AMOUNT PAID",
    "domain": null,
    "type": "esriFieldTypeSingle",
    "name": "AMOUNT_PAID"
  },
  {
    "alias": "PENALTY",
    "domain": null,
    "type": "esriFieldTypeSingle",
    "name": "PENALTY"
  },
  {
    "alias": "EXCESS",
    "domain": null,
    "type": "esriFieldTypeSingle",
    "name": "EXCESS"
  },
  {
    "alias": "DATE PAID",
    "length": 8,
    "type": "esriFieldTypeDate",
    "name": "DATE_PAID",
    "domain": null
  },
  {
    "alias": "COUNTY",
    "length": 50,
    "type": "esriFieldTypeString",
    "name": "COUNTY",
    "domain": null
  },
  {
    "alias": "YEAR",
    "domain": null,
    "type": "esriFieldTypeSmallInteger",
    "name": "YEAR"
  },
  {
    "alias": "PIN",
    "length": 50,
    "type": "esriFieldTypeString",
    "name": "PIN",
    "domain": null
  },
  {
    "alias": "SEC-TWN-RNG",
    "length": 255,
    "type": "esriFieldTypeString",
    "name": "SEC_TWN_RNG",
    "domain": null
  },
  {
    "alias": "PAID",
    "length": 1,
    "type": "esriFieldTypeString",
    "name": "PAID",
    "domain": {
      "codedValues": {
        "Y": "Y",
        "N": "N"
      },
      "type": "Text",
      "name": "Flag"
    }
  }
]

COUNTIES = ['BOLLINGER COUNTY',
    'CAPE GIRARDEAU COUNTY',
    'DUNKLIN COUNTY',
    'NEW MADRID COUNTY',
    'PEMISCOT COUNTY',
    'SCOTT COUNTY',
    'STODDARD COUNTY']
