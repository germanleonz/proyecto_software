from django.utils import TestCase

class PizarraModelTest(TestCase):
    """docstring for PizarraModelTest"""
    def test_crear_una_nueva_pizarra_y_guardarla_en_la_bd(self): 
        p = Pizarra()
        p.fechacreacion = timezone.now()
        p.fechafinal = timezone.now() 

        p.save()

        pizarras = Pizarra.objects.all()
        self.assertEquals(len(pizarras), 1)

    def test_actualizar_info_de_pizarra_luego_de_creacion(self):
        pass

