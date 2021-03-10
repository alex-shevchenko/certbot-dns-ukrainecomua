import os
import sys

from setuptools import find_packages
from setuptools import setup

version = '1.14.0.dev0'

# Remember to update local-oldest-requirements.txt when changing the minimum
# acme/certbot version.
install_requires = [
    'setuptools>=39.0.1',
    'zope.interface',
]

if not os.environ.get('SNAP_BUILD'):
    install_requires.extend([
        'acme>=0.31.0',
        'certbot>=1.1.0',
    ])
elif 'bdist_wheel' in sys.argv[1:]:
    raise RuntimeError('Unset SNAP_BUILD when building wheels '
                       'to include certbot dependencies.')
if os.environ.get('SNAP_BUILD'):
    install_requires.append('packaging')

# This package normally depends on dns-lexicon>=3.2.1 to address the
# problem described in https://github.com/AnalogJ/lexicon/issues/387,
# however, the fix there has been backported to older versions of
# lexicon found in various Linux distros. This conditional helps us test
# that we've maintained compatibility with these versions of lexicon
# which allows us to potentially upgrade our packages in these distros
# as necessary.
if os.environ.get('CERTBOT_OLDEST') == '1':
    install_requires.append('dns-lexicon>=2.2.1')
else:
    install_requires.append('dns-lexicon>=3.2.1')

setup(
    name='certbot-dns-ukrainecomua',
    version=version,
    description="Ukraine.com.ua DNS Authenticator plugin for Certbot",
#     url='https://github.com/certbot/certbot',
    author="Alex Shevchenko",
    author_email='caezaris@gmail.com',
    license='Apache License 2.0',
    python_requires='>=3.6',
#     classifiers=[
#         'Development Status :: 5 - Production/Stable',
#         'Environment :: Plugins',
#         'Intended Audience :: System Administrators',
#         'License :: OSI Approved :: Apache Software License',
#         'Operating System :: POSIX :: Linux',
#         'Programming Language :: Python',
#         'Programming Language :: Python :: 3',
#         'Programming Language :: Python :: 3.6',
#         'Programming Language :: Python :: 3.7',
#         'Programming Language :: Python :: 3.8',
#         'Programming Language :: Python :: 3.9',
#         'Topic :: Internet :: WWW/HTTP',
#         'Topic :: Security',
#         'Topic :: System :: Installation/Setup',
#         'Topic :: System :: Networking',
#         'Topic :: System :: Systems Administration',
#         'Topic :: Utilities',
#     ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'certbot.plugins': [
            'dns-ukrainecomua = certbot_dns_ukrainecomua._internal.dns_ukrainecomua:Authenticator',
        ],
    },
)