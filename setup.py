import setuptools

with open("README.md", "r", encoding="utf-8") as description:
    long_description: str = description.read()

setuptools.setup(
    name='ofd_elastic',
    version='0.0.1',
    author='Egor Zhelvakov',
    author_email='egor.zhelvakov@aisa.ru',
    description='OFD package helper for job',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests>=2.27.1',
        'pydantic>=1.9.0'
    ]
)
