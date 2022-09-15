import argparse
import json
from typing import List

import urllib3
from google.cloud.compute_v1.services.firewalls import FirewallsClient
from google.cloud.compute_v1.services.firewalls.pagers import ListPager
from google.cloud.compute_v1.types import Firewall

SSH_PORT = 22


def main():
    ip_updater = build_ip_updater_from_cli()
    ip_updater()


class FirewallRule:
    """Wrapper around protobuf madness."""

    def __init__(self, firewall_proto: Firewall) -> None:
        self._firewall_proto = firewall_proto

    @property
    def name(self) -> str:
        return self._firewall_proto.name

    @property
    def ips(self) -> List[str]:
        return list(self._firewall_proto.source_ranges)

    @ips.setter
    def ips(self, ips: List[str]) -> None:
        del self._firewall_proto.source_ranges[:]
        self._firewall_proto.source_ranges.extend(ips)

    def get_proto(self) -> Firewall:
        return self._firewall_proto


class PublicIPResolver:
    _MY_IP_API = 'https://ifconfig.me'

    def __init__(self, forced_ip: str = '', pool_manager: urllib3.PoolManager = None) -> None:
        self.forced_ip = forced_ip
        self._pool_manager = pool_manager or urllib3.PoolManager()

    def __call__(self) -> str:
        if self.forced_ip:
            return self.forced_ip
        response = self._pool_manager.request('GET', self._MY_IP_API)
        if response.status != 200:
            raise RuntimeError('Failed to resolve public IP through {self._MY_IP_API}')
        return response.data.decode('ascii')


class FirewallConfiguration:
    def __init__(self, firewalls_client: FirewallsClient, project: str) -> None:
        self._firewalls_client = firewalls_client
        self._project = project

    def get_rule_by_allowed_port(self, port: int) -> FirewallRule:
        matching_rules = [rule for rule in self._iter_rules() if self._port_is(rule, port)]
        if len(matching_rules) != 1:
            raise ValueError(
                f"Expected 1 firewall rule to allow access on port {port}, "
                f"found {len(matching_rules)}"
            )
        rule = matching_rules[0]
        return FirewallRule(rule)

    def update_rule(self, rule: FirewallRule) -> None:
        self._firewalls_client.update(
            project=self._project,
            firewall=rule.name,
            firewall_resource=rule.get_proto(),
        )

    @staticmethod
    def _port_is(rule: Firewall, port: int) -> bool:
        return str(port) in rule.allowed[0].ports

    def _iter_rules(self) -> ListPager:
        return self._firewalls_client.list(project=self._project)


class IPUpdater:
    def __init__(
        self,
        public_ip_resolver: PublicIPResolver,
        firewall_configuration: FirewallConfiguration,
        verbose: bool,
    ) -> None:
        self._public_ip_resolver = public_ip_resolver
        self._firewall_configuration = firewall_configuration
        self._verbose = verbose

    def __call__(self) -> None:
        """Updates SSH firewall rule to allow this machine."""
        public_ip = self._public_ip_resolver()
        self._debug(f"Target public IP: {public_ip}.")
        rule = self._firewall_configuration.get_rule_by_allowed_port(SSH_PORT)
        self._debug(f"IP(s) allowed for SSH: {', '.join(rule.ips)}.")
        if public_ip in rule.ips:
            self._debug("No action needed.")
            return
        rule.ips = [public_ip]
        self._debug("Updating rule to allow only target IP address...")
        self._firewall_configuration.update_rule(rule)
        self._debug("Done.")

    def _debug(self, text: str) -> None:
        if self._verbose:
            print(text)


def build_ip_updater_from_cli() -> IPUpdater:
    args = parse_args()
    return IPUpdater(
        public_ip_resolver=PublicIPResolver(forced_ip=args.ip or ''),
        firewall_configuration=FirewallConfiguration(
            firewalls_client=FirewallsClient.from_service_account_file(args.service_account_file),
            project=load_project_id(args.service_account_file),
        ),
        verbose=args.verbose,
    )


def load_project_id(service_account_file: str) -> str:
    with open(service_account_file, encoding='utf-8') as fobj:
        service_account_info = json.load(fobj)
    return service_account_info['project_id']


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("service_account_file", help="path to Google API service account JSON file")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--ip", help="use this IP instead of auto-resolved public IP")
    return parser.parse_args()


if __name__ == '__main__':
    main()
