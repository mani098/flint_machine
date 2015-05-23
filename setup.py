from setuptools import setup

setup(name='flint',
      version='1.0',
      description='OpenShift App',
      author='Mani Kandan',
      author_email='manikandancsea@gmail.com',
      url='http://www.python.org/sigs/distutils-sig/',
     install_requires=['Flask>=0.10.1', 'flask-classy>=0.6.7', 'WTForms>=2.0.2', 'SQLAlchemy>=1.0.3', 'Flask-SQLAlchemy>=2.0', 'MySQL-python>=1.2.5'],)
