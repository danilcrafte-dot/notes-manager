"""Модульні тести основних сценаріїв."""
import logging
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from notes.manager import NoteManager
from notes.storage import JsonStorage


class NoteManagerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.tmp.close()
        os.remove(self.tmp.name)
        self.path = self.tmp.name
        self.m = NoteManager(JsonStorage(self.path), logging.getLogger("test"))

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_add_and_get(self):
        n = self.m.add("Купити хліб", "Сьогодні", "Побут", ["Їжа", "їжа"])
        self.assertEqual(self.m.get(n.id).title, "Купити хліб")
        self.assertEqual(n.tags, ["їжа"])

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            self.m.add("  ", "x")

    def test_update_and_delete(self):
        n = self.m.add("A", "b")
        self.m.update(n.id, title="B")
        self.assertEqual(self.m.get(n.id).title, "B")
        self.m.delete(n.id)
        with self.assertRaises(KeyError):
            self.m.get(n.id)

    def test_search_and_filter(self):
        self.m.add("Python", "уроки", "Навчання", ["код"])
        self.m.add("Ліки", "купити", "Здоров'я")
        self.assertEqual(len(self.m.search("python")), 1)
        self.assertEqual(len(self.m.search("код")), 1)
        self.assertEqual(len(self.m.list_all(category="навчання")), 1)
        self.assertEqual(len(self.m.list_all(tag="код")), 1)

    def test_persistence(self):
        self.m.add("Збережено", "так")
        m2 = NoteManager(JsonStorage(self.path), logging.getLogger("test"))
        self.assertEqual(len(m2.notes), 1)


if __name__ == "__main__":
    unittest.main()
