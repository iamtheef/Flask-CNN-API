import unittest
from config import app

### it's actually used ###
import index as api
### --- ###
import utils
import json


class TestApi(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config['ENV'] = 'STAGING'

    def test_endpoints(self):
        headers = {"Content-Type": "application/json"}

        response = self.app.get('/')
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json['message'], 'hello all possible worlds --- -- - ***')

        # testing the prediction endpoint
        payload = json.dumps({
            "isLink": True,
            "input": "http://www.reportingday.com/wp-content/uploads/2018/06/Cat-Sleeping-Pics.jpg"
        })
        response = self.app.post('/predict/', data=payload, headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['message'], 'cat')

        payload = json.dumps({
            "isLink": True,
            "input": "http://images.hellogiggles.com/uploads/2017/02/04230309/happy-dog.jpg"
        })
        response = self.app.post('/predict/', data=payload, headers=headers)
        self.assertEqual(200, response.status_code)
        self.assertTrue(response.json['success'])
        self.assertEqual(response.json['message'], 'dog')

        payload = json.dumps({
            "isLink": True,
            "input": "http://images.hellogiggles.com/uploads/2017"
        })
        response = self.app.post('/predict/', data=payload, headers=headers)
        self.assertEqual(204, response.status_code)

        payload = json.dumps({
            "isLink": False,
            "input": "http://images.hellogiggles.com/uploads/2017"
        })
        response = self.app.post('/predict/', data=payload, headers=headers)
        self.assertEqual(404, response.status_code)

        # testing upload endpoint
        file = "assets/test_images/2.jpg"
        payload = {
            'image': (open(file, 'rb'), file)
        }
        response = self.app.post('/upload/', data=payload)
        self.assertEqual(200, response.status_code)

        payload = {
            'image': (open(file, 'rb'), 'file')
        }
        response = self.app.post('/upload/', data=payload)
        self.assertEqual(400, response.status_code)

    def test_utils(self):
        app.config['ENV'] = 'TESTING'
        # allowing files types
        self.assertTrue(utils.allowed_file('filename.jpg'))
        self.assertFalse(utils.allowed_file('filename.gif'))
        self.assertTrue(utils.allowed_file('filename.png'))
        self.assertFalse(utils.allowed_file('filename.pdf'))

        # search file function
        self.assertTrue(utils.find_file('1.jpg'))
        self.assertTrue(utils.find_file('2.jpg'))
        self.assertFalse(utils.find_file('3.jpg'))

        # download function
        file = utils._download('http://www.reportingday.com/wp-content/uploads/2018/06/Cat-Sleeping-Pics.jpg')
        self.assertTrue(file['success'])
        self.assertEqual(file['name'], file['name'])

        # remove function
        self.assertTrue(utils.remove_file(file['name']))
        self.assertFalse(utils.remove_file('randomanme.jpg'))

        # predict function
        self.assertEqual(utils.make_prediction('1.jpg'), 'dog')
        self.assertEqual(utils.make_prediction('2.jpg'), 'cat')
        self.assertRaises(FileNotFoundError, utils.make_prediction, 'asd.jpg')


if __name__ == '__main__':
    unittest.main()