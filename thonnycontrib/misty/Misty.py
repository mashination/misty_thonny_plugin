
import os
import sys
from PyInterpreter import PyInterpreter
from translate import tr


class Misty:
    TEXT_COLORS_BY_MODE = {
        'run': '\u001b[32m'
        , 'error': '\033[91m'
        , 'normal': '\033[95m'
        , 'warning': '\033[93m'
        , 'info' : '\033[94m'    }
    def __init__(self, filename):
        self.mode = "student"
        self.filename = filename
        

        
    def run(self):
        interp = PyInterpreter(None,self.mode,self.filename)
        ok, report = interp.execute()
        if report.has_compilation_error() or report.has_execution_error():
            ok = False
        self.write_report(ok, report,"exec")


    def write(self, s, tags=()):
        os.system('color')
        
        if len(tags)>0 and tags in self.TEXT_COLORS_BY_MODE: 
            print(self.TEXT_COLORS_BY_MODE[tags] + s + '\033[0m')
        else:
            print(s)

    def write_report(self, status, report, exec_mode):
            tag = 'run'
            if not status:
                tag = 'error'
                
            

            self.write(report.header, tags=(tag))
            #self.write("\n")
            
            has_convention_error = False
            
            for error in report.convention_errors:
                if error.severity == "error" and not has_convention_error:
                    self.write(tr("-----\nPython101 convention errors:\n-----\n"), tags='info')
                    has_convention_error = True

                
                #print("hyper={}".format(hyper))
                #print("hyper_spec={}".format(hyper_spec))
                self.write("\n")
                self.write(str(error), tags=(error.severity))
                self.write("\n")

            if not status:
                has_compilation_error = False
                for error in report.compilation_errors:
                    if error.severity == "error" and not has_compilation_error:
                        self.write(tr("\n-----\nCompilation errors (Python interpreter):\n-----\n"), tags='info')
                        has_compilation_error = True
                    
                    self.write("\n")
                    self.write(str(error), tags=(error.severity))
                    self.write("\n")


                has_execution_error = False
                for error in report.execution_errors:
                    if error.severity == "error" and not has_execution_error:
                        self.write(tr("\n-----\nExecution errors (Python interpreter):\n-----\n"), tags='info')
                        has_execution_error = True
                        
                   
                    self.write("\n")
                    self.write(str(error), tags=(error.severity))
                    self.write("\n")

            else:
                has_execution_error = False
                for error in report.execution_errors:
                    if error.severity == "error" and not has_execution_error:
                        self.write(tr("\n-----\nExecution errors (Python interpreter):\n-----\n"), tags='info')
                        has_execution_error = True

                   
                    self.write("\n")
                    self.write(str(error), tags=(error.severity))
                    self.write("\n")


                self.write(str(report.output), tags=('stdout'))
                if report.result is not None:
                    self.write(repr(report.result), tags=('normal'))

            if exec_mode == 'exec' and status and self.mode == tr('student') and report.nb_defined_funs > 0:
                if report.nb_passed_tests > 1:
                    self.write("==> " + tr("All the {} tests passed with success").format(report.nb_passed_tests), tags=('run'))
                elif report.nb_passed_tests == 1:
                    self.write("==> " + tr("Only one (successful) test found, it's probably not enough"), tags=('warning'))
                else:
                    self.write("==> " + tr("There is no test! you have to write tests!"), tags=('error'))
            
            self.write(report.footer, tags=(tag))


if __name__ == "__main__":
    filename = sys.argv[1]
    m=Misty(filename)
    m.run()
    