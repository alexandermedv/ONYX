# ONYX Collection Book renderer

Local ReportLab + Pillow + pypdf + Poppler. No service, model, GPU, network, global installation or existing delivery-pipeline changes.

From repository root, with those dependencies installed:

```powershell
python "13 Production/Templates/Collection_Book/render_collection_book.py" --data "13 Production/Templates/Collection_Book/example_data/P02_BUSINESS_COLLECTION_BOOK_v1.json" --output "13 Production/Samples/P02_Business_Collection_Book_v1_rebuild"
```

On this workstation replace `python` with `& 'C:/Users/ME/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe'`. `pdftoppm` is on PATH; otherwise pass `--poppler` with its executable path. No extra dependencies were installed.

```powershell
python "13 Production/Templates/Collection_Book/test_renderer.py"
```

Planner/privacy unit checks cover 1, 10 and 20 photos. The actual P02 Signature book additionally passes end-to-end PDF rendering checks. Previews are 1350 px JPEGs rendered directly from the PDF. Premium/Preview PDF output has not been visually certified.

See [data contract](ONYX_COLLECTION_BOOK_TEMPLATE.md), [production guide](COLLECTION_BOOK_PRODUCTION_GUIDE.md), [standard](../../Product_Standards/ONYX_COLLECTION_BOOK_STANDARD.md), and [sample](../../Samples/P02_Business_Collection_Book_v1/README.md). Do not send internal manifests, source_data or reports to clients.
