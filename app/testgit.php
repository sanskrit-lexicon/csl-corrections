<?php
/*
  testgit.php — run gitupdate.sh (add / commit / push correction-form intake).

  H1523 security: this used to be callable over plain HTTP with no auth:
    $cmd = "sh gitupdate.sh"; shell_exec($cmd);
  Anyone who could hit the URL could force a git commit+push of the app tree.
  Restrict to CLI only (php app/testgit.php). Server maintainers who still
  need a web hook should put an authenticated endpoint in front, not this file.
*/
if (PHP_SAPI !== 'cli') {
  http_response_code(403);
  header('Content-Type: text/plain; charset=utf-8');
  echo "Forbidden: CLI only (php app/testgit.php)\n";
  exit(1);
}

$cwd = __DIR__;
$script = $cwd . DIRECTORY_SEPARATOR . 'gitupdate.sh';
if (!is_file($script)) {
  fwrite(STDERR, "gitupdate.sh not found in $cwd\n");
  exit(1);
}

// Fixed path only — no user input. escapeshellarg for the path is defense-in-depth.
$cmd = 'sh ' . escapeshellarg($script);
$out = shell_exec($cmd);
if ($out === null) {
  fwrite(STDERR, "shell_exec failed for gitupdate.sh\n");
  exit(1);
}
echo $out;
?>
