from dataclasses import dataclass
from unittest.mock import Mock

import urllib3
from google.cloud.compute_v1.services.firewalls import FirewallsClient
from google.cloud.compute_v1.types import Allowed, Firewall

from update_firewall_ip import FirewallConfiguration, IPUpdater, PublicIPResolver


def test_ip_updater_happy_path():
    pool_manager_mock = Mock(spec_set=urllib3.PoolManager)
    pool_manager_mock.request.return_value = FakeResponse(status=200, data=b"127.0.0.1")
    firewalls_client = Mock(spec_set=FirewallsClient)
    firewalls_client.list.return_value = [
        Firewall(name='name-http', allowed=[Allowed(ports=['80'])]),
        Firewall(name='name-ssh', allowed=[Allowed(ports=['22'])], source_ranges=['192.168.0.1']),
    ]
    ip_updater = IPUpdater(
        public_ip_resolver=PublicIPResolver(
            pool_manager=pool_manager_mock,
        ),
        firewall_configuration=FirewallConfiguration(
            firewalls_client=firewalls_client,
            project="project",
        ),
        verbose=False,
    )

    ip_updater()

    pool_manager_mock.request.assert_called_once_with("GET", "https://ifconfig.me")
    firewalls_client.list.assert_called_once_with(project='project')
    firewalls_client.update.assert_called_once_with(
        project='project',
        firewall='name-ssh',
        firewall_resource=Firewall(
            name='name-ssh',
            allowed=[Allowed(ports=['22'])],
            source_ranges=['127.0.0.1'],
        ),
    )


@dataclass
class FakeResponse:
    status: int
    data: bytes
