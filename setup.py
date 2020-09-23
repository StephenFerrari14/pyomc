from setuptools import setup

setup(
    name='pyomc',
    version='1.0.1',
    author='Stephen Ferrari',
    author_email='stephenferrari14@gmail.com',
    description='',
    url="https://github.com/StephenFerrari14/pyomc",
    py_modules=['pyomc'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        pyomc=pyomc:pyomc
    ''',
    python_requires='>=3.6'
)