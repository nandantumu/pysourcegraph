""" This module provides parsers for given files."""
import ast

def import_lister(pyfile):
    """Outputs a list of all classes imported in this python file

    Args:
        pyfile (file): python source code file

    Returns:
        list: List of classes imported in this file, with no leading dots. Random text to exceed
        If nothing is imported, then an empty list will be returned.
    """
    tree = ast.parse(pyfile.read())
    pyfile.close()
    retlist = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            # This returns a list of alias nodes
            for aliasnode in node.names:
                retlist.append(aliasnode.name)
        elif isinstance(node, ast.ImportFrom):
            modname = ''
            if node.level > 0:
                modname = node.module
            for aliasnode in node.names:
                retlist.append(str(modname)+str(aliasnode.name))
    return retlist

def class_lister(pyfile):
    """Outputs a list of all classes in this python file

    Args:
        pyfile (file): python source code file

    Returns:
        list: List of class names in this file.
        If no classes are present, then an empty list will be returned.
    """
    tree = ast.parse(pyfile.read())
    pyfile.close()
    retlist = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            retlist.append(node.name)
    return retlist
