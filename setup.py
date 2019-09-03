try:
    from setuptools import setup, find_packages
    package = find_packages(exclude=['example', 'test', 'dist'])
except ImportError:
    from distutils.core import setup
    package = ['tgapi']

setup(
    name='tgapi',
    version='0.3.2',
    description='A Python module for I/O of Telegram bot API',
    author='KumaTea',
    author_email='oudoubleyang@outlook.com',
    url='https://github.com/oudoubleyang/tgapi',
    license='MIT License',
    keywords=['tgapi', 'Telegram', 'API', 'IO'],
    packages=package,
    include_package_data=True,
    install_requires=['requests'],
    setup_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',      # 3 - Alpha, 4 - Beta or 5 - Production/Stable
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
