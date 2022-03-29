# Using this service

To use this send

```bash
curl -X POST http://127.0.0.1/create-<type_of_acc>-account
   -H 'Content-Type: application/json'
   -d '{
    "Organization": "",
    "Id": "",
    "FirstName": "",
    "LastName": "",
    "Email": "",
    "Country": "",
    "PhoneNumber": ""
    }'
```

``` python
# ID password combo to test 

# Athelete
# [
#     {
#         "Id": "37189527454",
#         "Password": "895887f1"
#     }
# ]

# Tester

# [
#     {
#         "Id": "56297746115",
#         "Password": "68286860"
#     },
#     {
#         "Id": "75746108831",
#         "Password": "c9cb12c4"
#     }
# ]

# Orchestrator 
# {
#     "Id": "22132720116",
#     "Password": "8e987681"
# }

```
