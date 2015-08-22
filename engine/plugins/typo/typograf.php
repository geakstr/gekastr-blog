<?php
error_reporting(0);
header('Content-Type: text/html; charset=utf-8');
require_once('EMT.php');

$typograf = new EMTypograph();
$typograf->setup(array(
  'Text.paragraphs' => 'off',
  'Text.breakline' => 'off'
));
$typograf->set_text(base64_decode($argv[1]));
echo $typograf->apply();