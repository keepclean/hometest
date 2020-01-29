from setuptools import setup, find_packages

setup(
    name="weblog_helper",
    version="0.0.1",
    packages=find_packages(),
    description="Returns all log lines that correspond to a given source IP address or CIDR network",
    install_requires=["ipaddress==1.0.19"],
    entry_points={
        "console_scripts": ["weblog_helper = weblog_helper.weblog_helper:main"]
    },
)
