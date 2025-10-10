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
file,1.json;
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200

POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
file,2.json;
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200

POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
file,3.json;
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200

POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
file,4.json;
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200

POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
file,5.json;
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200

POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
file,6.json;
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200

POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
file,7.json;
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200
