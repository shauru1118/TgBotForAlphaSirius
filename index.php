<?php 
$output = shell_exec('python3 main.py h'); 
echo $output;
header('Location: index.php');
?>
