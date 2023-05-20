from flask import Flask, request, render_template
from flask import jsonify
import vobject
import json
from pymongo import MongoClient
import pymongo
import certifi
from bson import json_util
from flask import Response
from bson import json_util
from flask_cors import CORS
import os
import requests


import pytest
from flask import Flask
from main import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, World!" in response.data



def test_addition():
    assert 2 + 2 == 4