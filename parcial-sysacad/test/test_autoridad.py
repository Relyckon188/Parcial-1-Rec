import unittest
from app import create_app, db
from app.models import Autoridad, Materia, Facultad, Cargo
from app.services import AutoridadService
from test.instancias import nuevaautoridad, nuevamateria, nuevafacultad

class AutoridadTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_crear(self):
        facultad = nuevafacultad()
        materia = nuevamateria()
        autoridad = nuevaautoridad(materias=[materia], facultades=[facultad])
        
        self.assertIsNotNone(autoridad.id)
        self.assertEqual(autoridad.nombre, "Pelo")
        self.assertIn(materia, autoridad.materias)
        self.assertIn(facultad, autoridad.facultades)

    def test_buscar_por_id(self):
        autoridad = nuevaautoridad()
        encontrado = AutoridadService.buscar_por_id(autoridad.id)
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado.nombre, autoridad.nombre)

    def test_buscar_todos(self):
        autoridad1 = nuevaautoridad(nombre="Pelo1")
        autoridad2 = nuevaautoridad(nombre="Pelo2")
        autoridades = AutoridadService.buscar_todos()
        self.assertIsNotNone(autoridades)
        self.assertGreaterEqual(len(autoridades), 2)
        nombres = [a.nombre for a in autoridades]
        self.assertIn("Pelo1", nombres)
        self.assertIn("Pelo2", nombres)

    def test_actualizar(self):
        autoridad = nuevaautoridad()
        datos_actualizacion = {"nombre": "Nombre Actualizado"}
        actualizado = AutoridadService.actualizar(autoridad.id, datos_actualizacion)
        self.assertEqual(actualizado.nombre, "Nombre Actualizado")

    def test_borrar(self):
        autoridad = nuevaautoridad()
        borrado = AutoridadService.borrar_por_id(autoridad.id)
        self.assertTrue(borrado)
        resultado = AutoridadService.buscar_por_id(autoridad.id)
        self.assertIsNone(resultado)

    def test_relacion_materias(self):
        autoridad = nuevaautoridad()
        materia1 = nuevamateria(nombre="Matematica")
        materia2 = nuevamateria(nombre="Fisica")

        # Asociar materias desde autoridad.materias 
        autoridad.materias.append(materia1)
        autoridad.materias.append(materia2)
        db.session.commit()

        # Recargar la autoridad de la base de datos
        autoridad_db = AutoridadService.buscar_por_id(autoridad.id)
        
        self.assertIn(materia1, autoridad_db.materias)
        self.assertIn(materia2, autoridad_db.materias)

        # Desasociar una materia
        autoridad_db.materias.remove(materia1)
        db.session.commit()
        
        # Verificar que se desasoció correctamente
        autoridad_actualizada = AutoridadService.buscar_por_id(autoridad.id)
        self.assertNotIn(materia1, autoridad_actualizada.materias)

    def test_asociar_y_desasociar_materia(self):
        autoridad = nuevaautoridad()
        materia = nuevamateria()

        # Asociar materia
        resultado = AutoridadService.asociar_materia(autoridad.id, materia.id)
        self.assertTrue(resultado)
        
        autoridad_actualizada = AutoridadService.buscar_por_id(autoridad.id)
        self.assertIn(materia, autoridad_actualizada.materias)

        # Desasociar materia
        resultado = AutoridadService.desasociar_materia(autoridad.id, materia.id)
        self.assertTrue(resultado)
        
        autoridad_actualizada = AutoridadService.buscar_por_id(autoridad.id)
        self.assertNotIn(materia, autoridad_actualizada.materias)

    def test_asociar_y_desasociar_facultad(self):
        facultad = nuevafacultad()
        autoridad = nuevaautoridad()

        # Asociar facultad
        resultado = AutoridadService.asociar_facultad(autoridad.id, facultad.id)
        self.assertTrue(resultado)
        
        autoridad_actualizada = AutoridadService.buscar_por_id(autoridad.id)
        self.assertIn(facultad, autoridad_actualizada.facultades)

        # Desasociar facultad
        resultado = AutoridadService.desasociar_facultad(autoridad.id, facultad.id)
        self.assertTrue(resultado)
        
        autoridad_actualizada = AutoridadService.buscar_por_id(autoridad.id)
        self.assertNotIn(facultad, autoridad_actualizada.facultades)

    def test_crear_autoridad_sin_relaciones(self):
        autoridad = nuevaautoridad(materias=[], facultades=[])
        self.assertIsNotNone(autoridad.id)
        self.assertEqual(autoridad.nombre, "Pelo")
        self.assertEqual(len(autoridad.materias), 0)
        self.assertEqual(len(autoridad.facultades), 0)