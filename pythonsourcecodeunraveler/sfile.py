# Copyright 2017 Renukanandan Tumu. All Rights Reserved
"""
Provides framework to access python program attributes


"""


class SFile(object):  # pylint: disable=R0903
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
        """ Returns the classes/modules imported in a list format """
        for line in self._filelines:
            pass

    def get_method_signatures(self):
        """ Returns the methods present in the module that do not belong to any classes

        Returns:
            list: List of lists where the first item in each list is a method name, 
                and the next is a list of arguments.
        """
        raise NotImplementedError
