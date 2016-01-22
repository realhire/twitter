# -*- coding: utf-8 -*-
"""
This module will split the original 2.6GB file to 30 files. each containing one
day's data. This should produce 30 file with file size around 100MB, hopefully.

@author: realhire
"""

import os.path
import os

class fileSplitter:
    def __init__(self, infilePath, outfileDirectory, outfileFmt, outfileprefix=None):
        assert os.path.isfile(infilePath)
        self.infile = infilePath
        self.outdir = outfileDirectory
        self.outfileprefix = outfileprefix
        self.outFmt = outfileFmt

    def process(self):
        linenum = 0
        lastEntryDay = 0
        outfileName = None
        fout = None
        with open(self.infile, 'r') as f:
            while 1:
                oneline = f.readline()
                if not oneline:
                    break
                linenum += 1
                if len(oneline) is 0 or oneline[0] is not 'T':
                    continue
                tline = oneline
                uline = f.readline()
                wline = f.readline()
                day = tline.split()[1].split('-')[2]
                # Avoid open and close file all the time. that would be too time consuming
                if day != lastEntryDay:
                    lastEntryDay = day
                    outfileName = os.path.join(self.outdir, self.outfileprefix + day + '.' + self.outFmt)
                    if fout is not None:
                        fout.close()
                        print "close last file"
                    fout = open(outfileName, "a")
                    print "open file ", outfileName
                fout.write(tline)
                fout.write(uline)
                fout.write(wline + '\n')
        if fout is not None:
            fout.close()

fs = fileSplitter('tweets2009-06.txt', os.getcwd(), 'txt', 'tc')
fs.process()