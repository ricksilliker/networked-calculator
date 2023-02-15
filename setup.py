from setuptools import setup, find_packages

setup(
    name='calculator',
    version='0.1.0',
    description='a client and server app that sends math expression to the server and returns the solution.',
    author='Rick Silliker',
    author_email='ricksilliker@gmail.com',
    package_dir={"": "src"},
    package_data={'calculator': ['resources/*']},
    entry_points={
        'console_scripts': [
            'calculator-client = calculator.client:run_client',
            'calculator-server = calculator.server:run_server',
        ]
    },
    zip_safe=False,
    install_requires=['PySide2', 'requests']
)
