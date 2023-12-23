import logging
 
module_logger = logging.getLogger("fatherModule.son")
class SonModuleClass2(object):
     def __init__(self):
         self.logger = logging.getLogger("fatherModule.son.module")
         self.logger.info("creating an instance in SonModuleClass2")
     def doSomething(self):
         self.logger.info("do something in SonModule2")
         a = []
         a.append(1)
         self.logger.debug("list a = " + str(a))
         self.logger.info("finish something in SonModuleClass2")
 
def som_function():
    module_logger.info("call function some_function2")