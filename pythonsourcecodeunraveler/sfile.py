# Copyright 2017 Renukanandan Tumu. All Rights Reserved
"""
Provides framework to access python program attributes


"""


class SFile(object):
    """
    This class extracts classes, methods, and function signatures
    from a .py file

    Attributes:
        _filelines(list): This is a list of strings, where each
            item is a line of the source file
    """
    def __init__(self, filepath):
        """This initializes an SCFile object

        Args:
            filepath (str): Absolute or relative filepath of the python file
                to be analyzed

        """
        pyfile = open(filepath, 'r')
        self._filelines = pyfile.readlines()
        pyfile.close()
        del pyfile

    def get_imports(self):
        """ Get classes/modules imported in this module

        Returns:
            list: Classes/modules imported by this module

        Raises:
            SyntaxError:
        """
        retlist = []
        for line in self._filelines:
            linearray = line.split()
            if 'import' in linearray and 'from' in linearray:
                try:
                    retlist.append(linearray[linearray.index('from') + 1] +
                                   "." +
                                   linearray[linearray.index('import')+1])
                except IndexError:
                    raise SyntaxError("The file selected has \
invalid import statements.")
            elif 'import' in linearray:
                try:
                    retlist.append(linearray[linearray.index('import')])
                except IndexError:
                    raise SyntaxError("The file selected has \
invalid import statements.")
            del linearray
        return retlist
        # TODO check if the import statement is inside a string literal

    def get_method_signatures(self):
        """ Returns the methods present in the module that do not belong to any classes

        Returns:
            list: List of lists where the first item in each
            list is a method name, and the next is a list of arguments.
        """
        raise NotImplementedError
