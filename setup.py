from setuptools import setup, find_packages

with open('README.md', 'r') as file:
    readme = file.read()

setup(
	name="bsif-utils",
	version="1.0.0",
	author="Blue Sky Infomation Factory",
	description="Utils package.",
	long_description=readme,
	long_description_content_type="text/markdown",
	packages=find_packages(),
	package_data={},
	license="BSD 3-Clause License",
	python_requires=">=3.11",
	classifiers=[
		"License :: OSI Approved :: BSD License",
		"Programming Language :: Python :: 3"
	],
	url="https://github.com/Blue-Sky-Infomation-Factory/Python-utils"
)

# python -m build -w