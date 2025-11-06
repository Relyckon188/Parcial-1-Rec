import unittest
import os
from flask import current_app
from app import create_app
from app.models.tipodocumento import TipoDocumento
from app.services import TipoDocumentoService
from test.instancias import nuevotipodocumento
from app import db

class TipoDocumentoTestCase(unittest.TestCase):
    def setUp(self):
        os.environ['FLASK_CONTEXT'] = 'testing'
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear(self):
        tipodocumento = nuevotipodocumento()  # crea y guarda un tipo documento
        self.assertIsNotNone(tipodocumento)
        self.assertIsNotNone(tipodocumento.id)
        self.assertGreaterEqual(tipodocumento.id, 1)

    def test_buscar_por_id(self):
        tipodocumento = nuevotipodocumento(sigla="LC", nombre="Libreta Cívica")
        resultado = TipoDocumentoService.buscar_por_id(tipodocumento.id)
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado.nombre, "Libreta Cívica")

    def test_buscar_todos(self):
        nuevotipodocumento(sigla="DNI", nombre="Documento Nacional de Identidad")
        nuevotipodocumento(sigla="PAS", nombre="Pasaporte")
        documentos = TipoDocumentoService.buscar_todos()
        self.assertIsNotNone(documentos)
        self.assertEqual(len(documentos), 2)

    def test_actualizar(self):
        tipodocumento = nuevotipodocumento(sigla="DNI", nombre="Documento Nacional de Identidad")
        tipodocumento_actualizado = TipoDocumentoService.actualizar(
            tipodocumento.id, {"nombre": "Documento Identidad Nacional"}
        )
        self.assertEqual(tipodocumento_actualizado.nombre, "Documento Identidad Nacional")

    def test_borrar(self):
        tipodocumento = nuevotipodocumento(sigla="LC", nombre="Libreta Cívica")
        borrado = TipoDocumentoService.borrar_por_id(tipodocumento.id)
        self.assertTrue(borrado)
        resultado = TipoDocumentoService.buscar_por_id(tipodocumento.id)
        self.assertIsNone(resultado)
