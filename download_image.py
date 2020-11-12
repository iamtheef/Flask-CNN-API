from pathlib import Path
import requests
import uuid
import os

def _download(url):
    _filename = str(uuid.uuid4())
    try:
        Path(os.path.join('assets/uploads/'+ _filename + '.jpg')).touch()
        myfile = requests.get(url)
        open(os.path.join('assets/uploads/'+ _filename + '.jpg'), 'wb').write(myfile.content)
        return {'success': True, 'name': _filename}
    except:
        os.remove(os.path.join('assets/uploads/'+ _filename + '.jpg'))
        return {'success': False, 'name': None}

        