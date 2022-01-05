from distutils.core import setup


with open('requirements.txt') as f:
    requires = f.read().splitlines()

requires = [
    r for r in requires
    if not r.startswith("git+https")
]
requires.append('misaka')

setup(
    name="advert_parsing",
    version="0.1",
    packages=['advert_parsing'],
    requires=requires,
    dependency_links=['git+https://github.com/sapristi/misaka.git@master']
)
