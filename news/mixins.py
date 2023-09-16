from django.contrib.auth.mixins import UserPassesTestMixin

class AuthorPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        # Проверяем, является ли текущий пользователь членом группы "authors"
        return self.request.user.groups.filter(name='authors').exists()