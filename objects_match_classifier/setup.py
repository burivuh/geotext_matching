import os

from setuptools import setup

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    return [dirpath
            for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]


def get_package_data(package):
    """
    Return all files under the root package, that are not in a
    package themselves.
    """
    walk = [(dirpath.replace(package + os.sep, '', 1), filenames)
            for dirpath, dirnames, filenames in os.walk(package)
            if not os.path.exists(os.path.join(dirpath, '__init__.py'))]

    filepaths = []
    for base, filenames in walk:
        if 'test' not in base:
            filepaths.extend([os.path.join(base, filename)
                              for filename in filenames])
    return {package: filepaths}


setup(name='objects_match_classifier',
      version='0.0.1',
      description='A classifier to detect doublicates in OSM and booking objects.',
      long_description=open('../README.md').read(),
      author='Alina',
      author_email='thae@mapswithme.com',
      url='https://github.com/mapsme/geotext_matching',
      py_modules=['objects_match_classifier'],
      download_url='https://github.com/mapsme/geotext_matching/archive/master.zip',
      packages=get_packages('objects_match_classifier'),
      package_data=get_package_data('objects_match_classifier'),
      include_package_data=True
      )
