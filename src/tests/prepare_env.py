#coding:utf-8
'''
Модуль, который выполняет подготовку 
'''
import sys
import os
import Queue
import subprocess
import types
import datetime
import shutil
from decimal import Decimal


REPO_LOCATION = 'https://readonly:onlyread@repos.med.bars-open.ru/'
TOPMOST_VERSION = 'zzzzzzzzz'

#===============================================================================
# Точка входа.
#===============================================================================

def start(as_repos=False):
    '''
    Точка входа. 
    '''
    has_error= False
    
    script_root = os.path.dirname(__file__)
    env_root = os.path.join(script_root, '../env')
    envbuild_root = os.path.join(env_root, '.build')
    
    # достаем версию и зависимости основного продукта
    module = import_module('version')
    
    # словарь уже обработанных приложений
    app_queue = Queue.Queue()  
    processed_apps = {}
    synced_locally = {} 
    
    root_version, root_appname, root_require, root_require_locals = app_version('')
    
    print u'--------------------------------------------------------------------'
    print u'Сборка окружения для проекта \'%s\', версия %s' % (root_appname, root_version)
    print u'--------------------------------------------------------------------'
    
    # создаем папки для хранения информации
    if not os.path.exists(env_root):
        os.mkdir(env_root)
        
    #sys.path.insert(0, env_root)
    sys.path.insert(0, os.path.dirname(__file__))
    
        
    if not os.path.exists(envbuild_root):
        os.mkdir(envbuild_root)
    
    # забираем зависимости корневого приложения
    for require_app, require_version in root_require.iteritems():
        app_queue.put(AppDescription(require_app, require_version))
        
    for require_app, require_path in root_require_locals.iteritems():
        app_queue.put(AppDescription(require_app, require_path, is_local=True))
        
    
    #os.chdir('../')
    # основной цикл обработки
    while not app_queue.empty():
        
        # забираем приложение из очереди на обработку
        app = app_queue.get_nowait()
        print '>>', app.name, '(' + app.version + ')'
        
        if app.is_local:
            
            print '  ', u'Выполняется ЛОКАЛЬНАЯ синхронизация исходных текстов приложения', app.name
            
            # данное приложение необходимо синхронизировать только локально
            # поэтому тупо копируем данные
            # путь к исходным текстам по счастливой случайности хранится
            # в app.version
            
            if not os.path.exists(app.version):
                print '!!', u'Папка исходных текстов', app.version, u'не найдена'
                has_error = True
                continue
            
            copy_sources(app.name, env_root, app.version)
            
            # отмечаем, что данное приложение имеет наивысшую версию
            # и не может быть замещено ни одиним другим набором исходников
            # из репозитариев или других папок
            processed_apps[app.name] = TOPMOST_VERSION
            synced_locally[app.name] = app.version
            
        else:
            
            if processed_apps.get(app.name, '.') >= app.version:
                # точка всегда "меньше" любого другого символа
                print '  ', u'Исходные тексты', app.name, u'находятся в актуальном состоянии'
                continue
            # подготовка приложения
            app_repo_root = os.path.join(envbuild_root, app.name) 
            if not os.path.exists(app_repo_root):
                print '  ', u'Клонирование репозитария приложения', app.name
                if not clone_repo(app.name, app_repo_root):
                    has_error = True
                    print '!!', u'Исходные тексты приложения', app.name, u'из-за возникшей ошибки находятся в неактуальном состоянии'
                    continue
            else:
                print '  ', u'Пул репозитария приложения', app.name
                if not pull_repo(app_repo_root):
                    has_error = True
                    print '!!', u'Исходные тексты приложения', app.name, u'из-за возникшей ошибки находятся в неактуальном состоянии'
                    continue
            
            print '  ', u'Обновление репозитария приложения', app.name, u'на ветку', app.version
            if not update_repo(app_repo_root, app.version):
                has_error = True
                print '!!', u'Исходные тексты приложения', app.name, u'из-за возникшей ошибки находятся в неактуальном состоянии'
                continue
        
            # копируем получившееся в ./env
            print '  ', u'Копирование исходных кодов приложения в env'    
            copy_sources(app.name, env_root, app_repo_root)
            
            processed_apps[app.name] = app.version
            
        # производим разбор
        app_source_path = os.path.join(env_root, app.name)
        if os.path.exists(os.path.join(app_source_path, 'version.py')):
            sys.path.insert(0, app_source_path)
            _, _, require, require_locals = app_version()
            
            for require_app, require_version in require.iteritems():
                print '  ', app.name, 'требует приложение', require_app, u'версии', require_version
                app_queue.put(AppDescription(require_app, require_version))
    
    print u'--------------------------------------------------------------------'
    if has_error:
        print u'Сборка окружения завершена С ОШИБКАМИ.'
    else:
        print u'Сборка окружения успешно завершена'
        
    print u'--------------------------------------------------------------------'
    print u'Выполнена синхронизация следующих пакетов:'
    print '  ', root_appname + ':', root_version
    for app, version in processed_apps.iteritems():
        print '  ', app + ':', synced_locally.get(app, version)
    
