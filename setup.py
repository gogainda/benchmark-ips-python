"""Setup configuration for benchmark-ips."""

from setuptools import setup, find_packages
import os


def read_file(filename):
    """Read a file's contents."""
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()


# Read version from package
about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'benchmark_ips', '__init__.py'), 'r', encoding='utf-8') as f:
    for line in f:
        if line.startswith('__version__'):
            exec(line, about)
            break


setup(
    name='benchmark-ips',
    version=about.get('__version__', '2.14.0'),
    description='Iterations per second benchmarking for Python',
    long_description=read_file('README_PYTHON.md') if os.path.exists('README_PYTHON.md') else '',
    long_description_content_type='text/markdown',
    author='Python port by Claude',
    author_email='',
    url='https://github.com/evanphx/benchmark-ips',
    packages=find_packages(exclude=['tests', 'tests.*', 'examples']),
    install_requires=[
        # No external dependencies required
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=3.0.0',
        ],
    },
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Benchmark',
    ],
    keywords='benchmark benchmarking performance testing ips',
    project_urls={
        'Bug Reports': 'https://github.com/evanphx/benchmark-ips/issues',
        'Source': 'https://github.com/evanphx/benchmark-ips',
    },
)
