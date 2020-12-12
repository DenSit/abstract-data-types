class TreeNode:
    def __init__(self, val, left=None, right=None, parent=None):
        self.payload = val
        self.leftChild = left
        self.rightChild = right
        self.parent = parent
        self.balanceFactor = 0
        self.weight = val

    def hasLeftChild(self):
        return self.leftChild

    def hasRightChild(self):
        return self.rightChild

    def isLeftChild(self):
        return self.parent and self.parent.leftChild == self

    def isRightChild(self):
        return self.parent and self.parent.rightChild == self

    def isRoot(self):
        return not self.parent

    def isLeaf(self):
        return not (self.rightChild or self.leftChild)

    def hasBothChildren(self):
        return self.rightChild and self.leftChild

    def hasAnyChildren(self):
        return self.rightChild or self.leftChild

    def replaceNodeData(self, value, lc, rc):
        self.payload = value
        self.leftChild = lc
        self.rightChild = rc
        if self.hasLeftChild():
            self.leftChild.parent = self
        if self.hasRightChild():
            self.rightChild.parent = self

    def findSuccessor(self):
        succ = None
        if self.rightChild:
            succ = self.rightChild.findMin()
        else:
            if self.parent:
                if self.isLeftChild():
                    succ = self.parent
                else:
                    self.parent.rightChild = None
                    succ = self.parent.findSuccessor()
                    self.parent.rightChild = self
        return succ

    def spliceOut(self):
        if self.isLeaf():
            if self.isLeftChild():
                self.parent.leftChild = None
                self.parent.balanceFactor -= 1
            else:
                self.parent.rightChild = None
                self.parent.balanceFactor += 1
        elif self.hasAnyChildren():
            if self.isLeftChild():
                self.parent.leftChild = self.rightChild
                self.parent.balanceFactor -= 1
            else:
                self.parent.rightChild = self.rightChild
                self.parent.balanceFactor += 1
            self.rightChild.parent = self.parent

    def findMin(self):
        current = self
        while current.leftChild:
            current = current.leftChild
        return current


