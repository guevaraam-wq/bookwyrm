# BookWyrm Logical Architecture

```mermaid
flowchart TD

    UI["Presentation Layer<br/>bookwyrm/templates<br/>bookwyrm/static"]

    VIEWS["Controller / View Layer<br/>bookwyrm/views"]

    FORMS["Form / Input Layer<br/>bookwyrm/forms"]

    SERVICES["Application / Supporting Components<br/>bookwyrm/importers<br/>bookwyrm/connectors<br/>bookwyrm/utils"]

    MODELS["Domain / Data Layer<br/>bookwyrm/models"]

    DB[("Database")]

    EXTERNAL["External Book / Federation Services"]

    UI --> VIEWS

    VIEWS --> FORMS
    VIEWS --> SERVICES
    VIEWS --> MODELS

    FORMS --> MODELS
    SERVICES --> MODELS

    MODELS --> DB

    SERVICES --> EXTERNAL