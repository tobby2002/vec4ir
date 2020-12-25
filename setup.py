from setuptools import setup

requirements = [
    'boto',
    'bz2file',
    'cycler',
    'decorator',
    'gensim',
    'isodate',
    'matplotlib',
    'networkx',
    'nltk',
    'numpy',
    'pandas',
    'PyYAML',
    'rdflib',
    'requests',
    'scikit-learn',
    'scipy',
    'six',
    'sklearn',
    'smart-open',
    'joblib'

]

setup(name='ir',
      version=0.5,
      description='Neural Word Embeddings for Information Retrieval',
      author="neo",
      author_email="nn",
      # install_requires=requirements,
      # scripts=['bin/ir-evaluate',
      #          'bin/ir-run']
      )
