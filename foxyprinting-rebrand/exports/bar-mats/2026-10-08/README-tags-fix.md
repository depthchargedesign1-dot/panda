# Duplicate text boxes on the new bar mats: tag fix (8 Oct 2026)

Owner: "The bar mats have duplicated text options again" (e.g. personalised-club-bar-mat-red-and-white).
Cause: the 54 new mats carry the theme's own personalisation boxes (foxy.personalise_fields) AND the old mats' tags
"Bar Mat" / "Personalised Bar Mat" / "Football Bar Mats", which the Infinite Options app set for the old milan mats
appears to key on, so the app added its own text boxes too.
Fix:
- Collections widened (OR rules) so nothing drops out: bar-mats = TAG "Bar Mat" OR "bar-mat-2026";
  personalised-bar-mats = "Personalised Bar Mat" OR "personalised-bar-mat-2026";
  football-bar-mats = "Football Bar Mats" OR "football-bar-mat-2026". Counts unchanged after: 137 / 95 / 49.
- On the 54 new mats (created.json): removed "Bar Mat", "Personalised Bar Mat", "Football Bar Mats";
  added "bar-mat-2026" (all), "personalised-bar-mat-2026" (44), "football-bar-mat-2026" (17).
- Old milan/club mats untouched (they have no theme fields and rely on the app).
If the duplicate boxes still show, the app set is attached by collection, not tag: in Infinite Options, exclude the
new mats (tag bar-mat-2026) from that set.
RULE for new bar mats: never give them the tags "Bar Mat" / "Personalised Bar Mat" / "Football Bar Mats".
