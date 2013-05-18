## tivo_flash_packager

Cross-platform (eventually) python script to package swfs from an unzipped AIR package 
into a .tivoipkg

### usage:

    [python] tivo-package.py extractedAirPkgDir targetFile
    
...where extractedAirPkgDir is where you unzipped your AIR package and targetFile is the full path (including filename) of where you want your tivoipkg.

### important, _very_ alpha: 

* Currently only handles "flash2" package type
* Multiple simultaneous invocations will mess stuff up
* Only tested lightly on Windows so far, doubt it works anywhere else yet

### requirements:

On Windows, requires Python 3 (tested with 3.3), CPIO, and Gzip in the path.

* http://gnuwin32.sourceforge.net/packages/cpio.htm
* http://gnuwin32.sourceforge.net/packages/gzip.htm


