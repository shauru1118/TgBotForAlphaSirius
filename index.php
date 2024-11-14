<?php 
$output = shell_exec('python3 /var/www/static/blid.py h'); 
echo $output;
header('Location: index.php');
?>
