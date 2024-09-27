from setuptools import setup

setup(
    name='CacaCNPJ',
    version='1.0',
    py_modules=['consulta_cnpj'],
    install_requires=[
        'requests',
        'rich',
        'click',
    ],
    entry_points='''
        [console_scripts]
        cacacnpj=consulta_cnpj:main
    ''',
)
