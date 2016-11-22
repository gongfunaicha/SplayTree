''' Implementation of a splay tree node.  The data structure is a
    Python list that records the values stored at the node, including
    references to the two children and to the parent, but this list
    should be accessed only through the methods of this class.

    The methods that access left and right children have a parameter
    'reverse'.  A precondition is that 'reverse' is either 0 or 1.  If
    'reverse' is 1, then the roles of left and right child are reversed.
    For example, if v is a node, v.getLeft(0) gets its left child, but
    v.getLeft(1) gets its right child.  Similarly, v.setLeft(w,0) sets
    w to be its left child, but v.setLeft(w,1) sets it to be its right
    child, and v.getRight(1) returns the left child, etc.
'''


class pathNode:
   def __init__ (self, leftChild, key, rightChild, size, parent):
       self.values = [leftChild, rightChild, key, size, parent]

   # Get a label indicating size of the subtree rooted at the node
   def getSize(self):
       if self == None: return 0
       else:  return self.values[3]

   # Assign a label indicating the size of the subtree rooted at the node
   def setSize(self, size):
       self.values[3] = size

   # Get left child 
   def getLeft (self, reverse):
       return self.values[reverse]

   # Assign left child
   def setLeft (self, v, reverse):
       self.values[reverse] = v

   # Get the right child
   def getRight (self, reverse):
       return self.values[1 - reverse]

   # Assign the right child
   def setRight (self, v, reverse):
       self.values[1 - reverse] = v

   # get the parent
   def getParent(self):
      return self.values[4]

   # assign the parent
   def setParent(self, parent):
      self.values[4] = parent

   # get the Delta key stored at the node
   def getKey(self):
       return self.values[2]

   # assign the Delta key stored at the node
   def setKey(self, key):
       self.values[2] = key

