import os
import pytest
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from flask_app.app import allowed_file, save_file

@pytest.mark.parametrize('filename, expected', [
    ('image.jpg', True),
    ('image.png', True),
    ('image.jpeg', True),
    ('image.gif', True),
    ('image.bmp', False),
    ('image', False),
    ('image.', False),
    ('.jpg', True),
    ('', False)
])

def test_allowed_file(filename, expected):
    assert allowed_file(filename) == expected

def test_save_file(mocker):
    mock_file = mocker.Mock()
    mock_file.filename = 'image.jpg'
    mock_save = mocker.patch.object(mock_file, 'save')
    mock_join = mocker.patch('os.path.join',return_value='image/image.jpg')
    filepath, filename = save_file(mock_file)
    mock_save.assert_called_once_with('image/image.jpg')
    assert filepath == 'image/image.jpg'
    assert filename == 'image.jpg'