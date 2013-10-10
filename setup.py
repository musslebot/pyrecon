from distutils.core import setup
# Not sure that all of the listed install_requires are actually required --Michael Musslewhite
setup(
      name='PyRECONSTRUCT',
      version='0.2',
      author='Michael Musslewhite',
      author_email='mdmusslewhite@gmail.com',
      packages=[
                'tools',
                'toolsgui'
                ],
      license='LICENSE.txt',
      long_description=open('README.txt').read(),
      install_requires=[
                        "numpy == 1.7.1",
                        "scipy == 0.12.0",
                        "matplotlib == 1.2.1",
                        "ipython == 0.13.2",
                        "pandas == 0.12.0",
                        "sympy == 0.7.3",
                        "nose == 1.3.0",
                        "shapely == 1.2.18",
                        "cython == 0.19.1",
                        "scikit-image == 0.8.2",
                        "lxml == 3.2.3"
                        ],
      )