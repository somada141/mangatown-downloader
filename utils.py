# -*- coding: utf-8 -*-

import zipfile
import cStringIO


class InMemoryZip(object):
    def __init__(self):
        # Create the in-memory file-like object
        self.in_memory_data = cStringIO.StringIO()
        # Create the in-memory zipfile
        self.in_memory_zip = zipfile.ZipFile(self.in_memory_data, "w", zipfile.ZIP_DEFLATED, False)
        self.in_memory_zip.debug = 3

    def append(self, filename_in_zip, file_contents):
        """Appends a file with name filename_in_zip and contents of file_contents to the in-memory zip"""
        self.in_memory_zip.writestr(filename_in_zip, file_contents)
        return self   # so you can daisy-chain

    def read(self):
        return self.in_memory_data.getvalue()
        
    def writetofile(self, filename):
        """Writes the in-memory zip to a file"""

        # Mark the files as having been created on Windows so that
        # Unix permissions are not inferred as 0000
        for zfile in self.in_memory_zip.filelist:
            zfile.create_system = 0
        self.in_memory_zip.close()
        with open(filename, 'wb') as f:
            f.write(self.in_memory_data.getvalue())
