import os, sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from models import models
from run import app, ingest_data
import unittest
import json


class TestView(unittest.TestCase):
    """Define objeto de teste e caso de teste para Post"""
    def setUp(self):
        self.tester = app.test_client(self)
        self.user = {'user': 'Matheus'}


    """Teste API método DELETE no path '/'"""
    def test_get_route_delete_status(self):
        response = self.tester.delete('/')
        self.assertEqual(response.status_code, 200)

    def test_get_route_delete_assertin(self):
        response = self.tester.delete('/')
        self.assertIn('b\'{"sucess":true}\\n\'', str(response.data))


    """Teste API método POST no path </url/view/>. Inserir Url e Usuário na Base de Dados."""
    def test_post_route_view_status(self):
        response = self.tester.post('/http://www.globo.com/noticias/sera-moro-o-proximo-presidente.ghtml/view/',
                                    data = self.user)
        self.assertEqual(response.status_code, 201)

    def test_post_route_view_assertin(self):
        response = self.tester.post('/http://www.globo.com/noticias/sera-moro-o-proximo-presidente.ghtml/view/',
                                    data = self.user)
        self.assertIn('{"success":true}', str(response.data))


    """Teste API método GET no path </url/similar/>. Resposta 10 Url recomendadas"""
    def test_get_route_similar_status(self):
        response = self.tester.get('/http://www.globo.com/noticias/sera-moro-o-proximo-presidente.ghtml/similar/')
        self.assertEqual(response.status_code, 200)

    def test_get_route_similar_len_recommendation(self):
        ingest_data()
        result = models.make_recommendation('/http://www.globo.com/noticias/sera-moro-o-proximo-presidente.ghtml')
        self.assertEqual(10, len(result))


if __name__ == '__main__':
    unittest.main()