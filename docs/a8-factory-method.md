# Factory Method Pattern

Implemented in bookwyrm/importers/importer_factory.py.

ImporterCreator defines the factory method. Concrete creators return the appropriate importer. ServiceImporterCreator selects the creator based on the import source.

```mermaid
classDiagram
    class ImporterCreator {
        <<abstract>>
        +create_importer()
    }
    class GoodreadsCreator {
        +create_importer()
    }
    class BookwyrmCreator {
        +create_importer()
    }
    class LibrarythingCreator {
        +create_importer()
    }
    class ServiceImporterCreator {
        +create_importer()
    }
    class Importer
    class GoodreadsImporter
    class LibrarythingImporter

    ImporterCreator <|-- GoodreadsCreator
    ImporterCreator <|-- BookwyrmCreator
    ImporterCreator <|-- LibrarythingCreator
    ServiceImporterCreator ..> ImporterCreator : selects
    GoodreadsCreator ..> GoodreadsImporter : creates
    LibrarythingCreator ..> LibrarythingImporter : creates
    GoodreadsImporter --|> Importer
    LibrarythingImporter --|> Importer
```
