from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from notes.models import Note

User = get_user_model()


class AbstractTestCase(TestCase):
    """Абстрактный класс для наследования тестов."""
    SLUG_FOR_ARGS = 'note-slug'
    NOTES_HOME_URL = reverse('notes:home')
    NOTES_LIST_URL = reverse('notes:list')
    NOTES_ADD_URL = reverse('notes:add')
    NOTES_DETAIL_URL = reverse('notes:detail', args=(SLUG_FOR_ARGS,))
    NOTES_EDIT_URL = reverse('notes:edit', args=(SLUG_FOR_ARGS,))
    NOTES_DELETE_URL = reverse('notes:delete', args=(SLUG_FOR_ARGS,))
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
            slug=cls.SLUG_FOR_ARGS,
            author=cls.author,
        )

    # Почему это лишние строки?
    # Они же дают явно понять,
    # что класс предназначен только для наследования.
    #
    # class Meta:
    #   abstract = True
