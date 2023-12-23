import logging
 
module_logger = logging.getLogger("fatherModule.son")
class SonModuleClass1(object):
     def __init__(self):
         self.logger = logging.getLogger("fatherModule.son.module")
         self.logger.info("creating an instance in SonModuleClass")
     def doSomething(self):
         self.logger.info("do something in SonModule")
         a = []
         a.append(1)
         self.logger.debug("list a = " + str(a))
         self.logger.info("finish something in SonModuleClass")
 
def som_function():
    module_logger.info("call function some_function")