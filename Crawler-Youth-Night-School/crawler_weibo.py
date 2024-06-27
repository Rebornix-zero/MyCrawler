import requests
import csv
import re

URL_INFO = [
    {"id": "4968708394976919", "uid": "2097152664"},
    {"id": "4990792443628779", "uid": "3074181393"},
    {"id": "4968721531011748", "uid": "1700648435"},
    {"id": "4976379780925584", "uid": "2656274875"},
    {"id": "4982398804296493", "uid": "1784473157"},
    {"id": "4978813251361043", "uid": "1915671961"},
    {"id": "4990887247481207", "uid": "2318910945"},
    {"id": "4967545120752793", "uid": "2286092114"},
    # {"id":"","uid":""},
]
URL_TEMPLATE = "https://weibo.com/ajax/statuses/buildComments?is_reload=1&id={}&uid={}&max_id={}&is_show_bulletin=2&is_mix=0&count=20&fetch_level=0&locale=en-US"
COOKIE = "SUB=_2A25Ix8MIDeRhGeFI7lEV8yzJzTiIHXVrvVrArDV8PUNbmtANLWnDkW9NfRIpRVISWN-U4JOc9bKZlibJfDhe4MNF; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9Whm0FQ5MC7zxJ_oDPmOAiwI5JpX5o275NHD95QNSo-0SheESKqXWs4DqcjMi--NiK.Xi-2Ri--ciKnRi-zNSo.feh.EeKec1Btt; SINAGLOBAL=3159272990297.871.1706199052192; ULV=1707324187844:2:1:1:8590051356832.176.1707324187763:1706199054217; XSRF-TOKEN=f7Sw2kqx1kfSgXGg9GwdSQQz; WBPSESS=qW8mgATp6PM1SIUwfuePwSbF5zHmMGdKPasLc-y5ZsXi9DN_uXcuGkMN9FdiKsW4OPh7KKpkZIlguPePzcTiH3dfBqJhZGQVIQmS9qHy6VURi6u70TDmvWZh37LsKQa_fI6zkBp44lzQHu_Vsv2hXQ==; _s_tentry=weibo.com; Apache=8590051356832.176.1707324187763; ALF=1707929047; SSOLoginState=1707324248"
REFERER = "https://weibo.com/2097152664/NsPpZkSIT"
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


# @brief 将请求页面中展示出的评论进行处理，并加入文件中
# @param comments 该评论对应的comment object list
# TODO: 当前的对评论回复只能爬取到页面显示的部分，隐藏的评论需要进行额外的request
def handle_comments(comments):
    for comment_item in comments:
        add_comment(comment_item["text_raw"])


# @brief 使用URL模板与对应的id，页码等，组合出一个有效的url
# @param info_item 帖子相关信息，主要是id和uid等
# @param max_id 页码参数
# @return 有效的url
def get_url(info_item, max_id):
    return URL_TEMPLATE.format(info_item["id"], info_item["uid"], max_id)


# MAIN
file = open("./comments/comments_weibo.csv", mode="w", encoding="utf-8-sig", newline="")
csv_writer = csv.writer(file)
csv_writer.writerow(["comment"])
# 请求头
request_header = {"cookie": COOKIE, "referer": REFERER, "user_agent": USER_AGENT}
for info_item in URL_INFO:
    max_id = 0
    while True:
        # 请求并抓取数据
        response = requests.get(url=get_url(info_item, max_id), headers=request_header)
        response_json = response.json()
        # 添加评论
        for data_item in response_json["data"]:
            add_comment(data_item["text_raw"])
            handle_comments(data_item["comments"])
        # 翻页，如果已经到达最后一页，则爬下一个帖子
        max_id = response_json["max_id"]
        if max_id == 0:
            break

file.close()
