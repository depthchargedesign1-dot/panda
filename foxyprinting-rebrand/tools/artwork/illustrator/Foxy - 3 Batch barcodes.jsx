// Foxy Printing - 3 Batch barcodes (Adobe Illustrator script)
// Adds ColorCut Pro PageMARKs + BarCode + Job number to EVERY cut file in a folder, one after another.
//
// For each .svg (or .pdf / .ai) in the folder you pick:
//   1. Opens it and makes sure the cut lines are on a layer called "CUT" (red/magenta = cut, blue = crease).
//   2. Selects the CUT layer and runs your recorded action "Add barcode" (set "Foxy ColorCut"), which clicks
//      File > Add PageMARKs and BarCode (the ColorCut Pro item). The plug-in fills in a NEW unused job number itself
//      (Intec FB550 guide, section 7.1) - just press Enter/OK when its box appears.
//   3. Reads the job number the plug-in printed on the sheet.
//   4. Saves "<name>.ai" (cut job, CUT layer visible) and "<name> - PRINT.pdf" (CUT layer hidden) into a
//      "ColorCut ready" folder, then closes the file.
//   5. Writes "ColorCut job numbers.csv" (file, job number, date) so you can find any job again.
// Files that already have a .ai in "ColorCut ready" are skipped, so re-running never makes duplicate job numbers.
//
// ONE-TIME SETUP (2 minutes), see "HOW TO USE - Batch barcodes.txt".
#target illustrator

