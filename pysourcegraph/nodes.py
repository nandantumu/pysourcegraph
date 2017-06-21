""" This class contains objects used to maintain the structure of the python source code."""
class BaseNode(object):
    """ This object is the base for all of the other, more sepecific node types"""
    def __init__(self, name, docstring=None):
        """Create new BaseNode object"""
        self._name = name
        self._docstring = docstring
        self._children = list()

    def add_child(self, childnode):
        """Add a child node to this node
        Args:
            childnode(BaseNode): Node to be added under this node
        """
        self._children.append(childnode)

    def remove_child(self, targetnode):
        """Remove a child node from this node
        This is an O(n)=n function
        Args:
            targetnode(BaseNode): Node to be removed from this node
        """
        try:
            self._children.remove()
        except ValueError:
            print("Failed to remove node" + targetnode)

    def __eq__(self, other):
        """Define custom Equals behavior"""
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return NotImplemented

    def __ne__(self, other):
        """Define custom NotEquals behavior"""
        if isinstance(other, self.__class__):
            return not self == other
        else:
            return NotImplemented

    def __repr__(self):
        """Define python representation of object"""
        return str(self.__class__) + str(self.__dict__)

    @DeprecationWarning
    def getlocalattr(self, attrname):
        """Return a function that returns the value of attrname in this class

        >>>self.x = 100
        >>>self.getlocalattr("x")()
        >>>100

        Args:
            attrname(str): String of the name of the variable
        """
        return lambda: getattr(self, attrname)

    @DeprecationWarning
    def setlocalattr(self, attrname):
        """Return a function that sets the value of attrname in this class

        >>>f = self.setlocalattr("x")
        >>>f(100)
        >>>self.x
        >>>100

        Args:
            attrname(str): String of the name of the variable
        """
        return lambda value: setattr(self, attrname, value)

    @DeprecationWarning
    def dellocalattr(self, attrname):
        """Return a function that deletes attrname from this class

        Args:
            attrname(str): String of the name of the variable
        """
        return lambda: delattr(self, attrname)

    @property
    def name(self):
        """The fully qualified name of the Node"""
        return self._name

    @property
    def docstring(self):
        """The DocString found documenting this Node"""
        return self._docstring