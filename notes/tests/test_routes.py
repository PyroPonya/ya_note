from http import HTTPStatus

from django.contrib.auth import get_user_model

from .abstract_test_case import AbstractTestCase

User = get_user_model()


class TestRoutes(AbstractTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_redirects(self):
        """При попытке перейти на страницу списка заметок,
        страницу успешного добавления записи,
        страницу добавления заметки, отдельной заметки,
        редактирования или удаления заметки
        анонимный пользователь перенаправляется на страницу логина.
        """
        urls = (
            self.NOTES_LIST_URL,
            self.NOTES_SUCCESS_URL,
            self.NOTES_ADD_URL,
            self.NOTES_DETAIL_URL,
            self.NOTES_EDIT_URL,
            self.NOTES_DELETE_URL,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                redirect_url = f'/auth/login/?next={url}'
                self.assertRedirects(response, redirect_url)

    def test_pages_availability(self):
        """
        PS - надеюсь, я правильно понял твою мысль из рекомендации)).
        Порядок: client => author_client => user_client.

        Главная страница доступна анонимному пользователю.
        Аутентифицированному пользователю доступна страница
        со списком заметок notes/,
        страница успешного добавления заметки done/,
        страница добавления новой заметки add/.
        Страницы отдельной заметки, удаления и редактирования заметки
        доступны только автору заметки.
        Если на эти страницы попытается зайти другой пользователь
        — вернётся ошибка 404.
        Страницы регистрации пользователей,
        входа в учётную запись и выхода из неё
        доступны всем пользователям.
        """
        data = [
            {
                'url': self.NOTES_HOME_URL,
                'client': self.client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.USERS_SIGNUP_URL,
                'client': self.client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.USERS_LOGIN_URL,
                'client': self.client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.USERS_LOGOUT_URL,
                'client': self.client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_HOME_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_LIST_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_ADD_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_DETAIL_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_EDIT_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_DELETE_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_SUCCESS_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.USERS_SIGNUP_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.USERS_LOGIN_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.USERS_LOGOUT_URL,
                'client': self.author_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_HOME_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_LIST_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_ADD_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.NOTES_DETAIL_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.NOT_FOUND
            },
            {
                'url': self.NOTES_EDIT_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.NOT_FOUND
            },
            {
                'url': self.NOTES_DELETE_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.NOT_FOUND
            },
            {
                'url': self.NOTES_SUCCESS_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.USERS_SIGNUP_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.USERS_LOGIN_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.OK
            },
            {
                'url': self.USERS_LOGOUT_URL,
                'client': self.user_client,
                'status_code': HTTPStatus.OK
            }
        ]
        for item in data:
            with self.subTest(url=item['url']):
                response = item['client'].get(item['url'])
                self.assertEqual(response.status_code, item['status_code'])
                if item['status_code'] == HTTPStatus.FOUND:
                    prep_url = '/auth/login/?next=' + item['url']
                    self.assertRedirects(response, prep_url)
