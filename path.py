from pathNode import pathNode

reverse = 0


class path:
    #  Create an empty list
    def __init__(self):
        self.n = 0
        self.root = None
        reverse = 0

    # Get current number of elements in the list
    def getSize(self):
        if self.root == None:
            return 0
        else:
            return self.root.getSize()

    # To see how this works run ipython -i on this file, then try
    #  print p and p.tree() ...  It displays the tree with the root to the
    #  left and leaves to the right.  The printout at each node gives
    #  the key stored at the node, the label indicating the size of the
    #  subtree rooted at the node, and the key of the parent.  I've provided
    #  this to help you with debugging.  Study the code and make sure you
    #  understand how it works.
    def tree(self):
        self.treeAux(self.root, 0)

    def treeAux(self, v, indent):
        if v == None:
            print ' ' * 3 * indent + '*'
        else:
            if v.getParent() == None:
                parentKey = ''
            else:
                parentKey = v.getParent().getKey()
            if v.getRight(reverse) != None:
                self.treeAux(v.getRight(reverse), indent + 1)
            print ' ' * 3 * indent + str(v.getKey()) + ':' + str(v.getSize()) + ':' + str(parentKey)
            if v.getLeft(reverse) != None:
                self.treeAux(v.getLeft(reverse), indent + 1)

    # toString-type method that is invoked when you print the list.
    # Study the code.  It has an O(n) time bound because each element
    # is appended only once, and and Python uses the trick of doubling
    # the size of the array each time it gets full.  Understand why
    # it would be a mistake to refrain from passing in a string to
    # strAux, and instead concatenate the string returned by the left
    # recursive call, the string representing the key at v, and the string
    # returned by the right recursive call.
    def __str__(self):
        return self.strAux(self.root, '')

    def strAux(self, v, string):
        if v == None:
            return string
        else:
            string = self.strAux(v.getLeft(reverse), string)
            string = string + str(v.getKey()) + ' '
            string = self.strAux(v.getRight(reverse), string)
        return string

    ''' Inserts key to a given position in the list, without splaying.  It adds
        it at a leaf without splaying.  Use this is a model for one you will
        have to write that has to splay it once it is added.

        If position is larger than the length, it inserts the element at the
        end, and if it's smaller than 1, it inserts it at position 1.
        There can be no 'array out of bounds' error.  Keep to this
        convention in writing your other methods.
    '''

    def naiveInsert(self, key, position):
        self.n = self.n + 1
        if self.n == 1:
            self.root = pathNode(None, key, None, 1, None)
        else:
            self.naiveInsertAux(self.root, key, position)

    def naiveInsertAux(self, v, key, position):
        v.setSize(v.getSize() + 1)
        leftSize = self.getNodeSize(v.getLeft(reverse))

        if leftSize == 0 and position <= 1:
            v.setLeft(pathNode(None, key, None, 1, v), reverse)  # insert leaf

        # Note resemblance of the strategy to that of 'RandomizedSelect':
        elif position <= leftSize + 1:  # if position is in left subtree
            self.naiveInsertAux(v.getLeft(reverse), key, position)
        elif self.getNodeSize(v.getRight(reverse)) == 0 and position > leftSize + 1:
            v.setRight(pathNode(None, key, None, 1, v), reverse)
        else:
            self.naiveInsertAux(v.getRight(reverse), key, position - (leftSize + 1))

    ''' Return a reference to the pathNode at given position in the list.
        Don't splay it, since you can call a separate splay method on this
        reference, once it is returned.
    '''

    def findNode(self, position):
        if self.getSize() == 0:
            return None
        else:
            if position < 1:
                position = 1
            elif position > self.getSize():
                position = self.getSize()
            return self.findNodeAux(self.root, position)

    def findNodeAux(self, v, position):
        leftSize = self.getNodeSize(v.getLeft(reverse))

        if (leftSize >= position):
            return self.findNodeAux(v.getLeft(reverse), position)
        if ((leftSize + 1) == position):
            return v
        return self.findNodeAux(v.getRight(reverse), position - 1 - leftSize)

    '''  Perform a single rotation.  You must modify this operation so that
         it correctly updates the size labels in the nodes
    '''

    def rotate(self, parent, child):
        grandparent = parent.getParent()
        child.setParent(grandparent)
        if grandparent == None:
            self.root = child
        else:
            if grandparent.getLeft(reverse) == parent:
                grandparent.setLeft(child, reverse)
            else:
                grandparent.setRight(child, reverse)

        # Having the reverse parameter allows me to avoid repeating code
        #  for the two mirror-image operations
        if child == parent.getLeft(0):
            rev = 0
        else:
            rev = 1
        A = child.getLeft(rev)
        B = child.getRight(rev)
        C = parent.getRight(rev)
        if B != None: B.setParent(parent)
        parent.setLeft(B, rev)
        parent.setParent(child)
        child.setRight(parent, rev)

        # Change the size label of child and parent
        ASize = 0
        if (A != None):
            ASize = A.getSize()
        BSize = 0
        if (B != None):
            BSize = B.getSize()
        CSize = 0
        if (C != None):
            CSize = C.getSize()
        parent.setSize(BSize + CSize + 1)
        child.setSize(ASize + parent.getSize() + 1)

    ''' Splay x.  Write this method.  As a warmup, consider writing a fake
        splay that gets x to the root using ordinary rotations, rather than
        the double rotations described in the Tarjan book.  This won't give
        the O(log n) amortized bound, but it will let you work on other
        methods, then come back to it to turn it into the splay
        operation that gives the bound.   '''

    def splay(self, x):
        # No Parent
        if (x == self.root):
            return

        # No Grandparent
        if (x.getParent() == self.root):
            self.rotate(x.getParent(), x)
            return

        # Get grandparent and parent
        parent = x.getParent()
        grandparent = parent.getParent()

        xisleftchild = False
        parentisleftchild = False

        if (parent.getLeft(reverse) == x):
            xisleftchild = True

        if (grandparent.getLeft(reverse) == parent):
            parentisleftchild = True

        # All left child or all right child
        if (xisleftchild == parentisleftchild):
            # rotate at grandparent
            self.rotate(grandparent, parent)
            # rotate at parent
            self.rotate(parent, x)

        else:
            # rotate at parent
            self.rotate(parent, x)
            # rotate at new parent
            self.rotate(grandparent, x)

        # continue splaying at x
        self.splay(x)
        return

    ''' if position is larger than the length, it inserts the element at the
        end, and if it's smaller than 1, it inserts it at position 1.
        Otherwise, it inserts it at the given position in the list.
        This splays the inserted element.  Do not change any of the code in
        this method; using naiveInsertAux as a model, write insertAux
        so that it splays the node once it inserts it.  '''

    def insert(self, position, key):
        self.n = self.n + 1
        if self.n == 1:
            self.root = [None, key, None, 1, None]
        else:
            self.insertAux(self.root, key, position)

    # insert key at given position in subtree rooted at v, then splay
    def insertAux(self, v, key, position):
        pass  #

    # return the value at the given position
    def get(self, position):
        return 0  # replace this

    def assign(self, position, key):
        pass  # replace this

    def delete(self, position):
        pass  # replace this

    def split(self, position):
        pass  # replace this

    def append(self, p2):
        pass  # replace this

    def getNodeSize(self, v):
        if v == None:
            return 0
        else:
            return v.getSize()


