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

request to /admin-inactive-accounts

``` python

# POST
# {
#     "Country": "Ireland",
#     "AccountType": "Orchestrator",
# }

# returns
# {
#     "Id": "22132720116",
#     "Password": "8e987681"
# }
```

request to create-n-accounts

``` python

# will create n number of athlete accounts, to be used by the orchestrator
# expecting orchestrator id and number of accounts to create in JSON
# {
#     "Id": "68011495473",
#     "Organization": "Canada ADO",
#     "NumberOfAccounts": 5,
#     "AccountType": "Athlete"
# }
# orchestrator can create accounts for tester or athlete (Specify account type in JSON))


# ADMIN ACCOUNTSSSS!!!!!
# [
#     {
#         "Id": "90176246106",
#         "Password": "cfb88a6f"
#     }
# ]

# [
#     {
#         "Id": "99657640665",
#         "Password": "2d35aa10"
#     }
# ]
```