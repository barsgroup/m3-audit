#coding: utf-8
from setuptools import setup, find_packages

requires = []
with open('src/requires.txt', 'r') as f:
    requires.extend(f.readlines())

setup(name='m3-audit',
      version='2.0.1',
      url='https://bitbucket.org/barsgroup/m3_audit',
      license='MIT',
      author='BARS Group',
      author_email='bars@bars-open.ru',
      description=u'Аудит операций в прикладной системе',
      package_dir={'': 'src'},
      packages=find_packages('src'),
      install_requires=requires,
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
