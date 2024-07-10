from setuptools import setup, find_packages


setup(
    name='mkdocs-exercises',
    version='0.1.0',
    description='Support for exercises in MkDocs',
    long_description='',
    keywords='mkdocs',
    url='',
    author='Yves Chevallier',
    author_email='yves.chevallier@heig-vd.ch',
    license='MIT',
    python_requires='>=3.4',
    install_requires=[
        'mkdocs>=1.6'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ],
    packages=find_packages(),
    entry_points={
        'mkdocs.plugins': [
            'exercises = mkdocs_exercises.plugin:Exercises'
        ]
    }
)