def clone_repo(app_name, app_repo_root):
    
    out, err = run_command(['hg', 'clone', REPO_LOCATION + app_name, app_repo_root])
    if err:
        print '  ', u'Клонирование репозитория', REPO_LOCATION + app_name, u'завершено с ошибкой:', err
        
    return not err

def pull_repo(app_repo_root):
    
    out, err = run_command(['hg', 'pull', '-R', app_repo_root])
    if err:
        print '  ', u'Пул репозитория', app_repo_root, u'завершен с ошибкой:', err
        
    return not err

def update_repo(app_repo_root, app_version):
    
    out, err = run_command(['hg', 'update', app_version, '-R', app_repo_root])
    if err:
        print '  ', u'Обновление репозитория', app_repo_root, u'не ветку', app_version, u'завершено с ошибкой:', err
        
    return not err

def copy_sources(app_name, env_root, app_repo_root):
    
    app_source_root = os.path.join(env_root, app_name)
    if os.path.exists(app_source_root):
        shutil.rmtree(path=app_source_root)
    
    shutil.copytree(src=os.path.join(app_repo_root, 'src/' + app_name), dst=app_source_root)
    

def app_version(app_name=''):    
    '''
    Возвращает кортеж из трех элементов (app_version, require, require_local)
    '''
    module = import_module('%s.version' % app_name if app_name else 'version' )
    reload(module)
        
    return (module.__version__,
            module.__appname__,
            module.__require__,
            module.__require_local__ if hasattr(module, '__require_local__') else {},)
    
#===============================================================================
# Внутренние классы
#===============================================================================
class AppDescription(object):
    
    def __init__(self, name='', version='', is_local = False):
        self.name = name
        self.version = version
        self.is_local = is_local

#===============================================================================
# Внутренние функции
#===============================================================================
def run_command(command):
    '''
    Выполняет команду как subprocess,
    возвращает (stdout, stderr) процесса 
    '''
    popen = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    popen.wait()
    return popen.communicate()


def _resolve_name(name, package, level):
    """Return the absolute name of the module to be imported."""
    if not hasattr(package, 'rindex'):
        raise ValueError("'package' not set to a string")
    dot = len(package)
    for x in xrange(level, 1, -1):
        try:
            dot = package.rindex('.', 0, dot)
        except ValueError:
            raise ValueError("attempted relative import beyond top-level "
                              "package")
    return "%s.%s" % (package[:dot], name)


def import_module(name, package=None):
    """Import a module.

    The 'package' argument is required when performing a relative import. It
    specifies the package to use as the anchor point from which to resolve the
    relative import to an absolute import.

    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]

def force_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_unicode, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    # Handle the common case first, saves 30-40% in performance when s
    # is an instance of unicode. This function gets called often in that
    # setting.
    if isinstance(s, unicode):
        return s
    if strings_only and is_protected_type(s):
        return s
    try:
        if not isinstance(s, basestring,):
            if hasattr(s, '__unicode__'):
                s = unicode(s)
            else:
                try:
                    s = unicode(str(s), encoding, errors)
                except UnicodeEncodeError:
                    if not isinstance(s, Exception):
                        raise
                    # If we get to here, the caller has passed in an Exception
                    # subclass populated with non-ASCII data without special
                    # handling to display as a string. We need to handle this
                    # without raising a further exception. We do an
                    # approximation to what the Exception's standard str()
                    # output should be.
                    s = ' '.join([force_unicode(arg, encoding, strings_only,
                            errors) for arg in s])
        elif not isinstance(s, unicode):
            # Note: We use .decode() here, instead of unicode(s, encoding,
            # errors), so that if s is a SafeString, it ends up being a
            # SafeUnicode at the end.
            s = s.decode(encoding, errors)
    except UnicodeDecodeError, e:
        if isinstance(s, Exception):
            
            # If we get to here, the caller has passed in an Exception
            # subclass populated with non-ASCII bytestring data without a
            # working unicode method. Try to handle this without raising a
            # further exception by individually forcing the exception args
            # to unicode.
            s = ' '.join([force_unicode(arg, encoding, strings_only,
                    errors) for arg in s])
    return s

def is_protected_type(obj):
    """Determine if the object instance is of a protected type.

    Objects of protected types are preserved as-is when passed to
    force_unicode(strings_only=True).
    """
    return isinstance(obj, (
        types.NoneType,
        int, long,
        datetime.datetime, datetime.date, datetime.time,
        float, Decimal)
    )


if __name__ == '__main__':
    start()
