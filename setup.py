import os
import setuptools

from configDmanager import import_config, update_config

test = os.environ.get('Test', 'True') == 'True'

conf = import_config('PackageConfigs.VersionConfig')

setuptools.setup(**conf)

update_config(lambda c: {'__version.__patch': c['__version.__patch'] + 1 * (not test)}, 'PackageConfigs.VersionConfig')
