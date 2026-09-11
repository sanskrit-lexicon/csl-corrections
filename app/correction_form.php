<?php
/* General purpose correction form for Sanskrit-Lexicon.
    Mar 17, 2014
   Accepts some url parameters:
    dict  A dictionary identifier
   Sep 7, 2022. Avoid xss security flaw with $_GET['dict']
   May 3, 2026. Orphus option help
*/
 $dict_default = '?';
 $dict = $dict_default;
 if (isset($_GET['dict'])) {
  $dicta = $_GET['dict'];
  // $payload = '"' . "><svG onLoad=prompt('xss')>";
  // echo($payload); // this executes the javascript prompt
  $dictb = preg_replace('|[^A-Za-z0-9]|','',$dicta);
  if(strlen($dictb) > 8) {
   $dictb = $dict;
  }
  $dict = $dictb;
  }
  
 $lnum_default = '';
 $lnum = $lnum_default;
 if (isset($_GET['lnum'])) {
  $lnuma = $_GET['lnum'];
  $lnumb = preg_replace('|[^A-Za-z0-9]|','',$lnuma);
  if(strlen($lnumb) > 20) {
   $lnumb = $lnum_default;
  }
  $lnum = $lnumb;
 }
 
 $hw_default = '';
 $hw = $hw_default;
 if (isset($_GET['hw'])) {
  $hwa = $_GET['hw'];
  $hwb = preg_replace('|[^A-Za-z0-9]|','',$hwa);
  if(strlen($hwb) > 100) {
   $hwb = $hw_default;
  }
  $hw = $hwb;
 }
 
?>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "//www.w3.org/TR/html4/strict.dtd">
<html>
<head>

<meta http-equiv="Content-type" content="text/html; charset=utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=10; chrome=1;">
<meta name="fragment" content="!">
<base target="_blank">
<title>Sanskrit-Lexicon Correction Form </title>

<!--
<link href='https://docs.google.com/static/forms/client/css/656316836-formview_ltr.css' type='text/css' rel='stylesheet'>
-->
<link href='correction_form.css' type='text/css' rel='stylesheet'>

<style type="text/css">

</style>

<meta name="viewport" content="width=device-width">
<!--
<link href='/static/forms/client/css/1393690164-mobile_formview_ltr.css' type='text/css' rel='stylesheet' media='screen and (max-device-width: 721px)'>
-->

</head>
<!--
<p style="color:red; text-align:center">
The correction form is broken.  
<br/>Please save your correction and resubmit
in a day or two.
</br> We apologize for the inconvenience.  (Nov 5, 2015)
</p>
<hr/>
-->
<body dir="ltr" class="ss-base-body">
<div itemscope itemtype="//schema.org/CreativeWork/FormObject">
<!--
<meta itemprop="name" content="Sanskrit-Lexicon Correction Form ">
<meta itemprop="description" content="Instructions:  //www.sanskrit-lexicon.uni-koeln.de/doc/corrections/help.html">

<meta itemprop="url" content="https://docs.google.com/forms/d/1InNaDMuakzrKpkSXlzVn0ocnD3My2uBMWypUEebrO4c/viewform">
<meta itemprop="embedUrl" content="https://docs.google.com/forms/d/1InNaDMuakzrKpkSXlzVn0ocnD3My2uBMWypUEebrO4c/viewform?embedded=true">
<meta itemprop="faviconUrl" content="https://ssl.gstatic.com/docs/spreadsheets/forms/favicon_jfk2.png">
<a class="ss-edit-link" href="https://docs.google.com/forms/d/1InNaDMuakzrKpkSXlzVn0ocnD3My2uBMWypUEebrO4c/edit">Edit this form</a>

-->

<div class="ss-form-container"><div class="ss-top-of-page">


<div class="ss-form-heading">

<h1 class="ss-form-title" dir="ltr">Sanskrit-Lexicon Correction Form </h1>
<h3>For typographical errors</h3>
<h3 >Next time, 
 <a href="orphushelp/orphushelp.html"  target="OrphusHelp"> <span style="color:red">Try Orphus</span></a></h3>
<div class="ss-form-desc ss-no-ignore-whitespace"> 
<a href="//www.sanskrit-lexicon.uni-koeln.de/doc/corrections/help.html"
 target="CorrectionHelp">Instructions</a>  

</div>

<hr class="ss-email-break" style="display:none;">
<div class="ss-required-asterisk" style="display:none">* Required</div></div></div>

