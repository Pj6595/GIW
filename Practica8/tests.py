"""
Enrique Martín <emartinm@ucm.es> 2020
Tests de unidad para probar la práctica 8 "Persistencia en Python"

lanzar TODOS los tests desde el terminal:
$ python -m unittest tests.TestPersistencia

Lanzar un test concreto desde el terminal
$ python -m unittest tests.TestPersistencia.test_usuarios_validos
"""

import unittest
from mongoengine.errors import ValidationError
from mongoengine import connect
from gr06_mongoengine import Producto, Linea, Pedido, Tarjeta, Usuario, inserta
import inspect


PRODUCTOS_INCORRECTOS = [
            Producto(nombre=32, codigo_barras="1234567895412", categoria_principal=5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre=True, codigo_barras="1234567895412", categoria_principal=5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="a", codigo_barras="1234567895412", categoria_principal=5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(codigo_barras="1234567895412", categoria_principal=5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="a", codigo_barras="1234567895412", categoria_principal=5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas", codigo_barras=32, categoria_principal=5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas", codigo_barras=[1, 2, 3], categoria_principal=5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas", categoria_principal=5, categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas", codigo_barras="4006381333930", categoria_principal=5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas Oreo", codigo_barras="1234567895412", categoria_principal="alimentos",
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas O"
                            "reo", codigo_barras="1234567895412", categoria_principal=False,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas Oreo", codigo_barras="1234567895412", categoria_principal=-5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas Oreo", codigo_barras="1234567895412", categoria_principal=3.14,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas Oreo", codigo_barras="1234567895412", categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas Oreo", codigo_barras="1234567895412", categoria_principal=5,
                     categorias_secundarias=[]),
            Producto(nombre="Galletas Oreo", codigo_barras="1234567895412", categoria_principal=5,
                     categorias_secundarias=[8, 5, 9]),
            Producto(nombre="Galletas Oreo", codigo_barras="1234567895412", categoria_principal=5,
                     categorias_secundarias="alimentos"),
            Producto(nombre="Galletas Oreo", codigo_barras="1234567895412", categoria_principal=5,
                     categorias_secundarias="5, 4, 7")
        ]

PRODUCTOS_CORRECTOS = [
            Producto(nombre="Galletas Oreo", codigo_barras="9780201379624", categoria_principal=5,
                     categorias_secundarias=[5, 8, 9]),
            Producto(nombre="Galletas Cuetara", codigo_barras="9780201345629", categoria_principal=5,
                     categorias_secundarias=[5, 8, 10]),
            Producto(nombre="Bizcochitos", codigo_barras="5642379109004", categoria_principal=0,
                     categorias_secundarias=[0, 5])
        ]

LINEAS_INCORRECTAS = lineas_invalidas = [
            Linea(precio_item=1.5, name="Galletas Oreo", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items="dos", precio_item=1.5, name="Galletas Oreo", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=[1, 2, 3], precio_item=1.5, name="Galletas Oreo", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=0, precio_item=1.5, name="Galletas Oreo", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),

            Linea(num_items=3, name="Galletas Oreo", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item=0, name="Galletas Oreo", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item="hola", name="Galletas Oreo", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item=-100, name="Galletas Oreo", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),

            Linea(num_items=3, precio_item=0, total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item=1.5, name=56, total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item=1.5, name=["Gallet"
                                                      "as Oreao"], total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item=1.5, name="Galletas Orea", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item=1.5, name="G", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),

            Linea(num_items=3, precio_item=1.5, name="Galletas Oreo", ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item=1.5, name="Galletas Oreo", total="hola", ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item=1.5, name="Galletas Oreo", total=4, ref=PRODUCTOS_CORRECTOS[0]),
            Linea(num_items=3, precio_item=1.5, name="Galletas Oreo", total=4.6, ref=PRODUCTOS_CORRECTOS[0]),

            Linea(num_items=3, precio_item=1.5, name="Galletas Oreo", total=4.5)
        ]

LINEAS_CORRECTAS = [
    Linea(num_items=3, precio_item=1.5, name="Galletas Oreo", total=4.5, ref=PRODUCTOS_CORRECTOS[0]),
    Linea(num_items=3, precio_item=1, name="Galletas Oreo", total=3, ref=PRODUCTOS_CORRECTOS[0]),
    Linea(num_items=1, precio_item=2, name="Galletas Oreo", total=2, ref=PRODUCTOS_CORRECTOS[0]),
    Linea(num_items=1, precio_item=1.5, name="Galletas Cuetara", total=1.5, ref=PRODUCTOS_CORRECTOS[1]),
    Linea(num_items=2, precio_item=4.5, name="Bizcochitos", total=9.0, ref=PRODUCTOS_CORRECTOS[2])
]

PEDIDOS_INCORRECTOS = [
    Pedido(fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0]]),
    Pedido(total="hola", fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0]]),
    Pedido(total=False, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0]]),
    Pedido(total=24.5, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0]]),

    Pedido(total=4.5, lineas=[LINEAS_CORRECTAS[0]]),
    Pedido(total=4.5, fecha=4, lineas=[LINEAS_CORRECTAS[0]]),
    Pedido(total=4.5, fecha=False, lineas=[LINEAS_CORRECTAS[0]]),
    Pedido(total=4.5, fecha=[1, 2, 3], lineas=[LINEAS_CORRECTAS[0]]),

    Pedido(total=4.5, fecha='2016,11,25,10,15,24,000000'),
    Pedido(total=4.5, fecha='2016,11,25,10,15,24,000000', lineas=None),
    Pedido(total=4.5, fecha='2016,11,25,10,15,24,000000', lineas=35),

    Pedido(total=4.5, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0], LINEAS_CORRECTAS[3],
                                                                  LINEAS_CORRECTAS[4]]),
    Pedido(total=12, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0], LINEAS_CORRECTAS[3],
                                                                 LINEAS_CORRECTAS[4]]),
    Pedido(total=77, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0], LINEAS_CORRECTAS[3],
                                                                 LINEAS_CORRECTAS[4]]),

    Pedido(total=7.5, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0], LINEAS_CORRECTAS[1]]),
    Pedido(total=5, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[1], LINEAS_CORRECTAS[2]]),
    Pedido(total=6.5, fecha='2016,11,25,10,15,24,000000',
           lineas=[LINEAS_CORRECTAS[3], LINEAS_CORRECTAS[2], LINEAS_CORRECTAS[1]]),
    Pedido(total=11, fecha='2016,11,25,10,15,24,000000',
           lineas=[LINEAS_CORRECTAS[3], LINEAS_CORRECTAS[2], LINEAS_CORRECTAS[0], LINEAS_CORRECTAS[1]])
]

