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

    gcpfwup -v service_account_file.json

Help
----

.. code-block::

    gcpfwup --help
