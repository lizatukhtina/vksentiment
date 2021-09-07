# vksentiment

Оценка тональности комментариев сообществ Вконтакте с помощью готовой модели из библиотеки [Dostoevsky](https://github.com/bureaucratic-labs/dostoevsky). Проект создан в рамках прохождения летней практики на кафедре ИС СФУ.

## Описание
Проект состоит из двух основных модулей.
#### comments_mining
Модуль для получения комментариев из сообществ Вконтакте.
#### comments_analysis
Модуль для оценки тональности полученных комментариев.

## Установка

Загрузить библиотеку можно через TestPyPI:

```bash
$ pip install -i https://test.pypi.org/simple/ vksentiment
```
Также необходимо загрузить модель FastTextSocialNetworkModel из библиотки Dostoevsky:

```bash
$ python -m dostoevsky download fasttext-social-network-model
```
## Примеры использования
Получение 500 комментариев из сообщества [СФУ](https://vk.com/siberianfederal) (id: 220664). Полученные комментарии сохранятся в текстовой файл в папке 'comments'. Функция is_commented позволяет проверить, можно ли оставлять комментарии в сообществе.
```python
from comments_mining import CommentsMiner

miner = CommentsMiner('+71234567890', 'vkpassword')
miner.is_commented(220664) # true
miner.get_comments(220664, 500)
```
Анализ тональности 500 комментариев из сообщества СФУ. Подробный отчет с тональностью каждого комментария сохранится в текстовой файл в папку "reports".
```python
from comments_analysis import CommentsResearcher

researcher = CommentsResearcher()
comms = open('comments/Сибирский федеральный университет (СФУ).txt', 'r')

result = researcher.get_sentiment(comms)

comms_by_category = result[0]
print(comms_by_category)
# {'positive': 78, 'negative': 38, 'neutral': 362, 'skip': 13, 'speech': 9}

detailed_result = result[1]
for key in detailed_result.keys():
    print(key, '->', detailed_result[key])
# Я студент ИКИТ. -> neutral
# Второй курс ИАИД. -> neutral
# ...
# Самые лучшие! ❤ -> positive
# Нереально крутые😍💣💥 -> positive
# Огонь просто!! -> positive
# ...
```
 https://github.com/lizatukhtina/vksentiment.git
