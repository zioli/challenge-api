from src.service import loader
from flask import Response, request
from src.service.loader import Content
import pytest
# from werkzeug.datastructures import FileStorage 
# import io

def test_FactoryValidateAWS():
    received = loader.Factory(None, "aws", "any", "any")

    assert type(received) == loader.Aws

def test_FactoryValidateGCP():
    received = loader.Factory(None, "gcp", "any", "any")

    assert type(received) == loader.Gcp

## ita has to be fixed the Response context in order to be able to mock it
# def test_FactoryValidateContent(mocker):

#     mocker.patch("flask.request.files.get", FileStorage(io.BytesIO(b"content")))

#     assert 1 == 1
#     # received = loader.Factory(Response(), "content", "any", "any")

#     # assert type(received) == loader.Content

def test_FactoryValidateTest():
    received = loader.Factory(None, "test", "any", "any")
        
    assert type(received) == loader.Test

def test_ContentException():
    with pytest.raises(Exception) as e:
        content = Content()
    
    assert str(e.value) == "__init__() missing 3 required positional arguments: 'request', 'dababase', and 'table'"


    