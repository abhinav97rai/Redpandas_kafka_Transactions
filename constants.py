SCHEMA_STR = """{
    "type": "record",
    "name": "Transactions",
    "namespace": "assign.transaction.record",
    "fields": [
        {"name": "user_id","type": ["int","null"]},
        {"name": "transaction_timestamp_millis","type": ["long","null"]},
        {"name": "amount","type": ["float","null"]},
        {"name": "currency","type": ["string","null"]},
        {"name": "counterpart_id","type": ["int","null"]}
    ]
}"""