sequenceDiagram
    actor Reader
    participant S as BookWyrm

    Reader->>S: finishReading(bookId, startDate, finishDate)
    S-->>Reader: reading activity updated