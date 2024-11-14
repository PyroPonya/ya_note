from django.contrib.auth import get_user_model

from .abstract_test_case import AbstractTestCase
from notes.forms import NoteForm

User = get_user_model()


class TestContent(AbstractTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

    def test_notes_for_different_users(self):
        """
        отдельная заметка передаётся на страницу
        со списком заметок в списке object_list в словаре context.
        в список заметок одного пользователя
        не попадают заметки другого пользователя.
        """
        data = (
            (self.author_client, self.assertIn),
            (self.user_client, self.assertNotIn),
        )
        for (client, assertion) in data:
            with self.subTest(client=client):
                response = client.get(self.NOTES_LIST_URL)
                object_list = response.context['object_list']
                assertion(self.note, object_list)

    def test_pages_contains_form(self):
        """на страницы создания и редактирования заметки передаются формы."""
        urls = (
            self.NOTES_ADD_URL,
            self.NOTES_EDIT_URL,
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.author_client.get(url)
                self.assertIsInstance(response.context.get('form'), NoteForm)
