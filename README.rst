Google Cloud Firewall Updater
=============================

Overview
--------

A command-line utility to update Google Cloud Platform firewall rules.
Particularly, source IP range for allow SSH rule.

Use case
--------

Harden a personal virtual machine in Google Cloud by allowing only a single IP address to log in through SSH.

Usage
-----

.. code-block::

    gcpfwup service_account_file.json

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
