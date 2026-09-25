sequenceDiagram
    actor Reader
    participant S as BookWyrm

    Reader->>S: importReadingHistory(importFile)
    S-->>Reader: import accepted