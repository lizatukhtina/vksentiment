from comments_mining import CommentsMiner
from comments_analysis import CommentsResearcher

miner = CommentsMiner('+71234567890', 'vkpassword')
miner.is_commented(220664) # true
miner.get_comments(220664, 500)

researcher = CommentsResearcher()
comms = open('comments/Сибирский федеральный университет (СФУ).txt', 'r')
result = researcher.get_sentiment(comms)
comms_by_category = result[0]
print(comms_by_category)
# {'positive': 78, 'negative': 38, 'neutral': 362, 'skip': 13, 'speech': 9}

detailed_result = result[1]
for key in detailed_result.keys():
    print(key, '->', detailed_result[key])
# ГИ, ИППС. -> neutral
# ИАиД и ИППС?) -> neutral
# ...
# Самые лучшие! ❤ -> positive
# Нереально крутые😍💣💥 -> positive
# Огонь просто!! -> positive
# ...
