import requests
import json
import unittest

baseurl = "http://127.0.0.1:5000"


class TestSourceCalls(unittest.TestCase):

    def test_add_source(self):
        url = baseurl + "/sources"
        payload = {"short_hand": "test", "rss": "<no link>"}
        r = requests.post(url, json=payload)
        self.assertTrue(r, "201: item created")

    def test_get_and_delete_source(self):
        source_id = -1
        url = baseurl + "/sources"
        r = (requests.get(url)).json()
        for source in r:
            if source['short_hand'] == "test":
                source_id = source['id']

        if source_id != -1:
            url = baseurl + "/sources/" + str(source_id)
            r = requests.delete(url)
            self.assertTrue(r, "200: Source deleted")
        else:
            return False


class TestArticleCalls(unittest.TestCase):

    def test_add_article(self):
        url = baseurl + "/article"
        payload = {"id": "test_id", "title": "this is a test title", "transcript": "test, test, test", "source_id": "1"}
        r = requests.post(url, json=payload)
        self.assertTrue(r, "201: item created")

    def test_update_article(self):
        url = baseurl + "/update_article"
        payload = {"id": "test_id", "title": "update title", "transcript": "update transcript"}
        r = requests.put(url, json=payload)
        self.assertTrue(r, "200: updated Article")

    def test_article_status(self):
        url = baseurl + "/article/test_id/status"
        payload = {"status": "TESTING"}
        r = requests.put(url, json=payload)
        self.assertTrue(r, "200: updated article")

    def test_article_context(self):
        url = baseurl + "/article/test_id/context"
        payload = {"context": "AAPL"}
        r = requests.put(url, json=payload)
        self.assertTrue(r, "200: updated article")

    def test_get_and_delete_article(self):
        url = baseurl + "/article/test_id"
        r = (requests.get(url)).json()
        if r['status'] == "TESTING":
            url = baseurl + "/article/test_id"
            r = requests.delete(url)
            self.assertTrue(r, "200: Article deleted")
        else:
            return False


class TestSentenceCalls(unittest.TestCase):

    def test_add_sentence(self):
        url = baseurl + "/sentence"
        payload = {"text": "this is a test sentence", "article_id": "1"}
        r = requests.post(url, json=payload)
        self.assertTrue(r, "201: item created")

    def test_find_and_delete_sentence(self):
        url = baseurl + '/sentence/findByStatus'
        payload = {"status": ""}
        r = (requests.get(url, json=payload)).json()
        for item in r:
            if item['text'] == "this is a test sentence":
                url = baseurl + "/sentence/" + item['id']
                print(item[id])
                r = requests.delete(url)
                self.assertTrue(r, "200: sentence deleted")
        return False


class TestCompanyCalls(unittest.TestCase):

    def test_add_company(self):
        url = baseurl + "/company"
        payload = {"stock_code": "TEST", "short_hand": "NOT_REAL_TEST"}
        r = requests.post(url, json=payload)
        self.assertTrue(r, "201: item created")

    def test_get_company(self):
        url = baseurl + "/company/TEST"
        r = (requests.get(url)).json()
        self.assertTrue(r, {"stock_code": "TEST", "short_hand": "NOT_REAL_TEST"})


if __name__ == '__main__':
    unittest.main()