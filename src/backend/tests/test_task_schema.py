import datetime
from zoneinfo import ZoneInfo as TzInfo  # noqa: F401, RUF100

from inline_snapshot import snapshot
import pytest

from app.schemas.task_schema import CreateTaskSchema


UTC = 'UTC'


# ruff: noqa: E501
@pytest.mark.parametrize(
    ('data', 'expected'),
    [
        (
            r"""
            {
            "title": "水電修繕（電力恢復、臨時配線、水管配管及化糞池等）：50名",
            "description": "單位：花蓮縣政府資訊科\n現階段需要具備專業技能的志工，協助受災家戶恢復日常生活\n📌 注意事項\n請攜帶自行用之工具、設備及相關材料，並注意自身安全。\n因配合當地救援車輛優先原則，強烈建議搭乘火車前往。\n若遇天候惡化，將視狀況調整或暫停行程。",
            "start_at": "2025-10-03 01:00:00+0000",
            "deadline": "2025-10-08 09:00:00+0000",
            "contact_number": "📞志工聯繫專線\n0972223409\n0972223410 ",
            "registration_location": "地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)",
            "maximum_number_of_people": 50
            }
            """,
            snapshot(
                {
                    'title': '水電修繕（電力恢復、臨時配線、水管配管及化糞池等）：50名',
                    'status': None,
                    'description': """\
單位：花蓮縣政府資訊科
現階段需要具備專業技能的志工，協助受災家戶恢復日常生活
📌 注意事項
請攜帶自行用之工具、設備及相關材料，並注意自身安全。
因配合當地救援車輛優先原則，強烈建議搭乘火車前往。
若遇天候惡化，將視狀況調整或暫停行程。\
""",
                    'weight': None,
                    'start_at': datetime.datetime(2025, 10, 3, 1, 0, tzinfo=TzInfo(UTC)),
                    'deadline': datetime.datetime(2025, 10, 8, 9, 0, tzinfo=TzInfo(UTC)),
                    'contact_number': """\
📞志工聯繫專線
0972223409
0972223410 \
""",
                    'registration_location': '地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)',
                    'registration_location_url': None,
                    'work_location': None,
                    'work_location_url': None,
                    'maximum_number_of_people': 50,
                }
            ),
        ),
        (
            r"""
            {
            "title": "房屋修繕（泥作、門窗修補、牆面及地板修復）：50名",
            "description": "單位：花蓮縣政府資訊科\n現階段需要具備專業技能的志工，協助受災家戶恢復日常生活\n📌 注意事項\n請攜帶自行用之工具、設備及相關材料，並注意自身安全。\n因配合當地救援車輛優先原則，強烈建議搭乘火車前往。\n若遇天候惡化，將視狀況調整或暫停行程。",
            "start_at": "2025-10-03 01:00:00+0000",
            "deadline": "2025-10-08 09:00:00+0000",
            "contact_number": "📞志工聯繫專線\n0972223409\n0972223410 ",
            "registration_location": "地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)",
            "maximum_number_of_people": 50
            }
            """,
            snapshot(
                {
                    'title': '房屋修繕（泥作、門窗修補、牆面及地板修復）：50名',
                    'status': None,
                    'description': """\
單位：花蓮縣政府資訊科
現階段需要具備專業技能的志工，協助受災家戶恢復日常生活
📌 注意事項
請攜帶自行用之工具、設備及相關材料，並注意自身安全。
因配合當地救援車輛優先原則，強烈建議搭乘火車前往。
若遇天候惡化，將視狀況調整或暫停行程。\
""",
                    'weight': None,
                    'start_at': datetime.datetime(2025, 10, 3, 1, 0, tzinfo=TzInfo(UTC)),
                    'deadline': datetime.datetime(2025, 10, 8, 9, 0, tzinfo=TzInfo(UTC)),
                    'contact_number': """\
📞志工聯繫專線
0972223409
0972223410 \
""",
                    'registration_location': '地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)',
                    'registration_location_url': None,
                    'work_location': None,
                    'work_location_url': None,
                    'maximum_number_of_people': 50,
                }
            ),
        ),
        (
            r"""
            {
            "title": "機械維修（抽水機、發電機及其他機具維修）：50名",
            "description": "單位：花蓮縣政府資訊科\n現階段需要具備專業技能的志工，協助受災家戶恢復日常生活\n📌 注意事項\n請攜帶自行用之工具、設備及相關材料,並注意自身安全。\n因配合當地救援車輛優先原則，強烈建議搭乘火車前往。\n若遇天候惡化，將視狀況調整或暫停行程。",
            "status": null,
            "start_at": "2025-10-03 01:00:00+0000",
            "deadline": "2025-10-08 09:00:00+0000",
            "contact_number": "📞志工聯繫專線\n0972223409\n0972223410 ",
            "registration_location": "地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)",
            "maximum_number_of_people": 50
            }
            """,
            snapshot(
                {
                    'title': '機械維修（抽水機、發電機及其他機具維修）：50名',
                    'status': None,
                    'description': """\
單位：花蓮縣政府資訊科
現階段需要具備專業技能的志工，協助受災家戶恢復日常生活
📌 注意事項
請攜帶自行用之工具、設備及相關材料,並注意自身安全。
因配合當地救援車輛優先原則，強烈建議搭乘火車前往。
若遇天候惡化，將視狀況調整或暫停行程。\
""",
                    'weight': None,
                    'start_at': datetime.datetime(2025, 10, 3, 1, 0, tzinfo=TzInfo(UTC)),
                    'deadline': datetime.datetime(2025, 10, 8, 9, 0, tzinfo=TzInfo(UTC)),
                    'contact_number': """\
📞志工聯繫專線
0972223409
0972223410 \
""",
                    'registration_location': '地點：花蓮縣光復火車站門口(09:00集合，由花蓮縣政府人員引導與派工)',
                    'registration_location_url': None,
                    'work_location': None,
                    'work_location_url': None,
                    'maximum_number_of_people': 50,
                }
            ),
        ),
        (
            r"""
            {
            "title": "清潔機具操作與支援  (大型清掃設備操作與協助 ) ：50名",
            "description": "單位：花蓮縣政府資訊科\n現階段需要具備專業技能的志工，協助受災家戶恢復日常生活\n📌 注意事項\n請攜帶自行用之工具、設備及相關材料，並注意自身安全。\n因配合當地救援車輛優先原則，強烈建議搭乘火車前往。\n若遇天候惡化，將視狀況調整或暫停行程。",
            "start_at": "2025-10-03 01:00:00+0000",
            "deadline": "2025-10-08 09:00:00+0000",
            "contact_number": "📞志工聯繫專線\n0972223409\n0972223410 ",
            "maximum_number_of_people": 50
            }
            """,
            snapshot(
                {
                    'title': '清潔機具操作與支援  (大型清掃設備操作與協助 ) ：50名',
                    'status': None,
                    'description': """\
單位：花蓮縣政府資訊科
現階段需要具備專業技能的志工，協助受災家戶恢復日常生活
📌 注意事項
請攜帶自行用之工具、設備及相關材料，並注意自身安全。
因配合當地救援車輛優先原則，強烈建議搭乘火車前往。
若遇天候惡化，將視狀況調整或暫停行程。\
""",
                    'weight': None,
                    'start_at': datetime.datetime(2025, 10, 3, 1, 0, tzinfo=TzInfo(UTC)),
                    'deadline': datetime.datetime(2025, 10, 8, 9, 0, tzinfo=TzInfo(UTC)),
                    'contact_number': """\
📞志工聯繫專線
0972223409
0972223410 \
""",
                    'registration_location': None,
                    'registration_location_url': None,
                    'work_location': None,
                    'work_location_url': None,
                    'maximum_number_of_people': 50,
                }
            ),
        ),
        (
            r"""
            {
            "title": "物資需求：毛巾100條、抹布100條、小刷子100支、水管100條、清潔手套100雙",
            "description": "志工單位：花蓮縣政府社會處",
            "contact_number": "0966-589-021",
            "registration_location": "花蓮糖廠"
            }
            """,
            snapshot(
                {
                    'title': '物資需求：毛巾100條、抹布100條、小刷子100支、水管100條、清潔手套100雙',
                    'status': None,
                    'description': '志工單位：花蓮縣政府社會處',
                    'weight': None,
                    'start_at': None,
                    'deadline': None,
                    'contact_number': '0966-589-021',
                    'registration_location': '花蓮糖廠',
                    'registration_location_url': None,
                    'work_location': None,
                    'work_location_url': None,
                    'maximum_number_of_people': None,
                }
            ),
        ),
        (
            r"""
            {
            "title": "人力需求：貨車、堆高機、深入災區清淤志工各50名",
            "description": "備註：要具備貨車、堆高機等設備",
            "contact_number": "0927139554",
            "registration_location": "花蓮縣花蓮市國盛四街88號"
            }
            """,
            snapshot(
                {
                    'title': '人力需求：貨車、堆高機、深入災區清淤志工各50名',
                    'status': None,
                    'description': '備註：要具備貨車、堆高機等設備',
                    'weight': None,
                    'start_at': None,
                    'deadline': None,
                    'contact_number': '0927139554',
                    'registration_location': '花蓮縣花蓮市國盛四街88號',
                    'registration_location_url': None,
                    'work_location': None,
                    'work_location_url': None,
                    'maximum_number_of_people': None,
                }
            ),
        ),
        (
            r"""
            {
            "title": "太巴塱基督長老教會義廚需要您長期的加入！",
            "description": "期望人手：有廚師，團膳為優先，助廚幫手也很歡迎！\n工作內容：烹煮，切菜，打便當，清潔，洗滌\n工作時間：05：00~16：00\n聯絡電話：0955567736\n聯絡賴帳號：escoffier1974\n賴聯絡時請寫明您的中文姓名、聯絡電話，可以服務的專長，事項，服務日期，需要住宿也請備註（但是不保證有住宿床鋪位）\n#交通住宿請自理感謝\n抵達現場請找羅妹報到說明是林仁中師傅的人員，並且配合義廚現場內外場的主管指揮調度 \n#交通住宿請自理感謝\n抵達現場請找羅妹報到說明是林仁中師傅的人員，並且配合義廚現場內外場的主管指揮調度 \n",
            "start_at": "2025-10-09 02:12:04.902+0000",
            "deadline": "2025-10-30 02:12:04.902+0000",
            "contact_number": "0955567736",
            "registration_location": "太巴塱基督長老教會",
            "work_location": "太巴塱基督長老教會",
            "maximum_number_of_people": 10
            }
            """,
            snapshot(
                {
                    'title': '太巴塱基督長老教會義廚需要您長期的加入！',
                    'status': None,
                    'description': """\
期望人手：有廚師，團膳為優先，助廚幫手也很歡迎！
工作內容：烹煮，切菜，打便當，清潔，洗滌
工作時間：05：00~16：00
聯絡電話：0955567736
聯絡賴帳號：escoffier1974
賴聯絡時請寫明您的中文姓名、聯絡電話，可以服務的專長，事項，服務日期，需要住宿也請備註（但是不保證有住宿床鋪位）
#交通住宿請自理感謝
抵達現場請找羅妹報到說明是林仁中師傅的人員，並且配合義廚現場內外場的主管指揮調度 \n\
#交通住宿請自理感謝
抵達現場請找羅妹報到說明是林仁中師傅的人員，並且配合義廚現場內外場的主管指揮調度 \n\
""",
                    'weight': None,
                    'start_at': datetime.datetime(2025, 10, 9, 2, 12, 4, 902000, tzinfo=TzInfo(UTC)),
                    'deadline': datetime.datetime(2025, 10, 30, 2, 12, 4, 902000, tzinfo=TzInfo(UTC)),
                    'contact_number': '0955567736',
                    'registration_location': '太巴塱基督長老教會',
                    'registration_location_url': None,
                    'work_location': '太巴塱基督長老教會',
                    'work_location_url': None,
                    'maximum_number_of_people': 10,
                }
            ),
        ),
    ],
)
def test_create_task_schema(*, data: str, expected: dict) -> None:
    schema = CreateTaskSchema.model_validate_json(data)
    assert schema.model_dump() == expected
