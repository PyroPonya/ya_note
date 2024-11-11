from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from notes.models import Note
from notes.forms import NoteForm

User = get_user_model()


class TestContent(TestCase):
    NOTES_LIST_URL = reverse('notes:list')

    def setUp(self):
        self.user = User.objects.create_user(
            username='user'
        )
        self.author = User.objects.create_user(
            username='author'
        )
        self.note = Note.objects.create(
            title='title_1',
            text='body',
            author=self.author,
        )

        self.form_data = {
            'title': 'Новый заголовок',
            'text': 'Новый текст',
        }

    # отдельная заметка передаётся на страницу со списком заметок в списке object_list в словаре context;
    def test_note_in_list(self):
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)

    # в список заметок одного пользователя не попадают заметки другого пользователя;
    def test_notes_for_different_users(self):
        note = Note.objects.create(
            title='title_2',
            text='body',
            author=self.user,
        )
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_LIST_URL)
        object_list = response.context['object_list']
        self.assertNotIn(note, object_list)

    # на страницы создания и редактирования заметки передаются формы.
    def test_pages_contains_form(self):
        self.client.force_login(self.author)
        urls = (
            reverse('notes:add'),
            reverse('notes:edit', args=(self.note.slug,)),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertIsInstance(response.context['form'], NoteForm)
