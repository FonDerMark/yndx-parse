from setuptools import setup

with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='yndx_parse',
    version='0.10',
    packages=['yndx_parse'],
    url='https://github.com/FonDerMark/yndx-parse',
    license='MIT',
    author='Xm0rph',
    author_email='publicnox@gmail.com',
    description='some descr',
    long_description_content_type='text/markdown',
    long_description=long_description,
)
