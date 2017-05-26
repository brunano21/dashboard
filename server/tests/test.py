import unittest
import tempfile
import sys
import os
import json
sys.path.append('../')
import server


class BasicTests(unittest.TestCase):

    def setUp(self):
        self.db_fd, server.app.config["DATABASE"] = tempfile.mkstemp()
        server.app.config["TESTING"] = True
        server.app.config["WTF_CSRF_ENABLED"] = False
        server.app.config["DEBUG"] = False
        with server.app.app_context():
            server.dbmgr = server.init_db(
                server.app.config['DATABASE'], server.app.config["TESTING"])
        self.app = server.app.test_client()

        self.assertEqual(server.app.debug, False)

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(server.app.config['DATABASE'])

    def test_home_page(self):
        r = self.app.get('/')
        assert server.app.config["MAPS_KEY"] in r.data
        assert r.status_code == 200

    def test_not_existing_page(self):
        r = self.app.get('/noteExistingPage')
        assert r.status_code == 404

    def test_get_all_downloads(self):
        r = self.app.post("/new", data=json.dumps(dict(
            lng='92.7188302878112', lat='51.907510530508',
            app_id="ANDROID_MATE", downloaded_at="1494465907288.0")),
            content_type="application/json")
        assert r.data == "OK"
        r = self.app.get("/getAllDownloads")
        assert r.status_code == 200
        json_res = json.loads(r.data)
        assert json_res["status"] == "OK"
        assert len(json_res["results"]) is not 0

    def test_post_new_data(self):
        r = self.app.post("/new", data=json.dumps(dict(
            lng='92.7188302878112', lat='51.907510530508',
            app_id="ANDROID_MATE", downloaded_at="1494465907288.0")),
            content_type="application/json")
        assert r.data == "OK"
        db_data = server.dbmgr.get_all_downloads()
        assert len(db_data) is not 0

    def test_post_new_data_not_valid(self):
        r = self.app.post("/new", data=json.dumps(dict(
            lng='-33.491641', lat='51.931076',
            app_id="ANDROID_MATE", downloaded_at="1494465907288.0")),
            content_type="application/json")
        assert r.data == "NO"
        db_data = server.dbmgr.get_all_downloads()
        assert len(db_data) is 0

    def test_get_by_country(self):
        r = self.app.post("/new", data=json.dumps(dict(
            lng='92.7188302878112', lat='51.907510530508',
            app_id="ANDROID_MATE", downloaded_at="1494465907288.0")),
            content_type="application/json")
        assert r.data == "OK"
        r = self.app.get("/stats/byCountry")
        assert r.status_code == 200
        json_res = json.loads(r.data)
        assert json_res["status"] == "OK"
        assert len(json_res["results"]) is not 0

    def test_get_data_by_time(self):
        r = self.app.post("/new", data=json.dumps(dict(
            lng='92.7188302878112', lat='51.907510530508',
            app_id="ANDROID_MATE", downloaded_at="1494465907288.0")),
            content_type="application/json")
        assert r.data == "OK"
        r = self.app.get("/stats/byTime")
        json_res = json.loads(r.data)
        assert json_res["status"] == "OK"
        assert len(json_res["results"]) is not 0

    def test_get_history(self):
        r = self.app.post("/new", data=json.dumps(dict(
            lng='92.7188302878112', lat='51.907510530508',
            app_id="ANDROID_MATE", downloaded_at="1494465907288.0")),
            content_type="application/json")
        assert r.data == "OK"
        r = self.app.get("/stats/history")
        json_res = json.loads(r.data)
        assert json_res["status"] == "OK"
        assert len(json_res["results"]) is not 0


if __name__ == "__main__":
    unittest.main()
