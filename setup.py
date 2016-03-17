from setuptools import setup

version = '0.1.3'

setup(
    name='gsqlite3',
    description="A wrapper for 'sqlite3' to make it play better with 'gevent'",
    version=version,
    author='Giles Brown',
    author_email='giles_brown@hotmail.com',
    url='http://github.com/gilesbrown/gsqlite3',
    download_url = 'http://github.com/gilesbrown/gsqlite3/tarball/' + version,
    license='BSD',
    py_modules=['gsqlite3'],
    install_requires=['gevent>=1.0.1'],
    classifiers=(
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
    ),
    entry_points = """
        [sqlalchemy.dialects]
        sqlite.gsqlite3 = gsqlite3:SQLiteDialect_gsqlite3
    """
)