(function () {
    var ACTION_SET = 'Foxy ColorCut';
    var ACTION_NAME = 'Add barcode';

    var src = Folder.selectDialog('Pick the folder with the cut files (e.g. mask-cut-files)');
    if (!src) return;
    var outDir = new Folder(src.fsName + '/ColorCut ready');
    if (!outDir.exists) outDir.create();

    // .svg first (keeps the Artwork/CUT layers); fall back to .pdf/.ai when there is no .svg of the same name.
    var all = src.getFiles(function (f) { return f instanceof File && /\.(svg|pdf|ai)$/i.test(f.name) && !/ - PRINT\.pdf$/i.test(f.name); });
    var byBase = {}, order = [];
    var rank = { svg: 0, ai: 1, pdf: 2 };
    for (var i = 0; i < all.length; i++) {
        var nm = decodeURI(all[i].name);
        var base = nm.replace(/\.[^.]+$/, '');
        var ext = nm.replace(/^.*\./, '').toLowerCase();
        if (!byBase.hasOwnProperty(base)) { byBase[base] = all[i]; order.push(base); }
        else if (rank[ext] < rank[decodeURI(byBase[base].name).replace(/^.*\./, '').toLowerCase()]) byBase[base] = all[i];
    }
    order.sort();
    if (!order.length) { alert('No .svg, .pdf or .ai files in that folder.'); return; }
    if (!confirm(order.length + ' file(s) found.\n\nFor each one the ColorCut Pro box will appear with a new job number - press Enter (OK) to accept it.\n\nStart?')) return;

    var log = new File(outDir.fsName + '/ColorCut job numbers.csv');
    var newLog = !log.exists;
    log.encoding = 'UTF-8';
    log.open('a');
    if (newLog) log.writeln('File,Job number,Date');

    var done = 0, skipped = 0, problems = [];
    for (var n = 0; n < order.length; n++) {
        var base = order[n];
        var aiFile = new File(outDir.fsName + '/' + base + '.ai');
        if (aiFile.exists) { skipped++; continue; }
        var doc;
        try { doc = app.open(byBase[base]); } catch (e) { problems.push(base + ': could not open'); continue; }
        try {
            var cut = prepareLayers(doc);
            if (!cut) { problems.push(base + ': no red/magenta cut lines found'); doc.close(SaveOptions.DONOTSAVECHANGES); continue; }
            doc.selection = null;
            doc.activeLayer = cut;
            var before = doc.layers.length;
            try { app.doScript(ACTION_NAME, ACTION_SET, false); }
            catch (e) {
                doc.close(SaveOptions.DONOTSAVECHANGES);
                log.close();
                alert('Could not run the action "' + ACTION_NAME + '" in set "' + ACTION_SET + '".\nDo the one-time setup in "HOW TO USE - Batch barcodes.txt", then run this again.\n\n' + e);
                return;
            }
            var job = findJobNumber(doc);
            if (doc.layers.length === before && job === '') problems.push(base + ': ColorCut layer not added (cancelled?)');

            doc.saveAs(aiFile, new IllustratorSaveOptions());
            var cutLayer = doc.layers.getByName('CUT');
            cutLayer.visible = false;
            var opts = new PDFSaveOptions();
            try { opts.pDFPreset = '[High Quality Print]'; } catch (e2) {}
            opts.preserveEditability = false;
            opts.viewAfterSaving = false;
            doc.saveAs(new File(outDir.fsName + '/' + base + ' - PRINT.pdf'), opts);
            doc.close(SaveOptions.DONOTSAVECHANGES);

            log.writeln('"' + base.replace(/"/g, '""') + '",' + job + ',' + new Date().toDateString());
            done++;
        } catch (e) {
            problems.push(base + ': ' + e);
            try { doc.close(SaveOptions.DONOTSAVECHANGES); } catch (e3) {}
        }
    }
    log.close();
    alert('Batch barcodes finished.\n\nDone: ' + done + '\nSkipped (already done): ' + skipped +
          (problems.length ? '\n\nCheck these:\n' + problems.join('\n') : '') +
          '\n\nFiles and job number list are in:\n' + outDir.fsName);

    // ---- helpers ----
    function rgbOf(c) {
        if (!c) return null;
        switch (c.typename) {
            case 'RGBColor': return [c.red, c.green, c.blue];
            case 'CMYKColor':
                return [255 * (1 - c.cyan / 100) * (1 - c.black / 100),
                        255 * (1 - c.magenta / 100) * (1 - c.black / 100),
                        255 * (1 - c.yellow / 100) * (1 - c.black / 100)];
            case 'SpotColor': return rgbOf(c.spot.color);
        }
        return null;
    }
    function isCutLine(p) {
        if (!p.stroked) return false;
        var c = rgbOf(p.strokeColor);
        if (!c) return false;
        var r = c[0], g = c[1], b = c[2];
        return (r > 180 && g < 90 && b < 90) || (r > 180 && g < 90 && b > 180) || (b > 150 && r < 90 && g < 110);
    }
    // Make sure there is a "CUT" layer holding only the cut/crease lines; returns it (or null if there are none).
    function prepareLayers(d) {
        for (var i = 0; i < d.layers.length; i++) { d.layers[i].locked = false; d.layers[i].visible = true; }
        var cut = null;
        try { cut = d.layers.getByName('CUT'); } catch (e) {}
        if (!cut) { try { cut = d.layers.getByName('Cut lines'); cut.name = 'CUT'; } catch (e) { cut = null; } }
        if (!cut) { cut = d.layers.add(); cut.name = 'CUT'; }
        var move = [];
        for (var k = 0; k < d.pathItems.length; k++) {
            var p = d.pathItems[k];
            if (p.layer !== cut && isCutLine(p)) move.push(p);
        }
        for (var m = 0; m < move.length; m++) { move[m].filled = false; move[m].move(cut, ElementPlacement.PLACEATEND); }
        cut.zOrder(ZOrderMethod.BRINGTOFRONT);
        return cut.pageItems.length ? cut : null;
    }
    // The plug-in adds a layer "ColorCutPro Auto Placement Only" with the job number as text.
    function findJobNumber(d) {
        for (var i = 0; i < d.layers.length; i++) {
            var L = d.layers[i];
            if (L.name.toLowerCase().indexOf('colorcut') === -1) continue;
            for (var t = 0; t < L.textFrames.length; t++) {
                var m = String(L.textFrames[t].contents).match(/\d{1,5}/);
                if (m) return m[0];
            }
        }
        return '';
    }
})();
