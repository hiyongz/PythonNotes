#!/usr/bin/python3
# -*-coding:utf-8-*-
# @Time:    2021/11/20 21:32
# @Author:  hiyongz
# @File:    python_reflection4.py

class Demo():
    def __init__(self):
        self.person = Person()

    def get_function_arguments(self, name, *args, **kwargs):
        func = getattr(self.person, name)
        fmtLine = self._FormatArgs(func, *args, **kwargs)
        func(*args, **kwargs)
        print(fmtLine)

    def _FormatASCII(self, pyObj) :
        """
        Format the given pyObj as an ASCII string.  This is first attempted by doing str(pyObj).
        If that fails then if pyObj is a Unicode string it replaces each non-ASCII character with its
        repr encoding.  For any other pyObj it simply returns the complete repr encoding of pyObj.
        source：~\Lib\site-packages\AutoItLibrary\Logger.py
        """
        try :
            aString = str(pyObj)
        except UnicodeEncodeError :
            if isinstance(pyObj, type(u'')) :
                aString = ""
                for c in pyObj :
                    if ord(c) > 128 :
                        aString += repr(c)[2:-1]
                    else :
                        aString += c
            else :
                aString = repr(pyObj)
        finally :
            return aString


    def _FormatArg(self, fmtLine, argName, argVal) :
        """
        Format the given argName and argVal and add them to the current given fmtLine.
        If fmtLine is non-empty then ", " is appended to it before appending the formatted argName=argVal.
        """
        if len(fmtLine) > 0 :
            fmtLine += ", "

        if isinstance(argVal, type(1)) :
            fmtLine += "%s=%d" % (argName, argVal)

        elif isinstance(argVal, type(1.1)) :
            fmtLine += "%s=%g" % (argName, argVal)

        else :
            fmtLine += "%s='%s'" % (argName, self._FormatASCII(argVal))

        return fmtLine


    def _FormatArgs(self, func, *args, **kwargs) :
        """
        Format an arbitrary list of args and kwargs for function func for printing in a log line.
        TBD: Add any defaulted args not present in args or kwargs
        """
        fmtLine = ""
        funcArgs = None
        #
        # If we got some positional args then format those, adding the
        # argument name from the tuple of co_varnames obtained above.
        #
        if len(args) > 0 :
            funcArgs = func.__code__.co_varnames
            #
            # If func is a method of a class then it will have "self" as the first argument.
            # We don't want to print that, and it won't be in args or kwargs anyway, so remove it.
            #
            if funcArgs[0] == "self" :
                funcArgs = funcArgs[1:]
            ai = 0
            for arg in args :
                fmtLine = self._FormatArg(fmtLine, funcArgs[ai], arg)
                ai += 1
        #
        # If we got some kwargs, then format those.
        #
        if len(kwargs.keys()) > 0 :
            if funcArgs == None :
                funcArgs = func.__code__.co_varnames
                #
                # If func is a method of a class then it will have "self" as the first argument.
                # We don't want to print that, and it won't be in args or kwargs anyway, so remove it.
                #
                if funcArgs[0] == "self" :
                    funcArgs = funcArgs[1:]
                ai = 0

            for i in range(ai, len(funcArgs)) :
                key = funcArgs[i]
                if key not in kwargs.keys() :
                    continue
                fmtLine = self._FormatArg(fmtLine, key, kwargs[key])
                del kwargs[key]
        #
        # TBD: Add any defaulted args not present in args or kwargs
        #
        #
        # Add any additional args passed but not explicitly expected
        #
        if len(kwargs.keys()) > 0 :
            for key in kwargs :
                fmtLine = self._FormatArg(fmtLine, key, kwargs[key])

        return fmtLine

class Person():
    def talk(self, name, age, height=None):
        """talk function
        :return:
        """
        print(f"My name is {name}")
        print(f"My age is {age}")
        if height is not None:
            print(f"My height is {height}")

if __name__ == '__main__':
    demo = Demo()
    demo.get_function_arguments("talk","zhangsan", 18, height=2)