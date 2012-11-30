class Node(object):
    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.children = []

    def add_child(self, obj):
        self.children.append(obj)

    def get_child(self,index):
        return self.children[index] 
    
    def print_tree(self):
        print "padre ",self.data
        for i in range (0,len(self.children)):
            if isinstance(self.children[i],Node):
                self.children[i].print_tree()
            else:
                print self.children[i]
    def get_edges(self,lista):
        for i in range (0,len(self.children)):
            if isinstance(self.children[i],Node):
                lista = self.children[i].get_edges(lista)
                lista.append((self.data,self.children[i].data))
            else:
                lista.append((self.data,self.children[i]))

        return lista
