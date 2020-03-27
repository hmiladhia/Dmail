import pytest

from configDmanager import import_config
import Dmail


def test_config_d_manager_version():
    assert Dmail.__version__ == import_config('PackageConfigs.VersionConfig').version
