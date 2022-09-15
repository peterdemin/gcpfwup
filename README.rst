Google Cloud Firewall Updater
=============================

Overview
--------

A command-line utility to update Google Cloud Platform firewall rules.
Particularly, source IP range for allow SSH rule.

Use case
--------

Harden a virtual machine in Google Cloud by allowing only a single IP address to log in through SSH.

Installation
------------

.. code-block::

   pip install gcpfwup

Requires Python 3.8 or newer.
Depends on `google-cloud-compute <https://pypi.org/project/google-cloud-compute/>`_.

Usage
-----

.. code-block::

    gcpfwup -v service_account_file.json

    Target public IP: 101.35.101.248.
    IP(s) allowed for SSH: 127.0.0.1.
    Updating rule to allow only target IP address...
    Done.

The only required argument is a path to Google service account JSON key file.
You can download it from Google Cloud Console.
It should be under IAM & Admin / Service Accounts and needs permissions for Google compute engine.

Help
----

.. code-block::

    gcpfwup --help

    usage: gcpfwup [-h] [-v] [--ip IP] service_account_file

    positional arguments:
      service_account_file  path to Google API service account JSON file

    optional arguments:
      -h, --help            show this help message and exit
      -v, --verbose         increase output verbosity
      --ip IP               use this IP instead of auto-resolved public IP
