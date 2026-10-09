// Foxy Printing - 1 Prepare cut file (Adobe Illustrator script)
// Run with the artwork open: File > Scripts > Other Script... (or put it in Illustrator's Presets/Scripts folder).
//
// What it does, ready for the Intec ColorCut Pro plug-in:
//   1. Puts every RED line (cut) and BLUE line (crease) on a layer called "CUT", on top
//      (an old "Cut lines" layer is renamed CUT).
//   2. Puts everything else on a layer called "Artwork".
//   3. Asks for the customer's name and swaps it into the sample name (e.g. "Ava") in the live text.
//   4. Tells you to click ColorCut Pro > ADD PageMARKs & BarCode, then run "Foxy - 2 Save print PDF".
// Line colours follow Intec's ColorCut Pro guide: Red (RGB 255,0,0 / CMYK 2,98,95,0) = Cut,
// Blue (RGB 0,0,255 / CMYK 91,80,1,0) = Crease. Magenta (RGB 255,0,255 / CMYK 0,100,0,0, used on
// face mask files from mask_cutline.py) also counts as Cut. Close matches count too.
#target illustrator

(function () {
    if (app.documents.length === 0) { alert('Open the artwork file first.'); return; }
    var doc = app.activeDocument;

    function rgbOf(c) {
        if (!c) return null;
        switch (c.typename) {
            case 'RGBColor': return [c.red, c.green, c.blue];
            case 'CMYKColor':
                return [255 * (1 - c.cyan / 100) * (1 - c.black / 100),
                        255 * (1 - c.magenta / 100) * (1 - c.black / 100),
                        255 * (1 - c.yellow / 100) * (1 - c.black / 100)];
            case 'SpotColor': return rgbOf(c.spot.color);
            case 'GrayColor': var g = 255 * (1 - c.gray / 100); return [g, g, g];
        }
        return null;
    }
    function lineKind(item) {
        if (!item.stroked) return null;
        var rgb = rgbOf(item.strokeColor);
        if (!rgb) return null;
        var r = rgb[0], g = rgb[1], b = rgb[2];
        if (r > 180 && g < 90 && b < 90) return 'cut';
        if (r > 180 && g < 90 && b > 180) return 'cut';   // magenta (face mask cut files)
        if (b > 150 && r < 90 && g < 110) return 'crease';
        return null;
    }
    function getLayer(name) {
        try { return doc.layers.getByName(name); } catch (e) { var l = doc.layers.add(); l.name = name; return l; }
    }

    // Unlock everything so items can be moved.
    for (var i = 0; i < doc.layers.length; i++) { doc.layers[i].locked = false; doc.layers[i].visible = true; }

    // Owner's rule (5 Oct 2026): cut lines live on their own layer called CUT.
    var cutLayer = null;
    try { cutLayer = doc.layers.getByName('CUT'); } catch (e) {}
    if (!cutLayer) { try { cutLayer = doc.layers.getByName('Cut lines'); cutLayer.name = 'CUT'; } catch (e) {} }
    if (!cutLayer) cutLayer = getLayer('CUT');
    var artLayer = null;
    for (var j = 0; j < doc.layers.length; j++) {
        if (doc.layers[j] !== cutLayer && doc.layers[j].name.indexOf('ColorCut') === -1) { artLayer = doc.layers[j]; break; }
    }
    if (!artLayer) { artLayer = doc.layers.add(); }
    artLayer.name = 'Artwork';
    cutLayer.zOrder(ZOrderMethod.BRINGTOFRONT);

    // Move cut/crease paths (collect first: moving changes the collection).
    var toMove = [];
    for (var k = 0; k < doc.pathItems.length; k++) {
        var p = doc.pathItems[k];
        if (p.layer === cutLayer) continue;
        if (lineKind(p)) toMove.push(p);
    }
    var cuts = 0, creases = 0;
    for (var m = 0; m < toMove.length; m++) {
        var kind = lineKind(toMove[m]);
        toMove[m].filled = false;
        toMove[m].move(cutLayer, ElementPlacement.PLACEATEND);
        if (kind === 'cut') cuts++; else creases++;
    }
    // Anything else left on other layers goes to Artwork.
    for (var n = doc.layers.length - 1; n >= 0; n--) {
        var L = doc.layers[n];
        if (L === cutLayer || L === artLayer || L.name.indexOf('ColorCut') !== -1) continue;
        for (var q = L.pageItems.length - 1; q >= 0; q--) L.pageItems[q].move(artLayer, ElementPlacement.PLACEATBEGINNING);
        if (L.pageItems.length === 0 && L.layers.length === 0) L.remove();
    }

    // Customer name.
    var sample = 'Ava';
    var name = prompt('Customer name to print (leave as it is to keep the sample name):', sample, 'Foxy Printing');
    var swapped = 0;
    if (name && name !== sample) {
        for (var t = 0; t < doc.textFrames.length; t++) {
            var tf = doc.textFrames[t];
            if (tf.contents.indexOf(sample) !== -1) { tf.contents = tf.contents.split(sample).join(name); swapped++; }
        }
    }

    alert('Ready for ColorCut Pro.\n\n' +
          'CUT layer - cut lines (red/magenta): ' + cuts + '\nCrease lines (blue): ' + creases + '\nName changed in ' + swapped + ' place(s).\n\n' +
          'Next:\n1. ColorCut Pro > ADD PageMARKs & BarCode (Landscape for SRA3 boxes).\n' +
          '2. Run "Foxy - 2 Save print PDF" to save the file to print.\n' +
          '3. At the cutter: scan the barcode, Red = Cut, Blue = Crease.');
})();
