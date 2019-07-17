try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

requirements = ['requests']

setup(
    name='tgapi',
    version='0.1.1',
    description='A Python module for I/O of Telegram bot API',
    author='KumaTea',
    url='https://github.com/oudoubleyang/tgapi',
    license='GNU General Public License v3.0',
    keywords='tgapi',
    packages=find_packages(exclude=['example', 'test', 'dist']),
    include_package_data=True,
    install_requires=requirements,
    setup_requires=requirements,
)
