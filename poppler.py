# -*- coding: utf-8 -*-
import subprocess
from pathlib import Path
from PyQt5 import QtWidgets, QtCore, QtGui

class Poppler():
    def __init__(self):
        self.pdftocairo_path = Path('bin/poppler/bin/pdftocairo.exe')
        self.pdfinfo_path = Path('bin/poppler/bin/pdfinfo.exe')
        self.pdfunite_path = Path('bin/poppler/bin/pdfunite.exe')
        
    def pdfunite(self, pdf_paths, output_path):
        cmd = [ str(self.pdfunite_path) ]
        cmd.extend( [str(p) for p in pdf_paths] )
        cmd.append( str(output_path) )
        stdout, stderr = self.subprocess_popen(cmd)
        return stdout, stderr

    def pdftocairo(self, pdf_path, output_path, resolution, args=[]):
        '''
        return image path (type pathlib Path)
        '''

        # suffix option
        suffix_option = '-' + output_path.suffix.replace('.','')
        if suffix_option == '-jpg':
            suffix_option = '-jpeg'
        
        # output path
        if suffix_option == '-svg':
            output2 = output_path
            output_path2 = output_path
        else:
            output2 = output_path.parent / output_path.stem
            output_path2 = output_path.parent / (output_path.stem + '-1' + output_path.suffix)
        
        # create command
        cmd = [str(self.pdftocairo_path), suffix_option, '-r', str(resolution), str(pdf_path), str(output2)]
        cmd.extend(args)

        stdout, stderr = self.subprocess_popen(cmd)
        if stderr:
            print(stderr)
            return stdout, stderr
        
        return output_path2

    def pdfinfo(self, pdf_path):
        '''
        return dictionary from pdf info
        '''
        cmd = [ str(self.pdfinfo_path), str(pdf_path) ]
        stdout, stderr = self.subprocess_popen(cmd)
        if not stderr == '':
            return stdout, stderr
        lines = [ line.split(':') for line in stdout.splitlines() ]
        dict_ = { line[0].strip() : line[1].strip() for line in lines }
        s = dict_['Page size'].split()
        dict2 = { 'Name':str(pdf_path.name), 'Path':pdf_path, 'height':s[0], 'width':s[2] }
        dict_.update(dict2)
        return dict_

    def subprocess_popen(self, cmd):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        proc = subprocess.Popen(
            cmd, encoding='cp932', stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, startupinfo=startupinfo
        )
        stdout, stderr = proc.communicate(timeout=1000)
        return stdout, stderr
