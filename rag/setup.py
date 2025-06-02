from setuptools import setup

setup(
    name='myscript',
    version='0.1',
    py_modules=['myscript'],
    entry_points={
        'console_scripts': [
            'myscript = myscript:main',
        ],
    },
)