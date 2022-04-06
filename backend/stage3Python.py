import os
import multiprocessing
from multiprocessing import Pool
import subprocess
import shutil

STATUS_CODE_ERROR_CANT_PROCESS = 106
CODE_DESCEIOTION_ERROR_CANT_PROCESS = "This source code can't process"
STATUS_CODE_ERROR_TIMEOUT = 107
CODE_DESCEIOTION_ERROR_TIMEOUT = "This process timeout"

class compilePython:

    def __init__(self, dictdata, PATH_MAIN, queueFolder):
        self.queueFolder = queueFolder
        self.dictdata = dictdata
        self.filename = dictdata['data']['filename']
        self.pathFile = dictdata['data']['pathFile']
        self.pathIn = dictdata['data']['pathIn']
        self.pathOut = dictdata['data']['pathOut']
        self.process = False
        self.firstprocess = True
        self.PATH_OUTPUT = os.path.join(PATH_MAIN, 'store_output', queueFolder)
        self.fStage4 = {}
        os.makedirs(self.PATH_OUTPUT, exist_ok=True)

    def runWork(self):
        os.chdir(self.pathFile)
        for name_file in os.listdir(self.pathIn):
            path_file = os.path.join(self.pathIn, name_file)
            if not self.process and self.firstprocess:
                try:
                    subprocess.run(f"python {self.filename} < {path_file} > {os.path.join(self.PATH_OUTPUT, name_file)}", shell=True, check=True)
                    self.process = True
                except subprocess.CalledProcessError:
                    self.firstprocess = False
                    self.dictdata['status']['boolean'] = False
                    self.dictdata['status']['code'] = STATUS_CODE_ERROR_CANT_PROCESS
                    self.dictdata['status']['description'] = CODE_DESCEIOTION_ERROR_CANT_PROCESS
                    self.dictdata['status']['file'] = name_file
            if self.process:
                with Pool(processes=2) as pool:
                    try:
                        result = pool.apply_async(self.runprocess, (self.filename, path_file, name_file))
                        result.get(timeout=3)
                        self.fStage4 = {"PATH_OUTPUT": self.PATH_OUTPUT,
                                        "path_assignment": self.pathOut,
                                        "format": self.dictdata['data']['format'],
                                        "queueFolder": self.queueFolder,
                                        }
                        pool.close()
                        pool.terminate()
                        pool.join()
                    except multiprocessing.context.TimeoutError:
                        self.dictdata['status']['boolean'] = False
                        self.dictdata['status']['code'] = STATUS_CODE_ERROR_TIMEOUT
                        self.dictdata['status']['description'] = CODE_DESCEIOTION_ERROR_TIMEOUT
                        pool.close()
                        pool.terminate()
                        pool.join()
        if not os.listdir(self.pathOut):
            for item in os.listdir(self.PATH_OUTPUT):
                shutil.copy(os.path.join(self.PATH_OUTPUT, item), self.pathOut)
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def getWork(self):
        return self.dictdata, self.fStage4

    def runprocess(self, filename, path_file, name_file):
            subprocess.run(f"python {filename} < {path_file} > {os.path.join(self.PATH_OUTPUT, name_file)}", shell=True, check=True)