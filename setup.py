from setuptools import setup, find_packages

setup(
    name="acm-helper",
    version="0.1.0",
    packages=find_packages(),
    # 或者明确指定包
    # packages=['ACM_helper'],
    install_requires=[],
    author="Your Name",
    author_email="your.email@example.com",
    description="ACM competition helper library",
)