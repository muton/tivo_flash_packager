## tivo_flash_packager

Cross-platform (eventually) python script to repackage an AIR package into a .tivoipkg

### usage:

    [python] tivo-package.py airFile targetFile
    
...where airFile is the path to your packaged .air archive and targetFile is the full path (including filename) of where you want your tivoipkg.

### important, _very_ alpha: 

* Currently only handles "flash2" package type
* Multiple simultaneous invocations will mess stuff up
* Only tested lightly on Windows so far, doubt it works anywhere else yet

### requirements:

On Windows, requires Python 3 (tested with 3.3), CPIO, and Gzip in the path.

* http://gnuwin32.sourceforge.net/packages/cpio.htm
* http://gnuwin32.sourceforge.net/packages/gzip.htm


