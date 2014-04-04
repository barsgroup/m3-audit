#coding: utf-8

"""
Приложение, реализующее журналирование действий в m3 и прикладном приложении.
"""

from models import BaseAuditModel
from exceptions import M3AuditException
from manager import AuditManager