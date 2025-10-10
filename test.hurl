#!/usr/bin/env hurl --test --repeat 1 --variable backend_host=http://localhost:8000

# register
POST {{backend_host}}/api/v1/auth/register
{
  "email": "user@example.com",
  "password": "string",
  "is_active": true,
  "is_superuser": false,
  "is_verified": false
}
HTTP *
[Asserts]
status >= 200
status <= 400

# login
POST {{backend_host}}/api/v1/auth/jwt/login
content-type: application/x-www-form-urlencoded
`grant_type=password&username=user%40example.com&password=string`
HTTP 200
[Asserts]
jsonpath "$.token_type" == "bearer"
jsonpath "$.access_token" exists
[Captures]
access_token: jsonpath "$.access_token"
GET {{backend_host}}/api/v1/users/me
authorization: Bearer {{access_token}}
HTTP 200
[Asserts]
jsonpath "$.id" exists
jsonpath "$.email" exists
jsonpath "$.is_active" == true
jsonpath "$.is_superuser" == false
jsonpath "$.is_verified" == false


# creat task
POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
{"title": "string"}
HTTP 200
[Asserts]
jsonpath "$.id" exists
jsonpath "$.created_at" exists
jsonpath "$.creator_id" exists
jsonpath "$.title" == "string"
jsonpath "$.is_deleted" == false
jsonpath "$.registration_location" == null
jsonpath "$.work_location" == null
jsonpath "$.updated_at" == null
jsonpath "$.maximum_number_of_people" == null
jsonpath "$.description" == null
jsonpath "$.deadline" == null
jsonpath "$.status" == null
jsonpath "$.contact_number" == null
jsonpath "$.deleted_at" == null
jsonpath "$.start_at" == null
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200
[Asserts]
jsonpath "$.id" exists
jsonpath "$.title" == "string"
jsonpath "$.description" == null
jsonpath "$.registration_location" == null # ?
jsonpath "$.deadline" == null
jsonpath "$.creator_id" exists
jsonpath "$.status" == null
jsonpath "$.created_at" exists
jsonpath "$.updated_at" == null
jsonpath "$.is_deleted" == false # ?
jsonpath "$.start_at" == null # ?
jsonpath "$.contact_number" == null # ?
jsonpath "$.work_location" == null # ?
jsonpath "$.maximum_number_of_people" == null # ?
jsonpath "$.deleted_at" == null # ?

# list task
GET {{backend_host}}/api/v1/task
[Query]
page: 1
itemsPerPage: 1
HTTP 200
[Asserts]
jsonpath "$.data" exists
jsonpath "$.total_count" exists
jsonpath "$.has_more" exists
jsonpath "$.page" == 1
jsonpath "$.items_per_page" == 1


# update task
PATCH {{backend_host}}/api/v1/task/{{task_id}}
HTTP 401
PATCH {{backend_host}}/api/v1/task/{{task_id}}
authorization: Bearer {{access_token}}
{
  "type": "鏟土",
  "title": "string",
  "description": "string",
  "status": "工作中",
  "start_at": "2025-10-03T17:44:16.940Z",
  "deadline": "2025-10-03T17:44:16.940Z",
  "contact_number": "string",
  "registration_location": "string",
  "work_location": "string",
  "required_number_of_people": 0,
  "maximum_number_of_people": 0
}
HTTP 200


# delete task
DELETE {{backend_host}}/api/v1/task/{{task_id}}
HTTP 401
DELETE {{backend_host}}/api/v1/task/{{task_id}}
authorization: Bearer {{access_token}}
HTTP 200
