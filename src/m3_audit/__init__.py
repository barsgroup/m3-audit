#coding: utf-8

"""
Приложение, реализующее журналирование действий в m3 и прикладном приложении.

Предполагаемый сценарий использования:
...

Для вызова преднастроенного окна со списком нескольких или одного аудита необходимо
отнаследовать базовый экшнпак аудитов BaseAuditUIActions, где задать в list_audits
необходимые для отображения аудиты

Подключение к проекту
------------------------------

Добавить приложение в settings.py

    .. code-block:: py

        INSTALLED_APPS = (
            ...
            'm3_audit'
        )

В стандартной поставке модуля имеется возможность вести аудит:

    .. code-block:: py

        # аудит таблиц системы:
        AuditManager().write('model-changes', user=request.user)
        # аудит данных в справочниках
        AuditManager().write('dict-changes', user=request.user)
        # аудит авторизации пользователей
        AuditManager().write('auth', user=request.user)
        # аудит изменения прав пользователей
        AuditManager().write('roles', user=request.user)

Можно расширить объекты аудита следующим образом:

    1. создать модель для хранения аудита
    2. зарегистрировать аудит
    3. записывать изменения системы в экшене/представлении

    .. code-block:: py

        # models.py
        class CarsAudit(BaseModelChangeAuditModel):

        class Meta:
            verbose_name = u'Изменения данных в таблице автомобили'
            db_table = 'audit_cars_changes'

        AuditManager().register('cars_change', CarsAudit)

        #views.py

        def some_view(request):
            AuditManager().write('cars_change', user=request.user)

Для отображения окна истории аудита, необходимо добавить :py:class:`m3_audit.action
.BaseAuditUIActions` в контроллер

Пример приложения
-----------------

django==1.3.7

south

m3-core

m3_ext

m3_audit

создаем пустой проект джанго. настраиваем settings.py

    .. code-block:: py

        ...
        TEMPLATE_LOADERS = (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'm3_ext.ui.js_template_loader.load_template_source',
        )

        ...
        MIDDLEWARE_CLASSES = (
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'm3.PrettyTracebackMiddleware'
        )

        ...
        TEMPLATE_CONTEXT_PROCESSORS = (
            "django.contrib.auth.context_processors.auth",
            "django.core.context_processors.debug",
            "django.core.context_processors.i18n",
            "django.core.context_processors.media",
            "django.core.context_processors.static",
            "m3_ext.desktop_processor",
        )

        ...
        INSTALLED_APPS = (
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.admin',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',
            'm3',
            'm3_ext',
            'm3_ext.ui',
            'm3_audit'
        )

создаем приложение cars

    .. code-block:: py

        #-----------------
        # actions.py
        #-----------------

        #coding: utf-8

        from m3.actions.dicts.simple import BaseDictionaryModelActions, DictSaveAction
        from m3_audit.actions import BaseAuditUIActions

        from cars.forms import CarsEditWindow
        from cars.models import Car

        class CarsActionPack(BaseDictionaryModelActions):
            # экшенпак приложения автомобили

            url = '/cars'
            model = Car

            verbose_name = u"Автомобили"
            title = u"Автомобили"

            list_columns = [
                ('name', 'name'),
                ('code', 'code'),
            ]

            add_window = edit_window = CarsEditWindow

        class CarsAuditActionPack(BaseAuditUIActions):
            url = '/cars_audit'
            title = u"Аудит проекта"

        #-----------------
        # app_meta.py
        #-----------------

        # coding: utf-8

        from django.conf.urls import defaults

        from m3.actions import ActionController
        from m3_ext.ui import app_ui

        import actions

        # создаем контроллер
        cars_dictionary_controller = ActionController(url='/cars_dictionary')

        def cars_dictionary_view(request):
            # обработчик действий
            return cars_dictionary_controller.process_request(request)


        def register_actions():
            # регистрируем паки в контроллере
            cars_dictionary_controller.packs.extend((
                actions.CarsActionPack(),
                actions.CarsAuditActionPack()
            ))

        def register_urlpatterns():
            # прописываем урл для контроллера
            return defaults.patterns('',
                                     (r'^cars_dictionary/', cars_dictionary_view))


        def register_desktop_menu():
            # регистрируем десктоп элементы
            main_group = app_ui.DesktopLaunchGroup(name=u'Справочники')

            for pack in cars_dictionary_controller.top_level_packs:
                main_group.subitems.append(
                    app_ui.DesktopShortcut(pack=pack)
                )

            app_ui.DesktopLoader.add(app_ui.get_metarole(app_ui.GENERIC_USER),
                                     app_ui.DesktopLoader.START_MENU,
                                     main_group)

        #-----------------
        # forms.py
        #-----------------

        # coding: utf-8

        from m3_ext.ui.windows import ExtEditWindow
        from m3_ext.ui.containers import ExtForm
        from m3_ext.ui.controls import ExtButton
        from m3_ext.ui.fields import ExtStringField


        class CarsEditWindow(ExtEditWindow):]
            # окно добавления/редактирования записи

            def __init__(self, create_new=True, *args, **kwargs):
                super(CarsEditWindow, self).__init__(create_new, *args, **kwargs)

                self.form = ExtForm()

                self.name_field = ExtStringField(name='name')
                self.code_field = ExtStringField(name='code')

                self.form.items.extend((self.name_field, self.code_field))

                save_btn = ExtButton(text=u'Сохранить', handler="submitForm")
                cancel_btn = ExtButton(text=u'Отмена', handler='cancelForm')

                self.buttons.extend((save_btn, cancel_btn))

        # -------------
        # models.py
        # -------------

        # coding: utf-8

        from django.db import models


        class Car(models.Model):

            name = models.CharField(max_length=100)
            code = models.CharField(max_length=100)

|pict1|

.. |pict1| image:: _static/screen.png
"""

from models import BaseAuditModel
from exceptions import M3AuditException
from manager import AuditManager