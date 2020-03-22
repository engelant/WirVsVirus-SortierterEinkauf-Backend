# Get the details for the given location_ids

Get the details for the given location_ids, 

**URL** : `/api/locations`

**Method** : `GET`

**Permissions required** : None

## Success Response

**Code** : `200 OK`

**Data constraints**

Provide list of location_ids for which to obtain details

```json
[
    "[location_ids]"
]
```

**Data example** All fields must be sent.

```json
[
    0,
    1,
    5,
    9
]
```
**Content examples**

This returns an object with location_id as key and the location_details.
Invalid or not found ids will be ommitted!

```json
{
    "0": {
        "name": "Supermarket A",
        "address": "Somestreet, Sometown",
        "ltdtude": 12.2345
    },
}
```

For a user with ID 4321 on the local database but no details have been set yet.

```json
{
    "id": 4321,
    "first_name": "",
    "last_name": "",
    "email": ""
}
```

## Notes

* If the User does not have a `UserInfo` instance when requested then one will
  be created for them.