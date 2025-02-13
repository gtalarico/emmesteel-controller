from setuptools import setup

setup(
    name='emmesteel',
    version='0.1.0',    
    description='Emmesteel',
    url='https://github.com/gtalarico/emmesteel',
    author='Gui Talarico',
    author_email='gtalarico.dev@gmail.com',
    license='BSD 2-clause',
    packages=['emmesteel'],
    install_requires=['websockets=>13'],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.8',
    ],
)
