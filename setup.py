#!/usr/bin/env python

from setuptools import setup

with open('README.rst', encoding='utf-8') as readme_file:
    readme = readme_file.read()


def read_requirements():
    with open('requirements.in', encoding='utf-8') as fobj:
        lines = [line.split('#', 1)[0].strip()
                 for line in fobj]
    # drop empty lines:
    return [line for line in lines if line]


install_requires = read_requirements()

setup(
    name='gcpfwup',
    version='1.0.0',
    description="Firewall rule updater for Google Cloud Platform",
    long_description=readme,
    author="Peter Demin",
    author_email='peterdemin@gmail.com',
    url='https://github.com/peterdemin/gcpfwup',
    py_modules=['update_firewall_ip', 'test_update_firewall_ip'],
    entry_points={
        'console_scripts': [
            'gcpfwup=update_firewall_ip:main'
        ]
    },
    install_requires=install_requires,
    license="MIT license",
    zip_safe=False,
    keywords='GCP Firewall',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.8',
    tests_require=['pytest'],
)
