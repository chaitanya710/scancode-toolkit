#
# Copyright (c) nexB Inc. and others. All rights reserved.
# ScanCode is a trademark of nexB Inc.
# SPDX-License-Identifier: Apache-2.0
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/scancode-toolkit for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
#

import attr

from packagedcode import about
from packagedcode import bower
from packagedcode import build
from packagedcode import build_gradle
from packagedcode import cargo
from packagedcode import chef
from packagedcode import debian
from packagedcode import conda
from packagedcode import cocoapods
from packagedcode import cran
from packagedcode import freebsd
from packagedcode import golang
from packagedcode import haxe
from packagedcode import jar_manifest
from packagedcode import maven
from packagedcode import misc
from packagedcode import models
from packagedcode import msi
from packagedcode import npm
from packagedcode import nuget
from packagedcode import opam
from packagedcode import phpcomposer
from packagedcode import pubspec
from packagedcode import pypi
from packagedcode import readme
from packagedcode import rpm
from packagedcode import rubygems
from packagedcode import win_pe
from packagedcode import windows

# Note: the order matters: from the most to the least specific parser.
# a handler classes MUST be added to this list to be active
PACKAGE_DATAFILE_HANDLERS = [
#     rpm.RpmArchiveRecognizer,
#     debian.DebianPackageRecognizer,
#
#     jar_manifest.JavaJarManifestRecognizer,
#     jar_manifest.JavaJarRecognizer,
#     misc.JavaWarRecognizer,
#     misc.JavaWarWebXmlRecognizer,
#     maven.PomXml,
#     jar_manifest.IvyXmlRecognizer,
#     misc.JBossSarRecognizer,
#     misc.Axis2MarModuleXmlRecognizer,
#
     about.AboutFileHandler,
#     npm.PackageJson,
#     npm.PackageLockJson,
#     npm.YarnLockJson,
#     phpcomposer.ComposerJson,
#     phpcomposer.ComposerLock,
#     haxe.HaxelibJson,
    cargo.CargoTomlHandler,
    cargo.CargoLockHandler,
#     cocoapods.Podspec,
#     cocoapods.PodfileLock,
#     cocoapods.PodspecJson,
#     opam.OpamFile,
#     misc.MeteorPackage,
    bower.BowerJsonHandler,
#     freebsd.CompactManifest,
#     misc.CpanModule,
#     rubygems.GemArchive,
#     rubygems.GemArchiveExtracted,
#     rubygems.GemSpec,
#     rubygems.GemfileLock,
#     misc.AndroidApp,
#     misc.AndroidLibrary,
#     misc.MozillaExtension,
#     misc.ChromeExtension,
#     misc.IOSApp,
#     pypi.MetadataFile,
#     pypi.BinaryDistArchive,
#     pypi.SourceDistArchive,
#     pypi.SetupPy,
#     pypi.DependencyFile,
#     pypi.PipfileLock,
#     pypi.RequirementsFile,
#     golang.GoMod,
#     golang.GoSum,
#     misc.CabPackage,
#     misc.InstallShieldPackage,
#     misc.NSISInstallerPackage,
#     nuget.Nuspec,
#     misc.SharPackage,
#     misc.AppleDmgPackage,
#     misc.IsoImagePackage,
#     misc.SquashfsPackage,
#     chef.MetadataJson,
#     chef.Metadatarb,
#     build.BazelPackage,
#     build.BuckPackage,
#     build.AutotoolsPackage,
#     conda.Condayml,
#     win_pe.WindowsExecutable,
#     readme.ReadmeManifest,
#     build.MetadataBzl,
#     msi.MsiInstallerPackage,
#     windows.MicrosoftUpdateManifest,
#     pubspec.PubspecYaml,
#     pubspec.PubspecLock,
#     cran.DescriptionFile,
    build_gradle.BuildGradleHandler,
#     rpm.RpmSpecfileRecognizer,
]

HANDLER_BY_DATASOURCE_ID = {
    p.datasource_id for p in PACKAGE_DATAFILE_HANDLERS
}


class UnknownPackageDatasource(Exception):
    pass


def get_package_handler(package_data):
    """
    Return the DatafileHandler class that corresponds to a ``package_data``
    PackageData object. Raise a UnknownPackageDatasource error if the
    DatafileHandler is not found.
    """
    ppc = HANDLER_BY_DATASOURCE_ID.get(package_data.datasource_id)
    if not ppc:
        raise UnknownPackageDatasource(package_data)
    return ppc

