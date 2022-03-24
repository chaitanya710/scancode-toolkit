#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import logging
import os
import sys

import attr

from packagedcode.models import PackageData
from packagedcode.models import DatafileHandler
from commoncode import filetype
from typecode import contenttype
from commoncode.fileutils import as_posixpath

"""
Miscellaneous package data file formats.
"""

SCANCODE_DEBUG_PACKAGE_API = os.environ.get('SCANCODE_DEBUG_PACKAGE_API', False)

TRACE = False or SCANCODE_DEBUG_PACKAGE_API
TRACE_MERGING = False or SCANCODE_DEBUG_PACKAGE_API


def logger_debug(*args):
    pass


logger = logging.getLogger(__name__)

if TRACE or TRACE_MERGING:

    logging.basicConfig(stream=sys.stdout)
    logger.setLevel(logging.DEBUG)

    def logger_debug(*args):
        return logger.debug(' '.join(isinstance(a, str) and a or repr(a) for a in args))

    logger_debug = print

# Package types
# NOTE: this is somewhat redundant with extractcode archive handlers
# yet the purpose and semantics are rather different here



class ZipArchiveParser(DatafileHandler):

    @classmethod
    def is_datafile(cls, location):
        ipdf = super(ZipArchiveParser, cls).is_datafile(location)
        if ipdf:
            T = contenttype.get_type(location)
            return 'zip archive' in T.filetype_file.lower()



@attr.s()
class JavaWarPackageData(PackageData):
    default_type = 'war'
    default_primary_language = 'Java'


class JavaWarRecognizer(ZipArchiveParser):
    datatype = JavaWarPackageData
    path_patterns = ('*.war',)


class JavaWarWebXmlRecognizer(DatafileHandler):
    datatype = JavaWarPackageData
    path_patterns = ('*/WEB-INF/web.xml',)


@attr.s()
class JavaEarPackageData(PackageData):
    default_type = 'ear'
    default_primary_language = 'Java'


class JavaEarRecognizer(ZipArchiveParser):
    datatype = JavaEarPackageData
    path_patterns = ('*.ear')


class JavaEarAppXmlRecognizer(DatafileHandler):
    datatype = JavaEarPackageData
    path_patterns = ('*/meta-inf/application.xml', '*/meta-inf/ejb-jar.xml')


@attr.s()
class Axis2MarPackageData(PackageData):
    """Apache Axis2 module"""
    default_type = 'axis2'
    default_primary_language = 'Java'


class Axis2MarModuleXmlRecognizer(DatafileHandler):
    datatype = Axis2MarPackageData
    path_patterns = ('*/meta-inf/module.xml',)


class Axis2MarArchiveRecognizer(ZipArchiveParser):
    datatype = Axis2MarPackageData
    path_patterns = ('*.mar',)


@attr.s()
class JBossSarPackageData(PackageData):
    default_type = 'jboss'
    default_primary_language = 'Java'


class JBossSarRecognizer(ZipArchiveParser):
    datatype = JBossSarPackageData
    path_patterns = ('*.sar',)


class JBossServiceXmlRecognizer(DatafileHandler):
    datatype = JBossSarPackageData
    path_patterns = ('*/meta-inf/jboss-service.xml',)


@attr.s()
class MeteorPackageData(PackageData,):
    default_type = 'meteor'
    default_primary_language = 'JavaScript'


class MeteorPackageRecognizer(DatafileHandler):
    datatype = DatafileHandler
    path_patterns = ('*/package.js',)


@attr.s()
class CpanPackageData(PackageData):
    default_type = 'cpan'
    default_primary_language = 'Perl'


class CpanPodRecognizer(DatafileHandler):
    datatype = CpanPackageData
    path_patterns = (
        '*.pod',
        # TODO: .pm is not a package manifest
        '*.pm',
        '*/MANIFEST',
        '*/Makefile.PL',
        '*/META.yml',
        '*/META.json',
        '*.meta',
        '*/dist.ini',
    )


# TODO: refine me: Go packages are a mess but something is emerging
# TODO: move to and use godeps.py
@attr.s()
class GodepPackageData(PackageData):
    default_type = 'golang'
    default_primary_language = 'Go'


class Godep(PackageData):
    datatype = GodepPackageData
    path_patterns = ('*/Godeps',)


@attr.s()
class AndroidAppPackageData(PackageData):
    default_type = 'android'
    default_primary_language = 'Java'


class AndroidAppArchiveRecognizer(ZipArchiveParser):
    datatype = AndroidAppPackageData
    path_patterns = ('*.apk',)


