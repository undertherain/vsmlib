import setuptools


classifiers = [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Computational Linguists',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Natural Language Processing'
        ],

setuptools.setup(
    name='vsmlib',
    version='0.1',
    url='http://vsm.blackbird.pw/',
    classifiers=classifiers,
    keywords=['NLP', 'linguistics', 'language'],
    packages=setuptools.find_packages(exclude=['contrib', 'docs', 'tests*'])
    )