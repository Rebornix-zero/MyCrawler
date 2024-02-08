import requests
import csv
import re
import json

MAX_NOTES_PER_KEYWORD=5
SEARCH_KEYWORDS = ['年轻人夜校']
SEARCH_URL = "https://edith.xiaohongshu.com/api/sns/web/v1/search/notes"
NOTE_COMMENT_URL_TEMPLATE = "https://edith.xiaohongshu.com/api/sns/web/v2/comment/page?note_id={}&cursor={}&top_comment_id=&image_formats=jpg,webp,avif"
COOKIE = "abRequestId=9491683b-9d12-5fd7-be43-073c55dfc049; webBuild=4.1.6; xsecappid=xhs-pc-web; a1=18d8593e3b0edq7k95f6ahlhjf9nkqdpd890p917w50000430543; webId=06419f609ffa0ad3369674cc463e7a89; acw_tc=6c8e1edd01cb8508dbc1f60887b61ce396a273fa5530d93ebd8b6718bda5e164; websectiga=634d3ad75ffb42a2ade2c5e1705a73c845837578aeb31ba0e442d75c648da36a; sec_poison_id=ad2a4de2-f5dc-481e-acc0-cd592f80d81f; web_session=040069b4b7bfaf3183716fb5f6374b56712509; gid=yYfY2jqdYJf8yYfY2jqdqYjyD8dfAWTj2iK0jWEx1xVij828ITAfUU8884q824q8q8qJiiJd; unread={%22ub%22:%2265b60c23000000000c005418%22%2C%22ue%22:%2265aa49b2000000002b03c6ec%22%2C%22uc%22:30}"
REFERER = "https://www.xiaohongshu.com/"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0"
)


# @brief 过滤掉评论中的回复对象、表情信息、话题等无效字段
# @param text_raw 原始评论文本
# @return 过滤后的文本
def text_filter(text_raw):
    new_text = re.sub(r"\[.*\]|(回复)?@.*:|@.*|#.*# ?|转发微博", "", text_raw)
    return new_text


# @brief 添加一条评论到持久化文件中
# @param text_raw 原始评论文本
def add_comment(text_raw):
    new_text = text_filter(text_raw)
    # 如果过滤后为空则不必添加
    if new_text != "":
        csv_writer.writerow([new_text])

# @brief 获取笔记下评论的实际url
# @param note_id
# @param cursor
# @return 实际请求的有效url
def get_comments_url(note_id, cursor):
    return NOTE_COMMENT_URL_TEMPLATE.format(note_id, cursor)


# MAIN
note_id_list = []
# GET请求头
get_request_header = {"cookie": COOKIE, "user_agent": USER_AGENT}
# POST请求头
post_request_header = {
    "authority": "edith.xiaohongshu.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "content-type": "application/json;charset=UTF-8",
    "origin": "https://www.xiaohongshu.com",
    "referer": "https://www.xiaohongshu.com/",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188",
    "x-s": "XYW_eyJzaWduU3ZuIjoiNTEiLCJzaWduVHlwZSI6IngxIiwiYXBwSWQiOiJ4aHMtcGMtd2ViIiwic2lnblZlcnNpb24iOiIxIiwicGF5bG9hZCI6ImNiZjQzZDUyODU0NDhkZDI2ZmJkYzUyMTBhZTA4ODI4MGNmZjYyMWQ1NGYzNTg4YTBlYTEwZTkwZjkxMTBhOTZmYjg5ZGFmZWZiZTExZmFmMTA5MDQ0MWEzOTcxMmZiMWM5ZTNiZmRhMWZhYTFlYjkwZDc0YWEzMWI1NGM3MmNkMGQ3NGFhMzFiNTRjNzJjZGFjNDg5YjlkYThjZTVlNDhmNGFmYjlhY2ZjM2VhMjZmZTBiMjY2YTZiNGNjM2NiNTg2NDdlZGFjZGVhYzY5MGUwY2Y3ZGMyNTE5ZTVlNGFlZmRjZWY5ZDU5YTc2ZGY0YzQ2OGM4M2FmMjdlOGUzMDNhMWUxNzAzMDg1NDgwMTRmOTRhNDE4YWNjNjk2ODljYTE5MDM2NWY1MTI1NDhkZjg0MjIyMmJmZGI1MzM5NzhkZjdhNDgwOGIwYmExZTNhMWFkNDUzMDBhMmNiMDdkYWU3MTdjYmRjMWUzNDQ5NDVhNzM0MmE2NGNjMDMxNTM5MSJ9",
    "x-t": "1707361066510",
}
# post请求体 
post_json_body = {
    "image_scenes": "FD_PRV_WEBP,FD_WM_WEBP",
    "keyword": "",
    "page": "1",
    "page_size": "20",
    "search_id": "2c7hu5b3kzoivkh848hp0",
    "sort": "popularity_descending",
    "note_type": "0",
}
# post请求cookie
cookies = {
    "sec_poison_id": "b570ae85-0f9a-4804-a6c4-85e6e1da2578",
    "gid": "yYfY2jqdYJf8yYfY2jqdqYjyD8dfAWTj2iK0jWEx1xVij828ITAfUU8884q824q8q8qJiiJd",
    "a1": "18d8593e3b0edq7k95f6ahlhjf9nkqdpd890p917w50000430543",
    "websectiga": "9730ffafd96f2d09dc024760e253af6ab1feb0002827740b95a255ddf6847fc8",
    "webId": "06419f609ffa0ad3369674cc463e7a89",
    "web_session": "040069b4b7bfaf3183716fb5f6374b56712509",
    "xsecappid": "xhs-pc-web",
    "webBuild": "4.1.6",
}
# 创建csv writer
file = open(
    "./comments/comments_xiaohongshu.csv", mode="w", encoding="utf-8-sig", newline=""
)
csv_writer = csv.writer(file)
csv_writer.writerow(["comment"])

# 查询关键字，并从选择最热的至多前n（可调）个笔记，摘取其评论
for keyword in SEARCH_KEYWORDS:
    # FIXME: 此处的data只能这样传入并修改，否则406，可能是编码问题，但暂不明晰为何导致此结果
    data = json.dumps(post_json_body, separators=(",", ":"))
    data = re.sub(r'"keyword":".*?"', f'"keyword":"{keyword}"', data)
    response = requests.post(
        url=SEARCH_URL,
        cookies=cookies,
        headers=post_request_header,
        data=data.encode("utf-8"),
    )
    print(response)
    response_json = response.json()
    num=0
    for note_item in response_json["data"]["items"]:
        note_id_list.append(note_item["id"])
        num+=1
        if(num>=MAX_NOTES_PER_KEYWORD):
            break

# 获取评论数据
for note_id in note_id_list:
    cursor = ""
    while True:
        # 请求并抓取数据
        response = requests.get(
            url=get_comments_url(note_id, cursor), headers=get_request_header
        )
        response_json = response.json()
        # 添加评论
        for data_item in response_json["data"]["comments"]:
            # TODO: 暂未实现爬取二级评论
            add_comment(data_item["content"])
        # 翻页，如果已经到达最后一页，则爬下一个帖子
        if response_json["data"]["has_more"]:
            cursor = response_json["data"]["cursor"]
        else:
            break

file.close()
