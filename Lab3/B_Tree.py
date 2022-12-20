import math
from B_Tree_Node import BTreeNode
from Database_Object import DatabaseObject


class BTree:
    def __init__(self, t=10):
        self.root = BTreeNode(True)
        self.t = t
        self.counter = 0

    def search(self, key, start_node='default'):
        if start_node == 'default':
            start_node = self.root

        if not start_node.leaf:
            for i in range(len(start_node.keys)):
                self.counter += 1
                if key < start_node.keys[i]:
                    return self.search(key, start_node.children[i])
                elif key == start_node.keys[i]:
                    return start_node.keys[i]
            if start_node.children:
                return self.search(key, start_node.children[-1])
        else:
            return self.__Sharr_algorithm(key, start_node)

    def insert(self, k):
        root = self.root
        if len(root.keys) < (2 * self.t) - 1:
            self.__insert_non_full(root, k)
        else:
            temp = BTreeNode()
            self.root = temp
            temp.children.insert(0, root)
            self.__split_children(temp, 0)
            self.__insert_non_full(temp, k)

    def delete(self, node, value):
        t = self.t
        i = 0
        while i < len(node.keys) and value > node.keys[i]:
            i += 1
        if node.leaf:
            if i < len(node.keys) and node.keys[i] == value:
                node.keys.pop(i)
                return
            return

        if i < len(node.keys) and node.keys[i] == value:
            return self.__delete_internal_node(node, value, i)
        elif len(node.children[i].keys) >= t:
            self.delete(node.children[i], value)
        else:
            if i != 0 and i + 2 < len(node.children):
                if len(node.children[i - 1].keys) >= t:
                    self.__delete_sibling(node, i, i - 1)
                elif len(node.children[i + 1].keys) >= t:
                    self.__delete_sibling(node, i, i + 1)
                else:
                    self.__delete_merge(node, i, i + 1)
            elif i == 0:
                if len(node.children[i + 1].keys) >= t:
                    self.__delete_sibling(node, i, i + 1)
                else:
                    self.__delete_merge(node, i, i + 1)
            elif i + 1 == len(node.children):
                if len(node.children[i - 1].keys) >= t:
                    self.__delete_sibling(node, i, i - 1)
                else:
                    self.__delete_merge(node, i, i - 1)
            self.delete(node.children[i], value)

    def edit(self, old_obj, new_value):
        self.delete(self.root, old_obj)
        new_obj = DatabaseObject(old_obj.index, new_value)
        self.insert(new_obj)

    def __insert_non_full(self, node, k):
        i = len(node.keys) - 1
        if node.leaf:
            while i >= 0 and k < node.keys[i]:
                i -= 1
            node.keys.insert(i + 1, k)
        else:
            while len(node.children) < len(node.keys) + 1:
                node.children.append(BTreeNode(True))
            while i >= 0 and k < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == (2 * self.t) - 1:
                self.__split_children(node, i)
                if k > node.keys[i]:
                    i += 1
            self.__insert_non_full(node.children[i], k)

    def __split_children(self, x, i):
        t = self.t
        y = x.children[i]
        z = BTreeNode(y.leaf)
        x.children.insert(i + 1, z)
        x.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t: (2 * t) - 1]
        y.keys = y.keys[0: t - 1]
        if not y.leaf:
            z.children = y.children[t: 2 * t]
            y.children = y.children[0: t]

    def __Sharr_algorithm(self, key, node):
        k = math.floor(math.log(len(node.keys), 2))
        i = 2 ** k
        if node.keys[i - 1] == key:
            return node.keys[i - 1]
        elif node.keys[i - 1] > key:
            return self.__binary_search(key, node)
        else:
            l = math.floor(math.log(len(node.keys) - 2 ** k + 1, 2))
            i = len(node.keys) + 1 - 2 ** l
            l -= 1
            delta = math.floor(2 ** l)
            while 0 < i <= len(node.keys):
                self.counter += 1
                if node.keys[int(i) - 1] < key:
                    i = i + (delta // 2 + 1)
                    l -= 1
                    delta = 2 ** l
                elif node.keys[int(i) - 1] > key:
                    i = i - (delta // 2 + 1)
                    l -= 1
                    delta = 2 ** l
                else:
                    return node.keys[int(i) - 1]
            return None

    def __binary_search(self, key, node):
        temp_list = node.keys
        i = len(temp_list) // 2 + 1
        delta = len(temp_list) // 2
        temp_list.append(float('inf'))
        while delta != 0 and 1 <= i <= len(temp_list):
            self.counter += 1
            if temp_list[i - 1] < key:
                i = i + (delta // 2 + 1)
                delta //= 2
            elif temp_list[i - 1] > key:
                i = i - (delta // 2 + 1)
                delta //= 2
            else:
                temp_list.remove(float('inf'))
                return temp_list[i - 1]
        if temp_list[i - 1] == key:
            temp_list.remove(float('inf'))
            return temp_list[i - 1]
        temp_list.remove(float('inf'))
        return None

    def __delete_internal_node(self, node, value, i):
        t = self.t
        if node.leaf:
            if node.keys[i] == value:
                node.keys.pop(i)
                return
            return

        if len(node.children[i].keys) >= t:
            node.keys[i] = self.__delete_predecessor(node.children[i])
            return
        elif len(node.children[i + 1].keys) >= t:
            node.keys[i] = self.__delete_successor(node.children[i + 1])
            return
        else:
            self.__delete_merge(node, i, i + 1)
            self.__delete_internal_node(node.children[i], value, self.t - 1)

    def __delete_predecessor(self, node):
        if node.leaf:
            return node.keys.pop()
        n = len(node.keys) - 1
        if len(node.children[n].keys) >= self.t:
            self.__delete_sibling(node, n + 1, n)
        else:
            self.__delete_merge(node, n, n + 1)
        self.__delete_predecessor(node.children[n])

    def __delete_successor(self, node):
        if node.leaf:
            return node.keys.pop(0)
        if len(node.children[1].keys) >= self.t:
            self.__delete_sibling(node, 0, 1)
        else:
            self.__delete_merge(node, 0, 1)
        self.__delete_successor(node.children[0])

    def __delete_merge(self, node, i, j):
        cnode = node.children[i]
        if j > i:
            rsnode = node.children[j]
            cnode.keys.append(node.keys[i])
            for k in range(len(rsnode.keys)):
                cnode.keys.append(rsnode.keys[k])
                if len(rsnode.children) > 0:
                    cnode.children.append(rsnode.child[k])
            if len(rsnode.children) > 0:
                cnode.children.append(rsnode.children.pop())
            new = cnode
            node.keys.pop(i)
            node.children.pop(j)
        else:
            lsnode = node.child[j]
            lsnode.keys.append(node.keys[j])
            for i in range(len(cnode.keys)):
                lsnode.keys.append(cnode.keys[i])
                if len(lsnode.children) > 0:
                    lsnode.children.append(cnode.children[i])
            if len(lsnode.children) > 0:
                lsnode.children.append(cnode.children.pop())
            new = lsnode
            node.keys.pop(j)
            node.children.pop(i)

        if node == self.root and len(node.keys) == 0:
            self.root = new

    def __delete_sibling(self, node, i, j):
        cnode = node.children[i]
        if i < j:
            rsnode = node.children[j]
            cnode.keys.append(node.keys[i])
            node.keys[i] = rsnode.keys[0]
            if len(rsnode.children) > 0:
                cnode.children.append(rsnode.children[0])
                rsnode.children.pop(0)
            rsnode.keys.pop(0)
        else:
            lsnode = node.children[j]
            cnode.keys.insert(0, node.keys[i - 1])
            node.keys[i - 1] = lsnode.keys.pop()
            if len(lsnode.children) > 0:
                cnode.children.insert(0, lsnode.children.pop())
