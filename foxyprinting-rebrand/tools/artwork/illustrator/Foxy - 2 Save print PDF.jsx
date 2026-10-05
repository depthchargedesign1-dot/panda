// Foxy Printing - 2 Save print PDF (Adobe Illustrator script)
// Run AFTER ColorCut Pro > ADD PageMARKs & BarCode.
// Hides the "CUT" layer, saves a print-ready PDF next to the file as "<name> - PRINT.pdf"
// (artwork + PageMARKs + barcode, no cut lines), saves the .ai with the ColorCut job, then shows the cut lines again.
#target illustrator

(function () {
    if (app.documents.length === 0) { alert('Open the artwork file first.'); return; }
    var doc = app.activeDocument;
    var cut = null;
    try { cut = doc.layers.getByName('CUT'); } catch (e) {}
    if (!cut) { try { cut = doc.layers.getByName('Cut lines'); } catch (e) {} }
    if (!cut) { alert('No "CUT" layer. Run "Foxy - 1 Prepare cut file" first.'); return; }

    var hasMarks = false;
    for (var i = 0; i < doc.layers.length; i++) {
        if (doc.layers[i].name.toLowerCase().indexOf('colorcut') !== -1) hasMarks = true;
    }
    if (!hasMarks && !confirm('I can\'t see a ColorCut PageMARKs layer yet.\nDid you run ColorCut Pro > ADD PageMARKs & BarCode?\n\nSave the print PDF anyway?')) return;

    var folder = doc.path && doc.path.fsName ? doc.path : Folder.desktop;
    var base = doc.name.replace(/\.[^.]+$/, '');

    // Save the working .ai (keeps the cut layer and the ColorCut job link).
    var aiFile = new File(folder + '/' + base + '.ai');
    doc.saveAs(aiFile, new IllustratorSaveOptions());

    var cutName = cut.name;
    cut.visible = false;
    var opts = new PDFSaveOptions();
    try { opts.pDFPreset = '[High Quality Print]'; } catch (e) {}
    opts.preserveEditability = false;
    opts.viewAfterSaving = false;
    var pdfFile = new File(folder + '/' + base + ' - PRINT.pdf');
    doc.saveAs(pdfFile, opts);

    // Re-open the .ai so you keep working on the editable file, with the cut lines visible.
    doc.close(SaveOptions.DONOTSAVECHANGES);
    var again = app.open(aiFile);
    try { again.layers.getByName(cutName).visible = true; } catch (e) {}

    alert('Saved:\n' + pdfFile.fsName + '\n(print this - no cut lines)\n\n' + aiFile.fsName + '\n(keep this - cut job file)');
})();
