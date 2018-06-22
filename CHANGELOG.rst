.. :changelog:


История изменений
-----------------

2.1.2
+++++
- Проверка анонимности пользователя ``isinstance(user, AnonymousUser)`` 
  заменена на ``user.is_anonymous()``

2.1.1
+++++
- Декоратор ``django.transaction.commit_on_success`` заменен на
  ``m3_django_compat.atomic``.