import jieba
import wordcloud

STOP_WORDS = ["我", "你", "他", "的", "了", "啊", "都", "吗","呢", "是", "就", "不", "也","在"]

file = open("./comments/comments_weibo.csv", encoding="utf-8-sig", mode="r")
content = file.read()
word_list = jieba.lcut(content)
string = " ".join(word_list)

wc = wordcloud.WordCloud(
    stopwords=STOP_WORDS,
    width=720,
    height=720,
    background_color="white",
    scale=15,
    font_path="msyh.ttc",
    repeat=False
)

wc.generate(string)
wc.to_file("./comments/word_cloud.png")
