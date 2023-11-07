from setuptools import setup, find_packages

requirements = []
with open('reqs.txt') as f:
    requirements = f.read().splitlines()

readme = ''
with open('README.md') as f:
    readme = f.read()

setup(
    name='bhaicord.py',
    version='0.0.1',
    author='Your Name',
    author_email='147.himangshu@gmail.com',
    description='A discord API wrapper for python',
    requirements=requirements,
    readme=readme,
    long_description=readme,
    long_description_content_type='text/markdown',
    license='MIT',
    project_urls={
        'Documentation': 'https://github.com/himangshu147-git/bhaicord.py',
        'Issue tracker': 'https://github.com/himangshu147-git/bhaicord.py/issues',
    },
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)