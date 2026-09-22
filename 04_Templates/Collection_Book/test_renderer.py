import importlib.util
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('book', Path(__file__).with_name('render_collection_book.py'))
book = importlib.util.module_from_spec(spec)
spec.loader.exec_module(book)

class BookTests(unittest.TestCase):
    def test_tiers_cover_every_photo_once(self):
        for count,pages in ((1,7),(10,15),(20,16)):
            layout=book.plan(count)
            self.assertEqual(sorted(i for _,ids in layout for i in ids),list(range(count)))
            self.assertEqual(len(layout)+6,pages)

    def test_unsupported_counts_fail(self):
        for count in (0,2,9,11,21):
            with self.assertRaises(ValueError): book.plan(count)

    def test_internal_copy_is_detected(self):
        for value in ('P02','BUS_01','FLUX','LoRA','C:/private/photo','photo.png','AI pipeline'):
            self.assertIsNotNone(book.FORBIDDEN.search(value))
        self.assertIsNone(book.FORBIDDEN.search('Business Collection'))

if __name__=='__main__': unittest.main()
