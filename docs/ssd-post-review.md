sequenceDiagram
    actor Reader
    participant S as BookWyrm

    Reader->>S: postReview(bookId, rating, reviewText)
    S-->>Reader: review posted