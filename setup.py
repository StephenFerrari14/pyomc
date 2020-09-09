from setuptools import setup

setup(
    name='pyom',
    version='0.0.1',
    py_modules=['pyom'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pyom=pyom:pyom
    ''',
)