PEDIDOS_CORRECTOS = [
    Pedido(total=4.5, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0]]),
    Pedido(total=6, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0], LINEAS_CORRECTAS[3]]),
    Pedido(total=15, fecha='2016,11,25,10,15,24,000000', lineas=[LINEAS_CORRECTAS[0], LINEAS_CORRECTAS[3],
                                                                 LINEAS_CORRECTAS[4]])
]

TARJETAS_INCORRECTAS = [
    Tarjeta(numero="4500874512587896", mes="12", año="19", ccv="852"),
    Tarjeta(nombre="P", numero="4500874512587896", mes="12", año="19", ccv="852"),
    Tarjeta(nombre=325, numero="4500874512587896", mes="12", año="19", ccv="852"),
    Tarjeta(nombre=False, numero="4500874512587896", mes="12", año="19", ccv="852"),

    Tarjeta(nombre="Pepe", mes="12", año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero=1236547896521458, mes="12", año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero=4500874512587896, mes="12", año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero="500874512587896", mes="12", año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero="45008745125878966", mes="12", año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero="45008j4512587896", mes="12", año="19", ccv="852"),

    Tarjeta(nombre="Pepe", numero="4500874512587896", año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes=12, año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="1", año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="II", año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="ENE", año="19", ccv="852"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="123", año="19", ccv="852"),

    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", ccv="852"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año=19, ccv="852"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="1", ccv="852"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="193", ccv="852"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="EN", ccv="852"),

    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="19"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="19", ccv="85"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="19", ccv="8523"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="19", ccv="87T"),
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="19", ccv=852),
]

TARJETAS_CORRECTAS = [
    Tarjeta(nombre="Pepe", numero="4500874512587896", mes="12", año="19", ccv="852"),
    Tarjeta(nombre="Ana", numero="6786543651354687", mes="06", año="20", ccv="123"),
    Tarjeta(nombre="Eva", numero="9845631321564987", mes="10", año="22", ccv="745")
]

USUARIOS_CORRECTOS = [
    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="81614026K", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11"),
    Usuario(dni="22246432G", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="20847860Q", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]]),
    Usuario(dni="77944903L", nombre="Pepe", apellido1="Peces", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="21039092A", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="2000-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
]

USUARIOS_INCORRECTOS = [
    Usuario(nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni=65068806, nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806M", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806X", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806B", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),

    Usuario(dni="65068806N", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre="P", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre=34, apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),

    Usuario(dni="65068806N", nombre="Pepe", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre="Pepe", apellido1="M", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre="Pepe", apellido1=45, apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre="Pepe", apellido1="", apellido2="Cuadrado", f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),

    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2=358, f_nac="1985-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),

    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac=58,
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985/12/11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="98-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),

    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="98-12-11",
            tarjetas=38,
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),
    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="98-12-11",
            tarjetas="hola",
            pedidos=[PEDIDOS_CORRECTOS[0], PEDIDOS_CORRECTOS[2]]),

    Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="98-12-11",
            tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
            pedidos="hola"),
]


def init():
    connect('giw_mongoengine')


def obj_str(o):
    """Representa todos los atributos del objeto en una cadena"""
    class_name = type(o).__name__
    attrs = dict()
    members = inspect.getmembers(o)
    for k, v in members:
        if (not k.startswith('_') and not inspect.ismethod(v) and not inspect.isfunction(v)
                and not inspect.isclass(v) and k != 'STRICT'):
            attrs[k] = v
    return f"{class_name}({attrs})"


