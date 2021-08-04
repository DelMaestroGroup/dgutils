import setuptools

with open('README.md') as f:
    long_description = f.read()

setuptools.setup(
    name='dgutils',
    version='0.2.5',
    packages=setuptools.find_packages(),
    license='MIT',
    description='A python package implenting useful utilities used by the Del Maestro Group.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=['numpy','scipy'],
    python_requires='>=3.6',
    url='https://github.com/DelMaestroGroup/dgutils',
    author='Adrian Del Maestro',
    author_email='adrian@delmaestro.org',
    classifiers=[
   'License :: OSI Approved :: MIT License',
   'Programming Language :: Python :: 3.6',
   'Programming Language :: Python :: 3.7',
   'Topic :: Scientific/Engineering :: Physics']
)
