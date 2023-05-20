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

def test_addition():
    assert 2 + 2 == 4