<div class="ss-form">
<div id="cfr_submit_error"
 style="display:none;border:2px solid #b00;background:#fee;color:#900;padding:10px;margin:10px 0;"
 role="alert">
 <strong>Your correction was not saved.</strong>
 The server did not confirm the submission. Nothing has been recorded &mdash;
 please press <em>Submit</em> again, and if it keeps failing write to
 <a href="https://github.com/sanskrit-lexicon/csl-corrections/issues">the csl-corrections issue tracker</a>.
</div>
<script type="text/javascript">
/* H3885: the thank-you page used to appear on any iframe load, including a
   500 and an empty write, so a dropped correction looked accepted. Show it
   only when correction_form_response.php reports success. */
var submitted = false;
var cfr_settled = false;
var cfr_timer = null;

function cfr_show_error() {
  if (cfr_settled) { return; }
  cfr_settled = true;
  if (cfr_timer) { clearTimeout(cfr_timer); cfr_timer = null; }
  submitted = false;
  var box = document.getElementById('cfr_submit_error');
  if (box) { box.style.display = 'block'; box.scrollIntoView(); }
}

function cfr_show_thankyou() {
  if (cfr_settled) { return; }
  cfr_settled = true;
  if (cfr_timer) { clearTimeout(cfr_timer); cfr_timer = null; }
  submitted = false;
  window.location = 'correction_form_thankyou.php';
}

function cfr_on_submit() {
  submitted = true;
  cfr_settled = false;
  var box = document.getElementById('cfr_submit_error');
  if (box) { box.style.display = 'none'; }
  cfr_timer = setTimeout(cfr_show_error, 15000);
  return true;
}

/* primary channel: the response page posts {cfr:"ok"} or {cfr:"error"} */
window.addEventListener('message', function (e) {
  if (!submitted || !e.data || typeof e.data !== 'object') { return; }
  if (e.data.cfr === 'ok') { cfr_show_thankyou(); }
  else if (e.data.cfr === 'error') { cfr_show_error(); }
}, false);

/* fallback for a browser that blocks the message: read the status token
   out of the same-origin iframe once it has loaded. */
function cfr_iframe_loaded(frame) {
  if (!submitted) { return; }
  var status = null;
  try {
    var doc = frame.contentDocument || frame.contentWindow.document;
    var el = doc && doc.getElementById('cfr-status');
    if (el) { status = el.getAttribute('data-cfr-status'); }
  } catch (err) {
    return; /* cross-origin; wait for postMessage or the timeout */
  }
  if (status === 'ok') { cfr_show_thankyou(); }
  else { cfr_show_error(); }
}
</script>
    <iframe name="hidden_iframe" id="hidden_iframe" style="display:none;"
onload="cfr_iframe_loaded(this);">
    </iframe>
<form action="correction_form_response.php"
<?php
 //$action = '"https://docs.google.com/forms/d/1InNaDMuakzrKpkSXlzVn0ocnD3My2uBMWypUEebrO4c/formResponse"';
 //echo $action;
?>
 method="post" target="hidden_iframe" 
onsubmit="return cfr_on_submit();">
<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item ss-item-required ss-text"><div class="ss-form-entry"><label aria-hidden="true" class="ss-q-item-label" for="entry_dict"><div class="ss-q-title" title="Prefilled. Do not change">Which Dictionary?
<label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
<span class="ss-required-asterisk" title="Required">*</span>
&nbsp;&nbsp;
<?php
/* Use 'id' field of <input> to match with names in correction_form_response.php
   Leave 'name' field unchanged from the one originally used by Google
*/
 //$val = "<input type=\"text\" name=\"entry.1072768805\" value=\"$dict\" class=\"ss-q-short\" id=\"entry_1072768805\" dir=\"auto\" aria-label=\"Which Dictionary?  \" aria-required=\"true\" required=\"\" style=\"width:80px;position:relative;left:50px;\"  ></input>";
 $val = "<input type=\"text\" name=\"entry_dict\" value=\"$dict\" class=\"ss-q-short\" id=\"entry_dict\" dir=\"auto\" aria-label=\"Which Dictionary?  \" aria-required=\"true\" required=\"\" style=\"width:80px;position:relative;left:50px;\"  ></input>";
 echo $val;
?>
<div class="error-message"></div>
</div>

</div></div></div> 

<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item ss-item-required ss-text">
<div class="ss-form-entry">
 <label aria-hidden="true" class="ss-q-item-label" for="entry_L">
  <div class="ss-q-title" title="Record # where typo noticed. See Help.">Which ID?
  <label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
  <span class="ss-required-asterisk" title="Optional: Cologne Record ID">*</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">This is number appears on the display as L=1234.</div>
 </label>
