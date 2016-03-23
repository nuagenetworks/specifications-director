# -*- coding:utf-8 -*-

from setuptools import setup
import pip

setup(
    name='specifications-director-server',
    version='0.0.1',
    author='Antoine Mercadal',
    packages=['specsdirector',
              'specsdirector.lib',
              'specsdirector.plugins'],

    author_email='antoine@nuagenetworks.net',
    description='Specification Director Server Package',
    install_requires=[str(ir.req) for ir in pip.req.parse_requirements('requirements.txt', session=pip.download.PipSession())],
    license='TODO',
    url='TODO'
)
