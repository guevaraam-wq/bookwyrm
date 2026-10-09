"""Factory Method pattern for creating reading-history importers."""

from abc import ABC, abstractmethod

from .importer import Importer
from .bookwyrm_import import BookwyrmBooksImporter
from .calibre_import import CalibreImporter
from .goodreads_import import GoodreadsImporter
from .librarything_import import LibrarythingImporter
from .openlibrary_import import OpenLibraryImporter
from .openreads_import import OpenReadsImporter
from .storygraph_import import StorygraphImporter


class ImporterCreator(ABC):
    """Abstract creator defining the factory method."""

    @abstractmethod
    def create_importer(self) -> Importer:
        """Return a concrete importer."""


class GoodreadsCreator(ImporterCreator):
    def create_importer(self) -> Importer:
        return GoodreadsImporter()


class BookwyrmCreator(ImporterCreator):
    def create_importer(self) -> Importer:
        return BookwyrmBooksImporter()


class LibrarythingCreator(ImporterCreator):
    def create_importer(self) -> Importer:
        return LibrarythingImporter()


class StorygraphCreator(ImporterCreator):
    def create_importer(self) -> Importer:
        return StorygraphImporter()


class OpenLibraryCreator(ImporterCreator):
    def create_importer(self) -> Importer:
        return OpenLibraryImporter()


class OpenReadsCreator(ImporterCreator):
    def create_importer(self) -> Importer:
        return OpenReadsImporter()


class CalibreCreator(ImporterCreator):
    def create_importer(self) -> Importer:
        return CalibreImporter()


class ServiceImporterCreator:
    """Choose the appropriate concrete Factory Method creator."""

    CREATORS = {
        "BookWyrm": BookwyrmCreator,
        "LibraryThing": LibrarythingCreator,
        "Storygraph": StorygraphCreator,
        "OpenLibrary": OpenLibraryCreator,
        "OpenReads": OpenReadsCreator,
        "Calibre": CalibreCreator,
        "Goodreads": GoodreadsCreator,
    }

    def __init__(self, source: str | None):
        self.source = source

    def create_importer(self) -> Importer:
        creator_class = self.CREATORS.get(self.source, GoodreadsCreator)
        return creator_class().create_importer()
