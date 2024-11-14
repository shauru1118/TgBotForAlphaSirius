<?php 
$output = shell_exec('python3 background.py h'); 
echo $output;
header('Location: index.php');
?>