# see http://tools.android.com/tech-docs/new-build-system/aar-formats
@attr.s()
class AndroidLibraryPackageData(PackageData):
    default_type = 'android-lib'
    default_primary_language = 'Java'


class AndroidLibraryRecognizer(ZipArchiveParser):
    datatype = AndroidLibraryPackageData

    # note: Apache Axis also uses AAR path_patterns for plain Jars.
    # this could be decided based on internal structure
    path_patterns = ('*.aar',)

@attr.s()
class MozillaExtensionPackageData(PackageData):
    default_type = 'mozilla'
    default_primary_language = 'JavaScript'


class MozillaExtensionRecognizer(ZipArchiveParser):
    datatype = MozillaExtensionPackageData
    path_patterns = ('*.xpi',)



@attr.s()
class ChromeExtensionPackageData(PackageData):
    default_type = 'chrome'
    default_primary_language = 'JavaScript'


class ChromeExtensionRecognizer(DatafileHandler):
    datatype = ChromeExtensionPackageData
    path_patterns = ('*.crx',)


@attr.s()
class IOSAppPackageData(PackageData):
    default_type = 'ios'
    default_primary_language = 'Objective-C'


@attr.s()
class IOSAppIpaRecognizer(DatafileHandler):
    datatype = IOSAppPackageData
    path_patterns = ('*.ipa',)


@attr.s()
class CabArchivePackageData(PackageData):
    default_type = 'cab'
    default_primary_language = 'C'


class CabArchiveRecognizer(DatafileHandler):
    datatype = CabArchivePackageData
    path_patterns = ('*.cab',)

    @classmethod
    def is_datafile(cls, location):
        ipdf = super(CabArchiveRecognizer, cls).is_datafile(location)
        if ipdf:
            T = contenttype.get_type(location)
            return 'microsoft cabinet' in T.filetype_file.lower()


@attr.s()
class InstallShieldPackageData(PackageData):
    default_type = 'installshield'


class InstallShieldPackageRecognizer(DatafileHandler):
    datatype = InstallShieldPackageData
    path_patterns = ('*.exe',)

    @classmethod
    def is_datafile(cls, location):
        ipdf = super(InstallShieldPackageRecognizer, cls).is_datafile(location)
        if ipdf:
            T = contenttype.get_type(location)
            return 'installshield' in T.filetype_file.lower()


@attr.s()
class NSISInstallerPackageData(PackageData):
    default_type = 'nsis'


class NSISInstallerRecognizer(DatafileHandler):
    datatype = NSISInstallerPackageData
    path_patterns = ('*.exe',)

    @classmethod
    def is_datafile(cls, location):
        ipdf = super(NSISInstallerRecognizer, cls).is_datafile(location)
        if ipdf:
            T = contenttype.get_type(location)
            return 'nullsoft installer' in T.filetype_file.lower()


@attr.s()
class SharPackagePackageData(PackageData):
    default_type = 'shar'


class SharArchiveRecognizer(DatafileHandler):
    datatype = SharPackagePackageData
    path_patterns = ('*.shar',)

    @classmethod
    def is_datafile(cls, location):
        ipdf = super(SharArchiveRecognizer, cls).is_datafile(location)
        if ipdf:
            T = contenttype.get_type(location)
            return 'posix shell script' in T.filetype_file.lower()


@attr.s()
class AppleDmgPackageData(PackageData):
    default_type = 'dmg'


class AppleDmgRecognizer(DatafileHandler):
    datatype = AppleDmgPackageData
    path_patterns = ('*.dmg', '*.sparseimage',)


@attr.s()
class IsoImagePackageData(PackageData):
    default_type = 'iso'


class IsoImageRecognizer(DatafileHandler):
    datatype = IsoImagePackageData
    path_patterns = ('*.iso', '*.udf', '*.img',)

    @classmethod
    def is_datafile(cls, location):
        ipdf = super(IsoImageRecognizer, cls).is_datafile(location)
        if ipdf:
            fts = contenttype.get_type(location).filetype_file.lower()
            filetypes = ('iso 9660 cd-rom', 'high sierra cd-rom',)
            return any(ft in fts for ft in filetypes)


@attr.s()
class SquashfsPackageData(PackageData):
    default_type = 'squashfs'


@attr.s()
class SquashfsPackageRecognizer(DatafileHandler):
    datatype = SquashfsPackageData

    @classmethod
    def is_datafile(cls, location):
        if filetype.is_file(location):
            T = contenttype.get_type(location)
            return 'squashfs' in T.filetype_file.lower()

# TODO: Add VM images formats(VMDK, OVA, OVF, VDI, etc) and Docker/other containers