&nbsp;&nbsp;
<input type="text" name="entry_L" 
  value="
<?php
 if ($dict == 'APES'){
  echo "0(NA)";
 }else {
  echo $lnum;
 }
?>
  " 
  class="ss-q-short" id="entry_L" dir="auto" aria-label="Which L code?  " aria-required="true" required="" title="" style="width:80px;position:relative;left:70px;">
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>
</div></div></div> 

<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item ss-item-required ss-text">
<div class="ss-form-entry">
 <label aria-hidden="true" class="ss-q-item-label" for="entry_hw">
  <div class="ss-q-title" title="The headword where typo noticed">Which Headword?
  <label for="itemView.getDomIdToLabel()" aria-label="(Required field)"></label>
  <span class="ss-required-asterisk" title="Required">*</span>
  <div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">The headword under which you are submitting a correction</div>
 </label>
&nbsp;&nbsp;
<input type="text" name="entry_hw" value="<?php echo $hw; ?>" class="ss-q-short" id="entry_hw" dir="auto" aria-label="Headword The headword under which you are submitting a correction " aria-required="true" required="" title="" style="width:80px;position:relative;left:48px;">
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>
</div>
</div></div></div> 

<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item  ss-paragraph-text">
<div class="ss-form-entry">
 <label aria-hidden="true" class="ss-q-item-label" for="entry_old">
  <div class="ss-q-title" title="The text that is wrong">What is the typo?
  <div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">The text that is wrong</div>

 </label>
 </div>
<textarea name="entry_old" rows="2" cols="30" class="ss-q-long" id="entry_old" dir="auto" aria-label="Old  The text that is wrong "></textarea>

<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>

</div></div></div> 

<div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item  ss-paragraph-text"><div class="ss-form-entry"><label aria-hidden="true" class="ss-q-item-label" for="entry_new">
<div class="ss-q-title" title="The corrected text">What is the correction?
</div>
<div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none";>The text that is correct</div></label>
<textarea name="entry_new" rows="2" cols="40" class="ss-q-long" id="entry_new" dir="auto" aria-label="New The text that is correct "></textarea>
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>

</div></div></div> <div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item  ss-paragraph-text"><div class="ss-form-entry"><label aria-hidden="true" class="ss-q-item-label" for="entry_comment"><div class="ss-q-title" title="Typo, scan, other">What kind of error?
</div>
<div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">Any additional explanation of the error </div></label>
<textarea name="entry_comment" rows="2" cols="40" class="ss-q-long" id="entry_comment" dir="auto" aria-label="Comment Any additional explanation of the error  ">Typo</textarea>
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>

</div></div></div> <div class="ss-form-question errorbox-good">
<div dir="ltr" class="ss-item  ss-paragraph-text"><div class="ss-form-entry"><label aria-hidden="true" class="ss-q-item-label" for="entry_email"><div class="ss-q-title" title="Your Email Address or Name; Optional"
>Your Name or e-mail ID?
</div>
<div class="ss-q-help ss-secondary-text" dir="ltr" style="display:none;">Optional, if you with to be notified when the correction is made</div></label>
<textarea name="entry_email" rows="1" cols="40" class="ss-q-long" id="entry_email" dir="auto" aria-label="Your Email Address Optional, if you with to be notified when the correction is made "></textarea>
<div class="error-message"></div>
<div class="required-message" style="display:none;">This is a required question</div>

</div></div></div>
<!--
<input type="hidden" name="draftResponse" value="[,,&quot;-720978696993452283&quot;]">
<input type="hidden" name="pageHistory" value="0">
<input type="hidden" name="fbzx" value="-720978696993452283">
-->
<div class="ss-item ss-navigate"><table id="navigation-table"><tbody><tr><td class="ss-form-entry goog-inline-block" id="navigation-buttons" dir="ltr">
<input type="submit" name="submit" value="Submit" id="ss-submit">
<div class="ss-secondary-text" style="display:none;">Never submit passwords through Google Forms.</div></td>
</tr></tbody></table></div></ol></form></div>


<div id="docs-aria-speakable" class="docs-a11y-ariascreenreader-speakable docs-offscreen" aria-live="assertive" role="region" aria-atomic></div></div>

<script type='text/javascript' src='/static/forms/client/js/2161195797-formviewer_prd.js'></script>
<script type="text/javascript">H5F.setup(document.getElementById('ss-form'));_initFormViewer(
          "[100,\x22#ccc\x22,[]\n]\n");
      </script></div>
</body>
</html>
