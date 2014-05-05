from setuptools import setup
from setuptools import find_packages

EXCLUDE_FROM_PACKAGES = [
    'porter.bin',
]

version = __import__('porter.version').version

packages = find_packages(exclude=EXCLUDE_FROM_PACKAGES)

print(packages)

setup(
    name='Porter',
    license='BSD',
    version=version.version,
    # include_package_data=True,
    packages=packages,
    scripts=['porter/bin/porter-admin.py'],
    # entry_points={'console_scripts': [
    #     'porter-admin = porter.core.management:execute_from_commandline',
    # ]},
    zip_safe=False,
)
