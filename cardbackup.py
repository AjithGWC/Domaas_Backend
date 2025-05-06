import requests
import json

url = "https://gwcteq-partner.domo.com/api/content/v3/cards/kpi?pageId=-100000"

headers = {
    "Authorization": "Bearer YOUR_ACCESS_TOKEN",
    "Origin": "https://gwcteq-partner.domo.com",
    "Referer": "https://gwcteq-partner.domo.com",
    "x-domo-requestcontext": '{"clientToe":"OUI37IPHOQ-0MPJT"}',
    "Content-Type": "application/json",
    "Cookie": "did=3017514484; s_fid=17106B130881F7B6-1C324560921B7BD7; eb03b5b0dbaeb744_cfid=0764e305ba4c2ece857d11bbd17525b814e84a3cae2218f85bc373fce00df9491fb593002f7543bc9d62807cf7b1173b6f536805487934cc3a5a625fd69fea66; ELOQUA=GUID=1FC44200F75340C59C230240EC700713; _pubweb_is_cus=true; _gcl_au=1.1.1353622541.1739344752; amplitude_id_c68dc3f20888d7c6242144da91c31629domo.com=eyJkZXZpY2VJZCI6ImJjZTJlMmNjLThiMDMtNDM3Mi1hOGRhLTdmZTU0NzMxMWRiMFIiLCJ1c2VySWQiOm51bGwsIm9wdE91dCI6ZmFsc2UsInNlc3Npb25JZCI6MTc0NDk1MjEwMDg2MiwibGFzdEV2ZW50VGltZSI6MTc0NDk1MjEwMDg4NywiZXZlbnRJZCI6MTQsImlkZW50aWZ5SWQiOjUzLCJzZXF1ZW5jZU51bWJlciI6Njd9; _clck=1unelcj%7C2%7Cfv6%7C0%7C1741; s_vnum=1980785319108%26vn%3D6; _ga_JNW5SCCVXP=GS1.2.1744951166.21.1.1744952129.0.0.0; intercom-device-id-t2q61wxb=f9974053-5996-4dd7-9e9e-e813e5ad69d1; PLAY_SESSION=c36fa5593ab7be756ccf9fcecc80563927abcc89-isProxied=false; _ga_KCXF7VX0J3=GS1.1.1745785084.17.1.1745785122.0.0.0; amp_c68dc3=feK7lPGTEtTf2l1VDxTrVD.NDI5MkMxNTI4MDFDNjYzRjMxQTA5NDVFMkQ3RjBCRDdGNkY2QjgyQTRBMTIyQzM2NDlDNEFCRDE5NEE2NTFEMg==..1ipsefm6d.1ipseg1pv.em.2t.hj; _ga_P3SE4R9WJH=GS1.1.1745785194.12.0.1745785199.0.0.0; _ga=GA1.2.275374174.1728324404; _ga_ZH4TQCL1RC=GS1.1.1745846791.123.1.1745846822.29.0.0; _ga_3RM9SF8PCZ=GS1.1.1745846791.143.1.1745846822.29.0.0; intercom-session-t2q61wxb=UWxQL3V1TWpiQzVESVczYWU0aWc4bHkwb3VnVkpzcVltc0RJc0xWNFdISlBuM2lGeXBueEdmUEFwdTlKZERHRUhIY2I1Qkw1N3kyUUIyYlgvRXBmM1JDYUVFSXM1Qng5S2VSRm5CTytWNFk9LS04Q2pYWVNhNU5UOG85ZkxrSzdwMHdBPT0=--1bf0d9811c0378f8885794b8177057478427c317; _pubweb_idc=gwcteq-partner_#_standard; SESSION_TOE=7VUM9K9GM4; redirectUrl=%2Fpage%2F1978648218%3FuserId%3D696848368; mbox=PC#f6229fd995d742908114d2eb6916fa62.41_0#1809339584|session#fab0ecfdbb0f449a916f22dd7d89e38f#1746096645; _dsidv1=e9e72fec-de94-4539-bc85-bf9e051cc7de; csrf-token=9c6c44eb-1f9f-491f-a0b4-2f915e1cb5be; DA-SID-prod5-gwcteq-partner=eyJjdXN0b21lcklkIjoiZ3djdGVxLXBhcnRuZXIiLCJleHBpcmF0aW9uIjoxNzQ2MTk1Nzk3MDAwLCJobWFjU2lnbmF0dXJlIjoiZGI5Zjg1Y2YwZWZiODJiOGMwMGU0NGQ2MDYwZmUwNzQzMjhkOTU4MDBmYjJmNDg5ZTA1N2E4ODNiMjE4N2Y5MyIsInNpZCI6IjRhYjcxYWM4LTYxYjMtNDA5OS1hMmI1LWEyZmQ4N2ZlODQyZiIsInRpbWVzdGFtcCI6MTc0NjE2Njk5NzAwMCwidG9lcyI6IlVOS05PV05TSUQiLCJ1c2VySWQiOiI2OTY4NDgzNjgifQ%3D%3D"
}

body = {
    "definition": {
        "subscriptions": {
            "big_number": {
                "name": "big_number",
                "columns": [
                    {
                        "aggregation": "SUM",
                        "alias": "Sum of Age",
                        "column": "Age",
                        "format": {
                            "format": "#A",
                            "type": "abbreviated"
                        }
                    }
                ],
                "filters": [],
                "orderBy": [],
                "groupBy": [],
                "fiscal": False,
                "projection": False,
                "distinct": False,
                "limit": 1
            },
            "main": {
                "name": "main",
                "columns": [
                    {
                        "column": "Name",
                        "mapping": "ITEM"
                    },
                    {
                        "column": "Age",
                        "aggregation": "SUM",
                        "mapping": "VALUE"
                    }
                ],
                "filters": [],
                "orderBy": [],
                "groupBy": [
                    {
                        "column": "Name"
                    }
                ],
                "fiscal": False,
                "projection": False,
                "distinct": False
            }
        },
        "formulas": {
            "dsUpdated": [],
            "dsDeleted": [],
            "card": []
        },
        "annotations": {
            "new": [],
            "modified": [],
            "deleted": []
        },
        "conditionalFormats": {
            "card": [],
            "datasource": []
        },
        "controls": [],
        "segments": {
            "active": [],
            "create": [],
            "update": [],
            "delete": []
        },
        "charts": {
            "main": {
                "component": "main",
                "chartType": "badge_vert_stackedbar",
                "overrides": {},
                "goal": None
            }
        },
        "dynamicTitle": {
            "text": [
                {
                    "text": "nandha_test",
                    "type": "TEXT"
                }
            ]
        },
        "dynamicDescription": {
            "text": [],
            "displayOnCardDetails": True
        },
        "chartVersion": "12",
        "noDateRange": True,
        "title": "nandha_test",
        "description": ""
    },
    "dataProvider": {
        "dataSourceId": "2b36a579-1d9e-4497-ad5f-de1d00c34489"
    },
    "variables": True
}

response = requests.put(url, headers=headers, data=json.dumps(body))

print("Status:", response.status_code)
print("Response:", response.text)
