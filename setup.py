import setuptools
import typing as t
import os


_HERE = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))

classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Text Processing :: Linguistic'
        ]


def parse_requirements(
        requirements_path: str = 'requirements.txt') -> t.List[str]:
    """Read contents of requirements.txt file and return data from its relevant lines.

    Only non-empty and non-comment lines are relevant.
    """
    requirements = []
    with open(os.path.join(_HERE, requirements_path)) as reqs_file:
        for requirement in [line.strip() for line in reqs_file.read().splitlines()]:
            if not requirement or requirement.startswith('#'):
                continue
            requirements.append(requirement)

    return requirements


setuptools.setup(
    name='vsmlib',
    version='0.1.1',
    url='http://vsm.blackbird.pw/',
    classifiers=classifiers,
    keywords=['NLP', 'linguistics', 'language'],
    install_requires=parse_requirements(),
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*'])
    )
