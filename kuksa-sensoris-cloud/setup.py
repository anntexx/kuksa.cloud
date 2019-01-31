#!/usr/bin/env python
#  Copyright (c) 2019 Eclipse KUKSA project
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0
#
#  SPDX-License-Identifier: EPL-2.0
#
#  Contributors: Robert Bosch GmbH

import subprocess
import os
import sys

from setuptools import setup, find_packages
from distutils.command.build_py import build_py as _build_py
from distutils.command.clean import clean as _clean
from distutils.spawn import find_executable


def generate_proto(source, require=True):
    """This method invokes the protobuf compiler and generates python classed from the proto definitions."""

    if not require and not os.path.exists(source):
        return

    if 'PROTOC' in os.environ and os.path.exists(os.environ['PROTOC']):
        protoc = os.environ['PROTOC']
    else:
        protoc = find_executable("protoc")

    protoc_command = [protoc, "-I../src", "-I.", "--python_out=.", source]
    if subprocess.call(protoc_command) != 0:
        sys.exit(-1)


class clean(_clean):
    def run(self):
        # Delete generated files in the project such as protobug generated files
        for (dirpath, dirnames, filenames) in os.walk("."):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if filepath.endswith("_pb2.py") or filepath.endswith(".pyc"):
                    os.remove(filepath)
        # _clean is an old-style class, so super() doesn't work.
        _clean.run(self)


class build_py(_build_py):
  def run(self):
    # Generate necessary .proto file if it doesn't exist.
    generate_proto("./sensoris-v1.0.0/protobuf/messages/data.proto")
    # TODO other sensoris files need to be added

    # _build_py is an old-style class, so super() doesn't work.
    _build_py.run(self)

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='kuksa-sensoris-cloud',
    version='0.1.0',
    description='Sample application of a Cloud endpoint implementing the Sensoris API v1.0.0.',
    long_description=readme,
    author='Dennis Grewe',
    author_email='dennis.grewe@de.bosch.com',
    url='',
    cmdclass={
       'clean': clean,
       'build_py': build_py,
    },
    license=license
)

