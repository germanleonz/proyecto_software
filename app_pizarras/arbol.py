class Node(object):
    def __init__(self, data):
        self.data = data
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

    def generate_list(self):
        act = self.children
        lista = []
        lista.append(self.data)
        while ( len(act)>0 ):
            ady = act.pop()
            if len(ady.children)>0:
                for i in range (0,len(ady.children)):
                    act.append(ady.children[i])
            else:
                lista.append(ady.data)
        return lista

           
           


