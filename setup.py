import setuptools
import os

from configDmanager import import_config, ConfigManager

conf = import_config('PackageConfigs.VersionConfig')

with open("README.md", "r") as fh:
    long_description = fh.read()

try:
    setuptools.setup(long_description=long_description, **conf)
finally:
    gversion, version = conf.version.rsplit('.', 1)
    version = int(version) + 1
    conf.version = f"{gversion}.{version}"
    ConfigManager.export_config_file(conf, 'VersionConfig', os.path.join(os.getcwd(), 'PackageConfigs'))
