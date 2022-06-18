from unicodedata import name

class TreeNode:
    def __init__(self, value):
        self.data = value
        self.childrens = []
        self.parent = None

    def add_child(self, child):
        self.childrens.append(child) #check if the child already exists?
        child.parent=self

    def kill_node(self):
        self.parent.childrens.remove(self)
    
    def get_depth(self):
        depth = 0
        p = self.parent
        while p:
            depth += 1
            p = p.parent
        return depth

    def print_tree(self):
        spaces = '   |' * self.get_depth()
        prefix = spaces + "-" if self.parent else ""
        print(prefix + self.data)
        if self.childrens:
            for child in self.childrens:
                child.print_tree()