# coding: utf-8

from __future__ import absolute_import
from setuptools import setup, find_packages


setup(name='m3-audit',
      version='2.1.2',
      url='https://bitbucket.org/barsgroup/m3_audit',
      license='MIT',
      author='BARS Group',
      author_email='bars@bars-open.ru',
      description=u'Аудит операций в прикладной системе',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=(
          'm3-django-compat>=1.1.0',
          'm3-ui',
          'm3-core',
      ),
      include_package_data=True,
      classifiers=[
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Natural Language :: Russian',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 5 - Production/Stable',
      ],
      )
