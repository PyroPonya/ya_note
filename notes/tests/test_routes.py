from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user',
        )
        cls.author = User.objects.create_user(
            username='author',
        )
        cls.note = Note.objects.create(
            title='title',
            text='body',
            author=cls.author,
        )

    # Главная страница доступна анонимному пользователю.
    def test_home_page_anonymous(self):
        response = self.client.get(reverse('notes:home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    # Аутентифицированному пользователю доступна страница со списком заметок notes/, страница успешного добавления заметки done/, страница добавления новой заметки add/.
    def test_pages_availability_for_auth_user(self):
        self.client.force_login(self.user)
        urls = (
            reverse('notes:list'),
            reverse('notes:success'),
            reverse('notes:add'),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    # Страницы отдельной заметки, удаления и редактирования заметки доступны только автору заметки. Если на эти страницы попытается зайти другой пользователь — вернётся ошибка 404.
    def test_notes_availability_for_author(self):
        urls = (
            reverse('notes:detail', args=(self.note.slug,)),
            reverse('notes:edit', args=(self.note.slug,)),
            reverse('notes:delete', args=(self.note.slug,)),
        )
        self.client.force_login(self.author)
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_notes_availability_for_not_author(self):
        urls = (
            reverse('notes:detail', args=(self.note.slug,)),
            reverse('notes:edit', args=(self.note.slug,)),
            reverse('notes:delete', args=(self.note.slug,)),
        )
        self.client.force_login(self.user)
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    # При попытке перейти на страницу списка заметок, страницу успешного добавления записи, страницу добавления заметки, отдельной заметки, редактирования или удаления заметки анонимный пользователь перенаправляется на страницу логина.
    def test_redirects(self):
        urls = (
            reverse('notes:list'),
            reverse('notes:success'),
            reverse('notes:add'),
            reverse('notes:detail', args=(self.note.slug,)),
            reverse('notes:edit', args=(self.note.slug,)),
            reverse('notes:delete', args=(self.note.slug,)),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                redirect_url = f'/auth/login/?next={url}'
                self.assertRedirects(response, redirect_url)

    # Страницы регистрации пользователей, входа в учётную запись и выхода из неё доступны всем пользователям.
    def test_pages_availability_for_all_users(self):
        urls = (
            reverse('users:signup'),
            reverse('users:login'),
            reverse('users:logout'),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)
