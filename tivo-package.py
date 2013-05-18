import re, sys, subprocess, os, shutil
from os.path import join, relpath, abspath

inAppPath = sys.argv[1] 		# "bin"
inTargetFile = sys.argv[2]		# "localserver/app/testharness.tivoipkg"
tempDir = "tivo-package_temp"

if sys.platform == "win32":
	# Windows-specific code
	cmd_gzip = "gzip -c {0} > {1}"
	cmd_cpioBomPack = "cd {0} & type {1} | cpio -o -Hcrc --warning=truncate --quiet --force-local --file {2}"
else:
	# Non windows code
	cmd_gzip = "gzip < {0} > {1}"
	cmd_cpioBomPack = "cd {0}; cat {1} | cpio --force-local --warning=truncate --quiet -o -Hcrc -O {2}"

def main():
	shutil.rmtree( tempDir, True )
	os.mkdir( tempDir )

	tmpPkg = makeFlashPackage( tempDir )
	os.replace( tmpPkg, inTargetFile )
	shutil.rmtree( tempDir, True )

def makeFlashPackage( tempMakeDir ):

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

	packWithBOM( tempMakeDir, inAppPath, makeFileList( inAppPath ), "data.cpio" )
	gzip( join( tempMakeDir, "data.cpio" ), join( tempMakeDir, "data.cpio.gz" ) )

	files.append( "data.cpio.gz" )

	packWithBOM( tempMakeDir, tempMakeDir, files, "tmp-pkg.cpio" )
	finalGzPath = join( tempMakeDir, "tmp-pkg.cpio.gz" );
	gzip( join( tempMakeDir, "tmp-pkg.cpio" ), finalGzPath )
	return finalGzPath

def makeFileList( dirPath ):
	fileList = []
	for root, dirs, files in os.walk( dirPath ):
		if '.svn' in dirs:
			dirs.remove( '.svn' )
		fileList.extend( [ relpath( join( root, name ), dirPath ) for name in files ] )
	return fileList

def packWithBOM( workDir, sourceDir, fileList, cpioFileName ):
	bomPath = abspath( join( workDir, "bom" ) );
	out_file = open( bomPath, "wt" )
	out_file.writelines( [ name + "\n" for name in fileList ] )
	out_file.close()
	cmdStr = cmd_cpioBomPack.format( sourceDir, bomPath, abspath( join( workDir, cpioFileName ) ) ) 
	subprocess.call( cmdStr, shell=True )
	os.remove( bomPath );

def gzip( sourcePath, targetPath ):
	subprocess.call( cmd_gzip.format( sourcePath, targetPath ), shell=True )


if __name__ ==	'__main__':
	main()

