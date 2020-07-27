import vk_api
import time


class CommentsMiner:
    """
    Класс для работы с API Вконтакте

    Аргументы:
    login (str): логин Вконтакте (номер телефона)
    password (str): пароль Вконтакте
    """

    def __init__(self, login, password):
        vk_session = vk_api.VkApi(login, password)
        vk_session.auth()
        self.vk = vk_session.get_api()

    def is_commented(self, group_id):
        """ Проверка на возможность оставлять комментарии в сообществе.

        Аргументы:
        group_id (str): числовой идентификатор группы
        """

        group_id = -group_id
        post = self.vk.wall.get(owner_id=group_id, count=1, offset=2)['items'][0]
        return bool(post['comments']['can_post'])

    def get_comments(self, group_id, num_of_comments=500, delimiter="/t"):
        """" Получение комментариев из сообщества.
        Комментарии записываются в файл с именем сообщества (создается автоматически).
        Файл сохраняется в папку 'comments'.

        Аргументы:
        group_id (int): числовой идентификатор группы
        num_of_comments (int): число комментариев для извлечения (default 500)
        delimiter (str): разделитель (default "/t")
        """

        start_time = time.time()

        group_name = self.vk.groups.getById(group_id=group_id)[0]['name']
        file = open(f'comments/{group_name}.txt', 'w')
        print(f'Начинаем получение {num_of_comments} комментариев из сообщества {group_name}.')

        group_id = -group_id
        comments_extracted = 0
        offset = 5

        while 1:
            # получаем 100 постов
            # vk api позволяет получать за раз не более 100 постов
            posts_list = self.vk.wall.get(owner_id=group_id,count=100, offset=offset)
            # в цикле извлекаем комментарии из каждого поста
            for post in posts_list['items']:
                    post_id = str(post['id'])
                    comments_list = self.vk.wall.getComments(owner_id=group_id,
                                           post_id=post_id, count=20, offset=0)
                    for com in comments_list['items']:
                            # если комментарий содержит текст, записываем его в файл
                            if 'text' in com:
                                com_text = com['text'].replace('\n', '')
                                if com_text !='':
                                    file.write(com_text+'\t')
                                    comments_extracted += 1
                                    # данный код выполняется если получено нужное количество комментариев
                                    if comments_extracted == num_of_comments:
                                        print(f"extracted comments: {comments_extracted}")
                                        print(f'Получение {comments_extracted} комментариев завершено')
                                        print(f'Время: {time.time() - start_time} секунд')
                                        file.close()
                                        return
                    print(f"extracted comments: {comments_extracted}")
            # смещение на 100 для получения новых постов
            offset += 100
