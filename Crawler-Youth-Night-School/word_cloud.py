import jieba
import wordcloud

comments_file_path = [
    "./comments/comments_weibo.csv",
    "./comments/comments_xiaohongshu.csv",
]
STOP_WORDS = ["有", "我", "你", "他", "的", "了", "啊", "都", "吗", "呢", "是", "就", "不", "也", "在"]

final_str = ""
for file_path in comments_file_path:
    file = open(file_path, encoding="utf-8-sig", mode="r")
    content = file.read()
    word_list = jieba.lcut(content)
    string = " ".join(word_list)
    final_str = final_str + string + " "
    file.close()

wc = wordcloud.WordCloud(
    stopwords=STOP_WORDS,
    width=1080,
    height=1080,
    max_font_size=300,
    background_color="white",
    scale=15,
    font_path="msyh.ttc",
    repeat=False,
)

wc.generate(final_str)
wc.to_file("./comments/word_cloud.png")
