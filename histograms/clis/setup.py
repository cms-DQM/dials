from setuptools import setup

setup(
    name='dqm_playground_cli',
    version='0.1.0',
    py_modules=['dqm_playground_cli'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'dqm_playground_cli = dqm_playground_cli:cli',
        ],
    },
)
