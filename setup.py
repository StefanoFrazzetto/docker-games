import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
    setuptools.setup(
        name='docker-games',
        version='1.0.0-alpha2',
        author='Stefano Frazzetto',
        author_email='stefano+pypi@hey.com',
        description='Easily create game servers using Docker and Python.',
        long_description=long_description,
        long_description_content_type='text/markdown',
        url='https://github.com/StefanoFrazzetto/DockerGameServers',
        packages=setuptools.find_packages(),
        python_requires='>=3.6',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Operating System :: OS Independent',
            'Topic :: Games/Entertainment',
            'Topic :: Communications :: Conferencing',
            'Topic :: Software Development :: Libraries',
        ],
        keywords=[
            'automation',
            'game',
            'multiplayer',
            'server',
            'cloud',
        ],
        install_requires=[
            'docker'
        ],
        extras_require={
            'test': ['pytest'],
        },
        project_urls={
            'Bug Reports': 'https://github.com/StefanoFrazzetto/DockerGameServers/issues',
            'Source': 'https://github.com/StefanoFrazzetto/DockerGameServers',
        },
    )
