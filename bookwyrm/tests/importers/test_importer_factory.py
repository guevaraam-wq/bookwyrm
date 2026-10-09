"""Tests for importer creation."""

from django.test import SimpleTestCase

from bookwyrm.importers import (
    BookwyrmBooksImporter,
    CalibreImporter,
    GoodreadsImporter,
    LibrarythingImporter,
    OpenLibraryImporter,
    OpenReadsImporter,
    StorygraphImporter,
)
from bookwyrm.importers.importer_factory import ServiceImporterCreator


class ImporterFactoryTests(SimpleTestCase):
    """Verify that each service creates the correct importer."""

    def test_supported_services(self):
        services = {
            "BookWyrm": BookwyrmBooksImporter,
            "LibraryThing": LibrarythingImporter,
            "Storygraph": StorygraphImporter,
            "OpenLibrary": OpenLibraryImporter,
            "OpenReads": OpenReadsImporter,
            "Calibre": CalibreImporter,
            "Goodreads": GoodreadsImporter,
        }

        for source, expected_class in services.items():
            with self.subTest(source=source):
                importer = ServiceImporterCreator(source).create_importer()
                self.assertIsInstance(importer, expected_class)

    def test_unknown_service_defaults_to_goodreads(self):
        importer = ServiceImporterCreator("Unknown").create_importer()
        self.assertIsInstance(importer, GoodreadsImporter)

    def test_missing_service_defaults_to_goodreads(self):
        importer = ServiceImporterCreator(None).create_importer()
        self.assertIsInstance(importer, GoodreadsImporter)
