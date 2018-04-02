"""
   @copyright: 2018 by Pauli Rikula <pauli.rikula@gmail.com>
   @license: MIT <http://www.opensource.org/licenses/mit-license.php>
"""

from setuptools import setup
import domain_equations


README = "\n\n".join([
    "# python-domain-equations",
    domain_equations.PropertyGraph.__doc__])

with open('README.md', 'wt') as readme_file:
    readme_file.write(README)


setup(
    name='python-domain-equations',
    version='0.0.8',
    description='python-domain-equations',
    long_description=README,
    license="MIT",
    author="Pauli Rikula",
    url='https://github.com/kummahiih/python-domain-equations',
    packages=['domain_equations'],
    python_requires='~=3.6',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6'],
    install_requires=['python-category-equations == 0.3.7']
)

