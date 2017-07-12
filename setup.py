from setuptools import setup, find_packages

setup(
    name='flasky',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'Flask-WTF',
        'flask-login',
        'Flask-SQLAlchemy',
        'Flask-Migrate',
        'Flask-Script',
        'flask-restful'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'Flask-Testing',
        'coverage'
    ]
)
