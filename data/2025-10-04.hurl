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
{

  "title": "水電修繕（電力恢復、臨時配線、水管配管及化糞池等）：50名",
  "required_number_of_people": 50,
  "maximum_number_of_people": 50,

  "start_at": "2025-10-03T09:00:00+0800",
  "deadline": "2025-10-08T17:00:00+0800",

  "registration_location": "地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)",
  "description": "單位：花蓮縣政府資訊科\n現階段需要具備專業技能的志工，協助受災家戶恢復日常生活\n📌 注意事項\n請攜帶自行用之工具、設備及相關材料，並注意自身安全。\n因配合當地救援車輛優先原則，強烈建議搭乘火車前往。\n若遇天候惡化，將視狀況調整或暫停行程。",
  "contact_number": "📞志工聯繫專線\n0972223409\n0972223410 "
}
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200


# creat task
POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
{

  "title": "房屋修繕（泥作、門窗修補、牆面及地板修復）：50名",
  "required_number_of_people": 50,
  "maximum_number_of_people": 50,

  "start_at": "2025-10-03T09:00:00+0800",
  "deadline": "2025-10-08T17:00:00+0800",

  "registration_location": "地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)",
  "description": "單位：花蓮縣政府資訊科\n現階段需要具備專業技能的志工，協助受災家戶恢復日常生活\n📌 注意事項\n請攜帶自行用之工具、設備及相關材料，並注意自身安全。\n因配合當地救援車輛優先原則，強烈建議搭乘火車前往。\n若遇天候惡化，將視狀況調整或暫停行程。",
  "contact_number": "📞志工聯繫專線\n0972223409\n0972223410 "
}
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200


# creat task
POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
{

  "title": "機械維修（抽水機、發電機及其他機具維修）：50名",
  "required_number_of_people": 50,
  "maximum_number_of_people": 50,

  "start_at": "2025-10-03T09:00:00+0800",
  "deadline": "2025-10-08T17:00:00+0800",

  "registration_location": "地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)",
  "description": "單位：花蓮縣政府資訊科\n現階段需要具備專業技能的志工，協助受災家戶恢復日常生活\n📌 注意事項\n請攜帶自行用之工具、設備及相關材料，並注意自身安全。\n因配合當地救援車輛優先原則，強烈建議搭乘火車前往。\n若遇天候惡化，將視狀況調整或暫停行程。",
  "contact_number": "📞志工聯繫專線\n0972223409\n0972223410 "
}
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200



# creat task
POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
{

  "title": "清潔機具操作與支援  (大型清掃設備操作與協助 ) ：50名",
  "required_number_of_people": 50,
  "maximum_number_of_people": 50,

  "start_at": "2025-10-03T09:00:00+0800",
  "deadline": "2025-10-08T17:00:00+0800",

  "registration_location": "地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)",
  "description": "單位：花蓮縣政府資訊科\n現階段需要具備專業技能的志工，協助受災家戶恢復日常生活\n📌 注意事項\n請攜帶自行用之工具、設備及相關材料，並注意自身安全。\n因配合當地救援車輛優先原則，強烈建議搭乘火車前往。\n若遇天候惡化，將視狀況調整或暫停行程。",
  "contact_number": "📞志工聯繫專線\n0972223409\n0972223410 "
}
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200



# creat task
POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
{
  "description": "志工單位：花蓮縣政府社會處",
  "registration_location": "花蓮糖廠",
  "contact_number": "0966-589-021",
  "title": "物資需求：毛巾100條、抹布100條、小刷子100支、水管100條、清潔手套100雙"
}
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200



# creat task
POST {{backend_host}}/api/v1/task
authorization: Bearer {{access_token}}
{
  "registration_location": "花蓮縣花蓮市國盛四街88號",
  "contact_number": "0927139554",
  "title": "人力需求：貨車、堆高機、深入災區清淤志工各50名",
  "description": "備註：要具備貨車、堆高機等設備"
}
HTTP 200
[Captures]
task_id: jsonpath "$.id"
GET {{backend_host}}/api/v1/task/{{task_id}}
HTTP 200
