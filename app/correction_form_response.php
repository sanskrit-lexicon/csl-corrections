<?php
/* correction_form_response.php
 * Receives one submission from correction_form.php (posted into a hidden
 * iframe) and appends it as one tab-separated line to
 * correction_response/cfr-<YYYYMMDD>.tsv, which the csl-corrections nightly
 * cron fetches.
 *
 * H3885: this used to fopen/fwrite unchecked, so a full disk, a bad
 * permission or a lost lock silently discarded a correction while the form
 * still showed "thank you". It now locks, checks every step, caps field
 * length, and answers with a machine-readable status the parent page reads.
 */

// The form is served from the Cologne site; only that origin needs access.
header("Access-Control-Allow-Origin: https://sanskrit-lexicon.uni-koeln.de");
header("Vary: Origin");
header("Content-Type: text/html; charset=utf-8");

const CFR_MAX_FIELD_LEN = 2000;

function cfr_fail($message) {
 http_response_code(500);
 echo '<!DOCTYPE html><html><body>';
 echo '<div id="cfr-status" data-cfr-status="error">';
 echo 'ERROR: your correction was NOT saved. ' . htmlspecialchars($message, ENT_QUOTES, 'UTF-8');
 echo '</div>';
 echo '<script>if(window.parent!==window){window.parent.postMessage({cfr:"error"},"*");}</script>';
 echo '</body></html>';
 exit(1);
}

$outar = array();
// date-time stamp: 3/18/2014 14:48:54
$outar[] = date("m/d/Y H:i:s");
$columns = array("entry_dict","entry_L","entry_hw","entry_old",
 "entry_new","entry_comment","entry_email");
foreach ($columns as $postkey) {
 if (isset($_POST[$postkey]) && is_string($_POST[$postkey])) {
  $val = $_POST[$postkey];
  // Alter newline and tab
  $val = preg_replace("|[\n\r]+|", " LB ", $val);
  $val = preg_replace("|[\t]|", "  ", $val);
  // Cap each field: one line of the TSV must stay one manageable record.
  $val = mb_substr($val, 0, CFR_MAX_FIELD_LEN, 'UTF-8');
 } else {
  $val = "";
 }
 $outar[] = $val;
}

$out = join("\t", $outar);

// Append 'out' to correction_response/cfr-yyyymmdd.tsv
$dir = "correction_response";
if (!is_dir($dir) && !@mkdir($dir, 0775, true) && !is_dir($dir)) {
 cfr_fail("server storage is unavailable.");
}
$filedate = date("Ymd");
$fileout = "$dir/cfr-$filedate.tsv";

$fp = @fopen($fileout, "a");
if ($fp === false) {
 error_log("correction_form_response: cannot open $fileout for append");
 cfr_fail("server could not open the corrections file.");
}
if (!flock($fp, LOCK_EX)) {
 fclose($fp);
 error_log("correction_form_response: cannot lock $fileout");
 cfr_fail("server could not lock the corrections file.");
}
$line = "$out\n";
$written = fwrite($fp, $line);
$flushed = fflush($fp);
flock($fp, LOCK_UN);
fclose($fp);

if ($written === false || $written !== strlen($line) || $flushed === false) {
 error_log("correction_form_response: short write to $fileout ("
  . var_export($written, true) . " of " . strlen($line) . " bytes)");
 cfr_fail("server could not write the correction to disk.");
}

/* 04-04-2026 do NOT revise cfr.tsv on Cologne server */

http_response_code(200);
echo '<!DOCTYPE html><html><body>';
echo '<div id="cfr-status" data-cfr-status="ok">OK</div>';
echo '<script>if(window.parent!==window){window.parent.postMessage({cfr:"ok"},"*");}</script>';
echo '</body></html>';
