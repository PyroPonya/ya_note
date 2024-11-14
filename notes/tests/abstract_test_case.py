from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class AbstractTestCase(TestCase):
    """Абстрактный класс для наследования тестов."""
    SLUG_FOR_ARGS = None
    NOTES_HOME_URL = reverse('notes:home')
    NOTES_LIST_URL = reverse('notes:list')
    NOTES_ADD_URL = reverse('notes:add')
    NOTES_DETAIL_URL = None
    NOTES_EDIT_URL = None
    NOTES_DELETE_URL = None
    NOTES_SUCCESS_URL = reverse('notes:success')
    USERS_SIGNUP_URL = reverse('users:signup')
    USERS_LOGIN_URL = reverse('users:login')
    USERS_LOGOUT_URL = reverse('users:logout')

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='user',
        )
        cls.author = User.objects.create_user(
            username='author',
        )
        cls.user_client = Client()
        cls.user_client.force_login(cls.user)
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.note = Note.objects.create(
            title='Title',
            text='Text',
            slug='note-slug',
            author=cls.author,
        )
        cls.SLUG_FOR_ARGS = (cls.note.slug,)
        cls.NOTES_DETAIL_URL = reverse('notes:detail', args=cls.SLUG_FOR_ARGS)
        cls.NOTES_EDIT_URL = reverse('notes:edit', args=cls.SLUG_FOR_ARGS)
        cls.NOTES_DELETE_URL = reverse('notes:delete', args=cls.SLUG_FOR_ARGS)

    class Meta:
        abstract = True