class MyTree:
    def __init__(self):
        self.root = None
        self.size = 0
        self.sum = 0

    def put(self, val):
        val = (self.sum + val) % 1000000001
        if self.root:
            self._put(val, self.root)
        else:
            self.root = TreeNode(val)
            self.size += 1

    def _put(self, val, current_node):
        if val < current_node.payload:
            if current_node.leftChild:
                self._put(val, current_node.leftChild)
            else:
                current_node.leftChild = TreeNode(val, parent=current_node)
                self.size += 1
                self.updateWeight(current_node.leftChild)
                self.updateBalance(current_node.leftChild)
        elif val > current_node.payload:
            if current_node.rightChild:
                self._put(val, current_node.rightChild)
            else:
                current_node.rightChild = TreeNode(val, parent=current_node)
                self.size += 1
                self.updateWeight(current_node.rightChild)
                self.updateBalance(current_node.rightChild)
        else:
            pass

    def updateWeight(self, node):
        weight = node.weight
        while node.parent:
            node.parent.weight += weight
            node = node.parent

    def updateBalance(self, node):
        if node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            return
        if node.parent is not None:
            if node.isLeftChild():
                node.parent.balanceFactor += 1
            elif node.isRightChild():
                node.parent.balanceFactor -= 1
            if node.parent.balanceFactor != 0:
                self.updateBalance(node.parent)

    def rebalance(self, node):
        if node.balanceFactor < 0:
            if node.rightChild.balanceFactor > 0:
                self.rotateRight(node.rightChild)
                self.rotateLeft(node)
            else:
                self.rotateLeft(node)
        elif node.balanceFactor > 0:
            if node.leftChild.balanceFactor < 0:
                self.rotateLeft(node.leftChild)
                self.rotateRight(node)
            else:
                self.rotateRight(node)

    def rotateLeft(self, rotRoot):
        newRoot = rotRoot.rightChild
        if newRoot.leftChild:
            left_weight = newRoot.leftChild.weight
        else:
            left_weight = 0
        rotRoot.rightChild = newRoot.leftChild
        if newRoot.leftChild:
            newRoot.leftChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if rotRoot.isRoot():
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.leftChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor + 1 - min(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor + 1 + max(rotRoot.balanceFactor, 0)
        newRoot.weight, rotRoot.weight = rotRoot.weight, rotRoot.weight - newRoot.weight + left_weight

    def rotateRight(self, rotRoot):
        newRoot = rotRoot.leftChild
        if newRoot.rightChild:
            right_weight = newRoot.rightChild.weight
        else:
            right_weight = 0
        rotRoot.leftChild = newRoot.rightChild
        if newRoot.rightChild:
            newRoot.rightChild.parent = rotRoot
        newRoot.parent = rotRoot.parent
        if not rotRoot.parent:
            self.root = newRoot
        else:
            if rotRoot.isLeftChild():
                rotRoot.parent.leftChild = newRoot
            else:
                rotRoot.parent.rightChild = newRoot
        newRoot.rightChild = rotRoot
        rotRoot.parent = newRoot
        rotRoot.balanceFactor = rotRoot.balanceFactor - 1 - max(newRoot.balanceFactor, 0)
        newRoot.balanceFactor = newRoot.balanceFactor - 1 + min(rotRoot.balanceFactor, 0)
        newRoot.weight, rotRoot.weight = rotRoot.weight, rotRoot.weight - newRoot.weight + right_weight

    def delete(self, val):
        val = (self.sum + val) % 1000000001
        if self.size > 1:
            nodeToRemove = self._get(val, self.root)
            if nodeToRemove:
                self.remove(nodeToRemove)
                self.size -= 1
            else:
                pass
        elif self.size == 1 and self.root.payload == val:
            self.root = None
            self.size -= 1
        else:
            pass

    def updateWeightRemove(self, node, weight):
        node.weight -= weight
        while node.parent:
            node.parent.weight -= weight
            node = node.parent

    def remove(self, currentNode):
        if currentNode.isLeaf():                     # leaf
            self.updateWeightRemove(currentNode, currentNode.payload)
            if currentNode == currentNode.parent.leftChild:
                currentNode.parent.balanceFactor -= 1
                currentNode.parent.leftChild = None
            else:
                currentNode.parent.rightChild = None
                currentNode.parent.balanceFactor += 1
            self.update_delete(currentNode.parent)

        elif currentNode.hasBothChildren():          # interior (two childs)
            self.updateWeightRemove(currentNode, currentNode.payload)
            succ = currentNode.findSuccessor()
            self.updateWeghtWithBoth(succ, currentNode)
            succ.spliceOut()
            currentNode.payload = succ.payload
            self.update_delete(succ.parent)
        else:                                        # this node has one child
            self.updateWeightRemove(currentNode, currentNode.payload)
            if currentNode.leftChild:
                if currentNode.isLeftChild():
                    currentNode.parent.balanceFactor -= 1
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.leftChild
                    self.update_delete(currentNode.parent)
                elif currentNode.isRightChild():
                    currentNode.parent.balanceFactor += 1
                    currentNode.leftChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.leftChild
                    self.update_delete(currentNode.parent)
                else:
                    currentNode.replaceNodeData(currentNode.leftChild.payload,
                                              currentNode.leftChild.leftChild,
                                             currentNode.leftChild.rightChild)
                    currentNode.balanceFactor -= 1
            elif currentNode.rightChild:
                if currentNode.isLeftChild():
                    currentNode.parent.balanceFactor -= 1
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.leftChild = currentNode.rightChild
                    self.update_delete(currentNode.parent)
                elif currentNode.isRightChild():
                    currentNode.parent.balanceFactor += 1
                    currentNode.rightChild.parent = currentNode.parent
                    currentNode.parent.rightChild = currentNode.rightChild
                    self.update_delete(currentNode.parent)
                else:
                    currentNode.replaceNodeData(currentNode.rightChild.payload,
                                          currentNode.rightChild.leftChild,
                                         currentNode.rightChild.rightChild)
                    currentNode.balanceFactor += 1

    def updateWeghtWithBoth(self, succ, node):
        weight = succ.payload
        while succ.parent != node:
            succ.parent.weight -= weight
            succ = succ.parent

    def update_delete(self, node):
        if node.balanceFactor in [-1, 1]:
            return
        elif node.balanceFactor > 1 or node.balanceFactor < -1:
            self.rebalance(node)
            self.update_delete(node.parent)
        elif node.parent is not None:
            if node.isLeftChild():
                node.parent.balanceFactor -= 1
            elif node.isRightChild():
                node.parent.balanceFactor += 1
            self.update_delete(node.parent)

    def get(self, val):
        val = (self.sum + val) % 1000000001
        res = "Not found"
        if self.root:
            if self._get(val, self.root):
                res = "Found"
        return res

    def _get(self, val, currentNode):
        if not currentNode:
            pass
        elif currentNode.payload == val:
            return currentNode
        elif val < currentNode.payload:
            return self._get(val, currentNode.leftChild)
        else:
            return self._get(val, currentNode.rightChild)

    def sum_segment(self, lst):
        left = (self.sum + lst[0]) % 1000000001
        right = (self.sum + lst[1]) % 1000000001
        if left > right:
            self.sum = 0
            return self.sum
        if self.root:
            s1 = self.getLeft(self.root, left, s=0)
            s2 = self.getRight(self.root, right, s=0)
            if self.root.payload < left:
                self.sum = s1 - s2
            elif self.root.payload > right:
                self.sum = s2 - s1
            else:
                self.sum = self.root.weight - s1 - s2
        else:
            self.sum = 0
        return self.sum

    def getLeft(self, node, edge, s=0):
        if edge < node.payload:
            while edge < node.payload:
                if node.leftChild:
                    node = node.leftChild
                    if node.payload == edge:
                        s = 0
                        if node.leftChild:
                            s += node.leftChild.weight
                        return s
                    elif node.payload < edge:
                        s = node.weight
                        if node.rightChild:
                            s -= self.getLeft(node, edge)
                        return s
                else:
                    return 0

        elif edge == node.payload:
            if node.leftChild:
                return node.leftChild.weight
            else:
                return 0

        elif edge > node.payload:
            while edge > node.payload:
                if node.rightChild:
                    node = node.rightChild
                    if node.payload == edge:
                        s = node.weight
                        if node.leftChild:
                            s -= node.leftChild.weight
                        return s
                    elif node.payload > edge:
                        s = node.weight
                        if node.leftChild:
                            s -= self.getLeft(node, edge)
                        return s
                else:
                    return 0

    def getRight(self, node, edge, s=0):
        if edge > node.payload:
            while node.payload < edge:
                if node.rightChild:
                    node = node.rightChild
                    if node.payload == edge:
                        s = 0
                        if node.rightChild:
                            s += node.rightChild.weight
                        return s
                    elif node.payload > edge:
                        s = node.weight
                        if node.leftChild:
                            s -= self.getRight(node, edge, s=0)
                        return s
                else:
                    return 0

        elif node.payload == edge:
            if node.rightChild:
                return node.rightChild.weight
            else:
                return 0

        elif edge < node.payload:
            while edge < node.payload:
                if node.leftChild:
                    node = node.leftChild
                    if node.payload == edge:
                        s = node.weight
                        if node.rightChild:
                            s -= node.rightChild.weight
                        return s
                    elif node.payload < edge:
                        s = node.weight
                        if node.rightChild:
                            s -= self.getRight(node, edge, s=0)
                        return s
                else:
                    return 0

    # def rec_right(self, node, edge, s=0):
    #     if node.payload < edge:
    #         s = node.payload
    #     if node.hasRightChild():
    #         s += self.rec_right(node.rightChild, edge)
    #     if node.hasLeftChild():
    #         s += self.rec_right(node.leftChild, edge)
    #     return s
    #
    # def rec_left(self, node, edge, s=0):
    #     if node.payload >= edge:
    #         s = node.payload
    #     if node.hasRightChild():
    #         s += self.rec_left(node.rightChild, edge)
    #     if node.hasLeftChild():
    #         s += self.rec_left(node.leftChild, edge)
    #     return s
    #
    # def rec_right_right(self, node, edge, s=0):
    #     if node.payload <= edge:
    #         s = node.payload
    #     if node.hasRightChild():
    #         s += self.rec_right_right(node.rightChild, edge)
    #     if node.hasLeftChild():
    #         s += self.rec_right_right(node.leftChild, edge)
    #     return s
    #
    # def rec_left_left(self, node, edge, s=0):
    #     if node.payload > edge:
    #         s = node.payload
    #     if node.hasRightChild():
    #         s += self.rec_left_left(node.rightChild, edge)
    #     if node.hasLeftChild():
    #         s += self.rec_left_left(node.leftChild, edge)
    #     return s
    #

if __name__ == '__main__':
    mytree = MyTree()
    with open("6.4.txt", 'r') as f:
        n = int(f.readline())
        for i in range(n):
            command = f.readline().split()
            if command[0] == '+':
                mytree.put(int(command[1]))
            elif command[0] == '?':
                print(mytree.get(int(command[1])))
            elif command[0] == '-':
                mytree.delete(int(command[1]))
            elif command[0] == 's':
                print(mytree.sum_segment(list(map(int, command[1:]))))

