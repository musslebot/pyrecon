try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
      name='PyRECONSTRUCT',
      version='1.3.2',
      author='Michael Musslewhite',
      author_email='mdmusslewhite@gmail.com',
      url='https://github.com/wtrdrnkr/pyrecon',
      packages=[
                'pyrecon',
                'pyrecon.tools',
                'pyrecon.toolsgui',
                ],
      license='LICENSE.txt',
      description='Python tools for interacting with XML files associated with RECONSTRUCT',
      long_description=open('README.txt').read(),
      install_requires=[
                        "cython >= 0.19.1",
                        "numpy >= 1.7.1",
                        "scipy >= 0.12.0",
                        "matplotlib >= 1.2.1",
                        "ipython >= 0.13.2",
                        "pandas >= 0.12.0",
                        "sympy >= 0.7.3", 
                        "nose >= 1.3.0",
                        "shapely >= 1.2.18",
                        "scikit-image >= 0.8.2",
                        "lxml >= 3.2.3",
                        "openpyxl >= 1.6.2",
                        "PySide >= 1.2.1",
                        ],
      )
