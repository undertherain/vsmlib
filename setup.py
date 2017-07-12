import setuptools
import typing as t
import os
import shutil


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


def clean(build_directory_name: str = 'build') -> None:
    """Recursively delete build directory (by default "build") if it exists."""
    build_directory_path = os.path.join(_HERE, build_directory_name)
    if os.path.isdir(build_directory_path):
        shutil.rmtree(build_directory_path)


def setup():
    setuptools.setup(
        name='vsmlib',
        version='0.1.2',
        url='http://vsm.blackbird.pw/',
        classifiers=classifiers,
        keywords=['NLP', 'linguistics', 'language'],
        install_requires=parse_requirements(),
        packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*'])
        )


def main() -> None:
    clean()
    setup()

if __name__ == '__main__':
    main()
