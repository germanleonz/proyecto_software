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
            if nuevo.data.is_active == True:
                self.add_child(nuevo)
                nuevo.generate_tree()

    def generate_CronologicalOrder(self,idpiz, loginasignado):
        """
        Metodo que genera el orden cronologico como arbol
        """
        lista = app_actividad.models.orden_cronologico(idpiz,loginasignado)
        self.data = lista[0]
        actual = self
        for i in range(1,len(lista)):
            siguiente = Node(lista[i])
            if siguiente.data.is_active == True:
                actual.add_child(siguiente)
                actual = siguiente           
    
    def generate_stateOrder(self):
        """
        Metodo que genera el arbol por estados 
        """
        pila = []
        pila.append(self)
        while (len(pila)>0):
            actual = pila.pop()
            hijos = app_actividad.models.obtener_hijos(actual.data)
            for elem in hijos:
                nuevo = Node(elem)
                if nuevo.data.is_active == True:
                    if self.children == []:
                        self.add_child(nuevo)
                    else:
                        seteado = False
                        for obj in self.children:
                            if nuevo.data.estadoact == obj.data.estadoact:
                                obj.setLastChild(nuevo)
                                seteado = True
                                break
                        if seteado == False:
                            self.add_child(nuevo)

                    pila.append(nuevo)

    def setLastChild(self,objeto):
        """
        Metodo que setea a objeto como ultimo hijo de una rama lineal
        """
        if self.children == []:
            self.add_child(objeto)
        else:
            self.children[0].setLastChild(objeto)

    def generate_advanceOrder(self, idpiz, loginasignado):
        """
        Metodo que genera el arbol por avance
        """
        lista = app_actividad.models.orden_porAvance(idpiz,loginasignado)
        self.data = lista[0]
        actual = self
        for i in range(1,len(lista)):
            siguiente = Node(lista[i])
            actual.add_child(siguiente)
            actual = siguiente           
            
    def generate_json(self):
        """
        Metodo que genera el string en formato json para los nodos del spacetree
        """

        string = '"id": "'+str(self.data.idact)+'",'
        string += '"name": "'+self.data.nombreact+' '
        string += self.data.loginasignado.username+' '
        string += str(self.data.avanceact)+'",'
        string += '"data": { "$color" : '
        if (self.data.estadoact == 'c'):
            string += ' "#19AC19" }'
        elif (self.data.estadoact == 'r'):
            string += ' "#FFCC00" }'
        elif (self.data.estadoact == 'e'):
            string += ' "#3399FF" }'
        elif (self.data.estadoact == 'p'):
            string += ' "#FF0000" }'
        elif (self.data.estadoact == 's'):
            string += ' "#FFFFFF" }'

        string += ','
        string += '"children": ['
        
        if (len(self.children)>0):
            for elem in self.children:
                string += '{'
                string += elem.generate_json()
                string += '},'
        
            string = string[:-1]
            
        string += ']'

        return string
        



                
