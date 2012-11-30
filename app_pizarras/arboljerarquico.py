class Node(object):
    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.children = []
        
    def add_child(self, obj):
        self.children.append(obj)

    def get_child(self,index):
        return self.children[index]






