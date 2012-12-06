import app_actividad.models 

class Node(object):
    """
    Clase que implementa un arbol de n-hijos
    """

    def __init__(self, data):
        """
        Constructor
      """
        self.data = data
        self.children = []

    def add_child(self, obj):
        """
        Metodo que agrega un hijo a self
        """
        self.children.append(obj)

    def get_child(self,index):
        """
        Metodo que obtiene un hijo de self
        """
        return self.children[index] 
    
    def print_tree(self):
        """
        Metodo que imprime el arbol
        """
        print self.data.nombreact
        for i in range (0,len(self.children)):
            if isinstance(self.children[i],Node):
                self.children[i].print_tree()
            else:
                print self.children[i]

    def get_edges(self,lista):
        """
        Metodo que obtiene los lados del arbol self y los retorna en una lista
        """
        for i in range (0,len(self.children)):
            if isinstance(self.children[i],Node):
                lista = self.children[i].get_edges(lista)
                lista.append((self.data,self.children[i].data))
            else:
                lista.append((self.data,self.children[i]))

        return lista

    def generate_tree(self):
        """
        Metodo que genera el arbol a partir de un root actividad
        """
        hijos = app_actividad.models.obtener_hijos(self.data)
        for elem in hijos:
            nuevo = Node(elem)
            self.add_child(nuevo)
            nuevo.generate_tree()
            
    def generate_json(self):
        """
        Metodo que genera el string en formato json para los nodos del spacetree
        """

        string = '"id": "'+str(self.data.idact)+'",'
        string += '"name": "'+self.data.nombreact+'",'
        string += '"data": {},'
        string += '"children": ['
        
        if (len(self.children)>0):
            for elem in self.children:
                string += '{'
                string += elem.generate_json()
                string += '},'
        
            string = string[:-1]
            
        string += ']'

        return string
        



                
