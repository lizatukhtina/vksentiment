from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
import os


class CommentsResearcher:
    """ Класс для анализа тональности комментариев """

    def __init__(self):
        self.tokenizer = RegexTokenizer()
        self.model = FastTextSocialNetworkModel(tokenizer=self.tokenizer)

    def get_sentiment(self, file):
        """ Опредение тональности комментариев
        Возвращает 2 значения:
        - distribution (dict)
            словарь в количеством комментариев в разных категориях
        - sentiments (dict)
            словарь с тональностью каждого комментария
        Подробная информация о результатах записывается в файл с именем сообщества.
        Файл сохраняется в папку 'reports'.

        Аргументы:
        file (_io.TextIOWrapper): текстовой файл с комментариями (разделитель \t)
        """

        comments = file.read().split('\t')
        f_name = os.path.basename(file.name)
        
        # получение тональности для комментариев с помощью модели
        results = self.model.predict(comments[0:-1], k=1)
        output = []
        distribution = {}
        sentiments = {}

        for comment, sentiment in zip(comments, results):
            comment_sentiment = list(sentiment.keys())[0]
            output.append(comment_sentiment)
            sentiments[comment] = comment_sentiment

        # подсчет результатов для каждой категории
        distribution['positive'] = output.count('positive')
        distribution['negative'] = output.count('negative')
        distribution['neutral'] = output.count('neutral')
        distribution['skip'] = output.count('skip')
        distribution['speech'] = output.count('speech')

        # вызов функции для создания txt-отчета
        self.detailed_report(f_name, sentiments, distribution)

        return distribution, sentiments

    def detailed_report(self, group_name, sentiments, distribution):
        """ Создание детального txt-отчета.
        Вспомогательный метод для get_sentiment.
        Не рекомендуется для использования в качестве самостоятельной функции.
        """

        file = open(f'reports/{group_name}', 'w')
        file.write(f'Тональность комментариев из сообщества {group_name.replace(".txt", "")}: \n')

        negative = [k for k,v in sentiments.items() if v == 'negative']
        positive = [k for k,v in sentiments.items() if v == 'positive']
        neutral = [k for k,v in sentiments.items() if v == 'neutral']
        skip = [k for k,v in sentiments.items() if v == 'skip']
        speech = [k for k,v in sentiments.items() if v == 'speech']

        file.write(f'\nНегативные комментарии: {distribution["negative"]}\n\n')
        for comment in negative:
            file.write(comment + '\n')

        file.write(f'\nПозитивные комментарии: {distribution["positive"]}\n\n')
        for comment in positive:
            file.write(comment + '\n')

        file.write(f'\nНейтральные комментарии: {distribution["neutral"]}\n\n')
        for comment in neutral:
            file.write(comment + '\n')

        file.write(f'\nКомментарии без смысла: {distribution["skip"]}\n\n')
        for comment in skip:
            file.write(comment + '\n')

        file.write(f'\nРечь, цитирование: {distribution["speech"]}\n\n')
        for comment in speech:
            file.write(comment + '\n')

        file.close()