if __name__ == '__main__':
    # p = path()
    # p.naiveInsert(10, 1)
    # p.naiveInsert(7, 1)
    # p.naiveInsert(3, 1)
    # p.naiveInsert(15, 4)
    # p.naiveInsert(105, 5)
    # p.naiveInsert(103, 5)
    # p.naiveInsert(107, 7)
    # p.naiveInsert(4, 2)
    # p.naiveInsert(8, 4)
    # p.naiveInsert(2, 1)
    # p.naiveInsert(12, 7)

    # Check splay on Fig 4.10
    p2 = path()
    p2.naiveInsert(9,1)
    p2.naiveInsert(20, 2)
    p2.naiveInsert(8, 1)
    p2.naiveInsert(19, 2)
    p2.naiveInsert(7, 1)
    p2.naiveInsert(18, 2)
    p2.naiveInsert(6, 1)
    p2.naiveInsert(11, 1)
    p2.naiveInsert(5, 3)
    p2.naiveInsert(17, 4)
    p2.naiveInsert(4, 3)
    p2.naiveInsert(12, 3)
    p2.naiveInsert(3, 5)
    p2.naiveInsert(13, 5)
    p2.naiveInsert(2, 7)
    p2.naiveInsert(14, 7)
    p2.naiveInsert(1, 9)
    p2.naiveInsert(15, 9)
    p2.naiveInsert(16, 11)
