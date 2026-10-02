# Interaction Diagram: Import Reading History

This interaction diagram shows how BookWyrm handles a reading history CSV import. The `Import` view validates the request, selects the correct importer, creates an import job, and starts the background import process.

```mermaid
sequenceDiagram
    actor Reader
    participant IV as Import
    participant IF as ImportForm
    participant GI as GoodreadsImporter
    participant IJ as ImportJob

    Reader->>IV: post(request)

    IV->>IF: ImportForm(request.POST, request.FILES)
    IF-->>IV: form

    IV->>IF: is_valid()
    IF-->>IV: valid / invalid

    alt Form is invalid
        IV-->>Reader: HttpResponseBadRequest
    else Form is valid
        IV->>GI: GoodreadsImporter()
        GI-->>IV: importer

        IV->>GI: create_job(user, csv_file, options)

        GI->>IJ: objects.create(...)
        IJ-->>GI: job

        loop Each CSV entry
            GI->>GI: create_item(job, index, entry, shelf_override)
        end

        GI-->>IV: job

        IV->>IJ: start_job()
        IJ->>IJ: save(task_id)
        IJ-->>IV: job started

        IV-->>Reader: redirect("/import/{job.id}")
    end
```