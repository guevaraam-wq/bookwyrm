classDiagram

    class Reader {
        username
        displayName
    }

    class Book {
        title
        publicationDate
    }

    class Author {
        name
    }

    class Shelf {
        name
    }

    class Review {
        rating
        reviewText
    }

    class ReadingActivity {
        status
        startDate
        finishDate
    }
    class ReadingImport{
        status
    }
    class Notification{
        message
    }

    Reader "1" -- "0..*" Shelf : owns
    Shelf "0..*" -- "0..*" Book : contains
    Reader "1" -- "0..*" Review : writes
    Review "0..*" -- "1" Book : is about
    Author "0..*" -- "0..*" Book : writes
    Reader "1" -- "0..*" ReadingActivity : has
    ReadingActivity "0..*" -- "1" Book : involves
        Reader "1" -- "0..*" ReadingImport : starts
    ReadingImport "0..*" -- "0..*" Book : includes
    Reader "1" -- "0..*" Notification : receives