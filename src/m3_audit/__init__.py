#coding: utf-8
'''
Приложение, реализующее журналирование действий в m3 и прикладном приложении.

Предполагаемый сценарий использования:
...

Для вызова преднастроенного окна со списком нескольких или одного аудита необходимо
отнаследовать базовый экшнпак аудитов BaseAuditUIActions, где задать в list_audits
необходимые для отображения аудиты
'''

from models import BaseAuditModel
from exceptions import M3AuditException
from manager import AuditManager