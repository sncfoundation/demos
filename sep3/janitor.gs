/**
 * SheetsOperator janitor — the one thing the external controller cannot do.
 *
 * The SheetsOperator controller owns desired state and reconciles cell values, backgrounds,
 * notes and embedded charts through the Sheets API. But floating objects inserted *over*
 * the grid — Insert -> Image -> "Image over cells", and Insert -> Drawing — are NOT exposed
 * by Sheets API v4 at all (there is no images/drawings field to read or delete). The only
 * API that can remove an over-cell image is Apps Script, bound to the sheet.
 *
 * So this is a dumb actuator, not a second brain: it holds no desired state, it just deletes
 * floating over-cell images. The controller stays the operator; this covers the object class
 * Google withholds from remote callers (think of it as a node-local agent).
 *
 * Install (one-time, on the managed sheet):
 *   1. Extensions -> Apps Script, paste this file.
 *   2. Run clean() once and authorize it.
 *   3. Triggers (clock icon) -> Add Trigger -> clean, Time-driven, Minutes timer, every minute.
 *
 * Note: Apps Script exposes over-cell images via getImages(); standalone "drawings" are not
 * removable from script. Images are the practical vandalism vector, so this covers the case.
 */
function clean() {
  var ss = SpreadsheetApp.getActive();
  var removed = 0;
  ss.getSheets().forEach(function (sh) {
    sh.getImages().forEach(function (img) { img.remove(); removed++; });
  });
  if (removed) Logger.log('janitor: removed %s over-cell image(s)', removed);
}
