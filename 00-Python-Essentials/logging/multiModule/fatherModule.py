import logger
import sonModule1
import sonModule2

mylogger = logger.Loggers()
# mylogger.logger.info("creating an instance of sonModule.sonModuleClass")
a = sonModule1.SonModuleClass1()
# mylogger.logger.info("calling sonModule.sonModuleClass.doSomething")
a.doSomething()
# mylogger.logger.info("done with  sonModule.sonModuleClass.doSomething")
# mylogger.logger.info("calling sonModule.some_function")
sonModule1.som_function()
# mylogger.logger.info("done with sonModule.some_function")

# mylogger.logger.info("creating an instance of sonModule.sonModuleClass2")
a = sonModule2.SonModuleClass2()
# mylogger.logger.info("calling sonModule.sonModuleClass2.doSomething")
a.doSomething()
# mylogger.logger.info("done with  sonModule.sonModuleClass2.doSomething")
# mylogger.logger.info("calling sonModule.some_function2")
sonModule2.som_function()
# mylogger.logger.info("done with sonModule.some_function2")