class TestPersistencia(unittest.TestCase):
    """Tests a ejecutar sobre las clases """
    
    def setUp(self):
        connect('giw_mongoengine')
        
    def tearDown(self):
        Usuario.drop_collection()
        Pedido.drop_collection()
        Producto.drop_collection()
    

    def test_producto_invalido(self):
        """Productos con datos incorrectos"""
        for p in PRODUCTOS_INCORRECTOS:
            with self.assertRaises(ValidationError, msg=obj_str(p)):
                p.save(cascade=True, force_insert=True)

    def test_productos_validos(self):
        """Productos con datos validos"""
        for p in PRODUCTOS_CORRECTOS:
            p.save(cascade=True, force_insert=True)
            psaved = Producto.objects.get(pk=p.pk)
            self.assertEqual(p, psaved)
        self.assertEqual(len(Producto.objects), len(PRODUCTOS_CORRECTOS))

    def test_lineas_invalidas(self):
        """Lineas con datos invalidos"""
        for linea in LINEAS_INCORRECTAS:
            with self.assertRaises(ValidationError, msg=obj_str(linea)):
                linea.validate()

    def test_lineas_validas(self):
        """Lineas con datos validos"""
        for linea in LINEAS_CORRECTAS:
            linea.ref.save()
            linea.validate()

    def test_pedidos_invalidos(self):
        """Pedidos con datos invalidos"""
        for pedido in PEDIDOS_INCORRECTOS:
            with self.assertRaises(ValidationError, msg=obj_str(pedido)):
                pedido.save(cascade=True, force_insert=True)

    def test_pedidos_validos(self):
        """Pedidos con datos válidos"""
        for pedido in PEDIDOS_CORRECTOS:
            pedido.save(cascade=True, force_insert=True)
            pedido_added = Pedido.objects.get(pk=pedido.pk)
            self.assertEqual(pedido, pedido_added, msg=obj_str(pedido))
        self.assertEqual(len(Pedido.objects), len(PEDIDOS_CORRECTOS))
        Pedido.drop_collection()
        Producto.drop_collection()

    def test_tarjetas_invalidas(self):
        """Tarjetas con datos invalidos"""
        for tarjeta in TARJETAS_INCORRECTAS:
            with self.assertRaises(ValidationError, msg=obj_str(tarjeta)):
                tarjeta.validate()

    def test_tarjetas_validas(self):
        """Tarjetas con datos válidos"""
        for tarjeta in TARJETAS_CORRECTAS:
            tarjeta.validate()

    def test_usuarios_invalidos(self):
        """Usuarios con datos incorrectos"""
        for usuario in USUARIOS_INCORRECTOS:
            with self.assertRaises(ValidationError, msg=obj_str(usuario)):
                usuario.save(cascade=True, force_insert=True)

    def test_usuarios_validos(self):
        """Creación de usuarios con datos válidos"""
        for e in PRODUCTOS_CORRECTOS + PEDIDOS_CORRECTOS:
            e.save()

        for usuario in USUARIOS_CORRECTOS:
            usuario.save(cascade=True, force_insert=True)
            usuario_added = Usuario.objects.get(pk=usuario.pk)
            self.assertEqual(usuario, usuario_added, msg=obj_str(usuario))
        self.assertEqual(len(Usuario.objects), len(USUARIOS_CORRECTOS))

    def test_eliminacion_pedido(self):
        """Eliminación automática de pedidos"""
        Usuario.drop_collection()
        Pedido.drop_collection()
        Producto.drop_collection()

        prod1 = Producto(nombre="Galletas Oreo", codigo_barras="9780201379624", categoria_principal=5,
                         categorias_secundarias=[5, 8, 9])
        prod1.save(cascade=True, force_insert=True)
        linea = Linea(num_items=3, precio_item=1.5, name="Galletas Oreo", total=4.5, ref=prod1)
        p1 = Pedido(total=4.5, fecha='2016,11,25,10,15,24,000000', lineas=[linea])
        p1.save(cascade=True, force_insert=True)

        u = Usuario(dni="65068806N", nombre="Pepe", apellido1="Peces", apellido2="Cuadrado", f_nac="1985-12-11",
                    tarjetas=[TARJETAS_CORRECTAS[0], TARJETAS_CORRECTAS[1]],
                    pedidos=[p1])
        u.save(cascade=True, force_insert=True)
        self.assertEqual(len(u.pedidos), 1)
        
        p1.delete()
        u.reload()
        self.assertEqual(len(u.pedidos), 0)

    def test_inserta(self):
        """Comprueba que la función inserta almacena el número esperado de objetos"""
        Usuario.drop_collection()
        Pedido.drop_collection()
        Producto.drop_collection()

        self.assertEqual(len(Usuario.objects), 0)
        self.assertEqual(len(Pedido.objects), 0)
        self.assertEqual(len(Producto.objects), 0)

        inserta()
        self.assertTrue(len(Usuario.objects) >= 2)

        for user in Usuario.objects:
            self.assertTrue(len(user.pedidos) >= 2)
            for pedido in user.pedidos:
                self.assertTrue(len(pedido.lineas) > 1)
            self.assertTrue(len(user.tarjetas) >= 2)
