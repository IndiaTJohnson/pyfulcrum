#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from io import BytesIO
import zipfile

from . import BaseTestCase
from ..formats import FORMATS
from ..models import Record, Project


class FormatTestCase(BaseTestCase):

    def test_format_json(self):

        self.api_manager.forms.list(cached=False)
        self.api_manager.records.list(cached=False)
        self.api_manager.photos.list(cached=False)

        r = self.api_manager.records.get('4e1c33ad-5496-4818-826f-504e66239b4d')
        f = FORMATS['json']
        out = json.loads(f(r, self._storage, multiple=False))
        self.assertTrue(isinstance(out, dict), out)
        self.assertEqual(out['id'], r.id)
        self.assertEqual(out.get('class'), 'Record')
        r = self.api_manager.records.list()
        out = json.loads(f(r, self._storage, multiple=True))
        self.assertTrue(isinstance(out, list))
        self.assertEqual(out[0].get('class'), 'Record')
        self.assertEqual(out[0]['id'], r[0].id)


    def test_format_raw(self):

        self.api_manager.forms.list(cached=False)
        self.api_manager.records.list(cached=False)
        self.api_manager.photos.list(cached=False)

        r = self.api_manager.records.get('4e1c33ad-5496-4818-826f-504e66239b4d')
        f = FORMATS['raw']
        out = json.loads(f(r, self._storage, multiple=False))
        self.assertTrue(isinstance(out, dict), out)
        self.assertEqual(out['id'], r.id)
        r = self.api_manager.records.list()
        out = json.loads(f(r, self._storage, multiple=True))
        self.assertTrue(isinstance(out, list))
        self.assertEqual(out[0]['id'], r[0].id)

    def test_format_geojson(self):

        self.api_manager.forms.list(cached=False)
        self.api_manager.records.list(cached=False)
        self.api_manager.photos.list(cached=False)

        r = self.api_manager.records.get('4e1c33ad-5496-4818-826f-504e66239b4d')
        f = FORMATS['geojson']
        out = json.loads(f(r, self._storage, multiple=False))
        self.assertTrue(isinstance(out, dict), out)
        self.assertEqual(out.get('type'), 'Feature')
        self.assertEqual(out['properties']['id'], r.id)
        r = self.api_manager.records.list()
        out = json.loads(f(r, self._storage, multiple=True))
        self.assertTrue(isinstance(out, dict))
        self.assertTrue(isinstance(out.get('features'), list))
        self.assertEqual(out.get('type'), 'FeatureCollection')
        self.assertEqual(out['features'][0].get('type'), 'Feature')
        self.assertEqual(out['features'][0]['properties']['id'], r[0].id)

    def test_format_shapefile(self):
        
        self.api_manager.forms.list(cached=False)
        self.api_manager.records.list(cached=False)
        self.api_manager.photos.list(cached=False)

        r = self.api_manager.records.get('4e1c33ad-5496-4818-826f-504e66239b4d')
        f = FORMATS['shapefile']
        out = BytesIO(bytes(f(r, self._storage, multiple=False)))
        zf = zipfile.ZipFile(out, mode='r')
        names = zf.namelist()
        self.assertEqual(set(names), set(['records.shp', 'records.dbf', 'records.prj', 'records.shx']))


    def test_format_str(self):
        self.api_manager.forms.list(cached=False)
        self.api_manager.records.list(cached=False)
        self.api_manager.photos.list(cached=False)
        r = self.api_manager.records.get('4e1c33ad-5496-4818-826f-504e66239b4d')
        f = FORMATS['str']
        out = f(r, self._storage, multiple=False)
        self.assertTrue(isinstance(out, str), out.__class__)

        self.assertTrue('Record: id=4e1c33ad-5496-4818-826f-504e66239b4d ' in out)
        r = self.api_manager.records.list()
        out = f(r, self._storage, multiple=True)
        self.assertTrue('Record: id=4e1c33ad-5496-4818-826f-504e66239b4d ' in out)

    def test_format_kml(self):
    
        self.api_manager.forms.list(cached=False)
        self.api_manager.records.list(cached=False)
        self.api_manager.photos.list(cached=False)

        r = self.api_manager.records.get('4e1c33ad-5496-4818-826f-504e66239b4d')
        f = FORMATS['kml']
        out = BytesIO(bytes(f(r, self._storage, multiple=False)))
        self.assertEqual(out.read(5), b'<?xml')
