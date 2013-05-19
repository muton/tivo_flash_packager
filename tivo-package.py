#!/usr/bin/env python3
import sys, subprocess, gzip, os, shutil, zipfile
from os.path import join, relpath, abspath

inAppPath = sys.argv[1] 		# "air/myapp.air"
inTargetFile = sys.argv[2]		# "localserver/app/testharness.tivoipkg"
tempDir = "tivo-package_temp"

if sys.platform == "win32":
	# Windows-specific code
	cmd_cpioBomPack = "cd {0} & type {1} | cpio --force-local --warning=truncate --quiet -o -Hcrc --file {2}"
else:
	# Non windows code
	cmd_cpioBomPack = "cd {0}; cat {1} | cpio --force-local --warning=truncate --quiet -o -Hcrc -O {2}"

def main():
	# set up temp dir, clean out if present for previous failure
	shutil.rmtree( tempDir, True )
	os.mkdir( tempDir )
	
	# extract AIR package
	airDir = join( tempDir, "air-extract" )
	os.mkdir( airDir )
	extractAir( inAppPath, airDir )
	
	# create TiVo package
	tivoDir = join( tempDir, "tivo-build" )
	os.mkdir( tivoDir )
	tmpPkg = makeFlashPackage( airDir, tivoDir )
	
	# move TiVo package to desired location and clean up
	os.replace( tmpPkg, inTargetFile )
	shutil.rmtree( tempDir, True )

	
def extractAir( airPath, tempAirDir ):
	"""Unzip AIR package into specified dir"""
	
	with zipfile.ZipFile( airPath, 'r' ) as airZip:
		# file "hash" seems to always get a bad CRC, hopefully ignoring it won't be a problem
		airZip.extractall( tempAirDir, filter( 
			lambda f: f != "META-INF/AIR/hash" and not f.endswith('/'), airZip.namelist() ) )
		airZip.close()
		
def makeFlashPackage( airDir, tempMakeDir ):
	"""Create a .tivopkg from a decompressed AIR package"""
	
	files = []
	pkgType = "flash2"

	# create manifest
	manifestFileName = "manifest.txt"
	out_file = open( join( tempMakeDir, manifestFileName ), "wt" )
	out_file.writelines( [ 
		"Type: " + pkgType,
		"\nX-Format: cpio-gz",
		"\nX-File: data.cpio.gz"] )
	out_file.close();

	files.append( manifestFileName )

	packWithBOM( tempMakeDir, airDir, makeFileList( airDir ), "data.cpio" )
	compressWithGZip( join( tempMakeDir, "data.cpio" ), join( tempMakeDir, "data.cpio.gz" ) )
	files.append( "data.cpio.gz" )

	packWithBOM( tempMakeDir, tempMakeDir, files, "tmp-pkg.cpio" )
	finalGzPath = join( tempMakeDir, "tmp-pkg.cpio.gz" );
	compressWithGZip( join( tempMakeDir, "tmp-pkg.cpio" ), finalGzPath )
	return finalGzPath

def makeFileList( dirPath ):
	"""Returns a list of files in the specified directory, with paths relative to it"""
	
	fileList = []
	for root, dirs, files in os.walk( dirPath ):
		if '.svn' in dirs:
			dirs.remove( '.svn' )
		fileList.extend( [ relpath( join( root, name ), dirPath ) for name in files ] )
	return fileList

def packWithBOM( workDir, sourceDir, fileList, cpioFileName ):
	"""Packs files using the external CPIO tool and a BOM (Bill Of Materials? Maybe; that's what TiVo's Perl script calls it"""
	
	bomPath = abspath( join( workDir, "bom" ) );
	out_file = open( bomPath, "wt" )
	out_file.writelines( [ name + "\n" for name in fileList ] )
	out_file.close()
	cmdStr = cmd_cpioBomPack.format( sourceDir, bomPath, abspath( join( workDir, cpioFileName ) ) ) 
	subprocess.call( cmdStr, shell=True )
	os.remove( bomPath );

def compressWithGZip( sourcePath, targetPath ):
	with open( sourcePath, 'rb' ) as f_in:
		with gzip.open( targetPath, 'wb' ) as f_out:
			f_out.writelines( f_in )

if __name__ ==	'__main__':
	main()

