# Interaction Diagram: Finish Reading a Book

This interaction diagram expands the `finish` system event from the Finish Reading SSD and shows the objects inside BookWyrm that collaborate to complete the operation.

```mermaid
sequenceDiagram
    actor Reader
    participant RS as ReadingStatus
    participant Shelf as Shelf
    participant Edition as Edition
    participant SB as ShelfBook
    participant RT as ReadThrough

    Reader->>RS: post(request, "finish", book_id)

    RS->>Shelf: get(identifier=READ_FINISHED, user)
    Shelf-->>RS: desired_shelf

    RS->>Edition: get(id=book_id)
    Edition-->>RS: book

    alt Book is on a different reading-status shelf
        RS->>SB: delete()
        SB-->>RS: deleted
    else Book is already on finished shelf
        RS-->>Reader: redirect
    end

    RS->>SB: create(book, desired_shelf, user)
    SB-->>RS: ShelfBook

    RS->>RS: update_readthrough_on_shelve(...)

    loop Existing active readthroughs
        RS->>RT: save(is_active=False)
        RT-->>RS: saved
    end

    RS->>RT: set finish_date
    RS->>RT: save()
    RT->>RT: set is_active=False
    RT-->>RS: saved

    opt User selected "post status"
        RS->>RS: handle_reading_status(...)
    end

    RS-->>Reader: redirect
```