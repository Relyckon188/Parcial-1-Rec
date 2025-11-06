# tests/test_especialidad_alumnos.py
import unittest
from app import create_app, db
from app.models import Especialidad, Facultad, Alumno, Usuario
from app.services import EspecialidadService
from test.instancias import nueva_facultad, nueva_especialidad, nuevo_alumno

class TestEspecialidadAlumnos(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_obtener_alumnos_especialidad_con_facultad(self):
        # Arrange
        facultad = nueva_facultad(nombre="Ingeniería")
        especialidad = nueva_especialidad(
            nombre="Ingeniería de Sistemas", 
            facultad=facultad
        )
        
        alumno1 = nuevo_alumno(
            nombre="Juan Pérez",
            especialidad=especialidad
        )
        alumno2 = nuevo_alumno(
            nombre="María García", 
            especialidad=especialidad
        )

        # Act
        resultado = EspecialidadService.obtener_alumnos_con_facultad(especialidad.id)

        # Assert
        self.assertIsNotNone(resultado)
        self.assertEqual(resultado['especialidad']['nombre'], "Ingeniería de Sistemas")
        self.assertEqual(resultado['facultad']['nombre'], "Ingeniería")
        self.assertEqual(len(resultado['alumnos']), 2)
        self.assertEqual(resultado['alumnos'][0]['nombre'], "Juan Pérez")

    def test_obtener_alumnos_especialidad_sin_alumnos(self):
        # Arrange
        facultad = nueva_facultad()
        especialidad = nueva_especialidad(facultad=facultad)

        # Act
        resultado = EspecialidadService.obtener_alumnos_con_facultad(especialidad.id)

        # Assert
        self.assertIsNotNone(resultado)
        self.assertEqual(len(resultado['alumnos']), 0)
        self.assertEqual(resultado['especialidad']['nombre'], especialidad.nombre)

    def test_obtener_alumnos_especialidad_inexistente(self):
        # Act
        resultado = EspecialidadService.obtener_alumnos_con_facultad(999)

        # Assert
        self.assertIsNone(resultado)

    def test_formato_json_correcto(self):
        # Arrange
        facultad = nueva_facultad(nombre="Medicina", codigo="MED")
        especialidad = nueva_especialidad(
            nombre="Medicina General", 
            codigo="MG",
            facultad=facultad
        )
        alumno = nuevo_alumno(
            nombre="Carlos López",
            codigo="A001",
            especialidad=especialidad
        )

        # Act
        resultado = EspecialidadService.obtener_alumnos_con_facultad(especialidad.id)

        # Assert
        self.assertEqual(resultado['especialidad']['nombre'], "Medicina General")
        self.assertEqual(resultado['especialidad']['codigo'], "MG")
        self.assertEqual(resultado['facultad']['nombre'], "Medicina")
        self.assertEqual(resultado['facultad']['codigo'], "MED")
        self.assertEqual(resultado['alumnos'][0]['nombre'], "Carlos López")
        self.assertEqual(resultado['alumnos'][0]['codigo'], "A001")