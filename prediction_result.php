<!DOCTYPE html>
<html>
<title>ABDpred</title>
<link rel="icon" href="image/abdpred_logo.jpg" type="image/jpg"/>
<head>
<style>
body {
  font-size: 20px;
}

ul {
  list-style-type: none;
  margin: 20;
  padding: 20;
  overflow: hidden;
  background-color: #333;
  position: -webkit-sticky; /* Safari */
  position: sticky;
  top: 0;
}

li {
  float: left;
}

li a {
  display: block;
  color: white;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}

li a:hover {
  background-color: #111;
}

.active {
  background-color: #4CAF50;
}

div.sticky {
  position: -webkit-sticky;
  position: sticky;
  top: 0;
  background-color: #CCCCCC;
  padding: 50px;
  font-size: 20px;
}

</style>

<style>
</style>

</head>
<body>

<div class="header">
  <h2 align="center"><img src="image/abdpred.png" height="80" width="120">ABDpred: Antibiotic Drug Prediction Server</h2>
</div>

<ul>
  <li><a class="active" href="index.php">Home</a></li>
  <li><a href="about.php">About</a></li>
  <li><a href="help.php">Help</a></li>
  <li><a href="download.php">Download</a></li>
  <li><a href="team.php">Team</a></li>
  <li><a href="link.php">Link</a></li>
</ul>

<p>
<?php
$a=$_POST["CID"];
$b=$_POST["methods"];
if ($b=='XGB')

{
	
$t=time();
#echo($t . "<br>");
$xgb='XGBoost Classifier';	
$a=trim($a);
exec("python3.8 code/test3.py $a $t");
exec("python3.8 code/test2.py $a > $t.csv");

exec("python3.8 code/blind_run_5_fold_best_model_XGB.py $t");

#rmdir("$t");
#chdir("$t");



?>




<p align="center"><strong><u>Input Drug brief details</u></strong>
<table width="900" border="1" align="center">
  <tr>
    <td width="300"><div align="center">Structure</div></td>
    <td width="600"><div align="center">Synonyms Name </div></td>
  </tr>
  <tr>
    <td width="300">
	<?php
	 $image = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/".$a."/PNG";
	$imageData = base64_encode(file_get_contents($image));
	echo '<img src="data:image/jpeg;base64,'.$imageData.'" width="400" height="300">';
	 ?>    </td>
    <td width="600">
	<?php
	$myfile = fopen($t."syno.txt", "r") or die("Unable to open file!");
	echo "<p align='center'>".fread($myfile,filesize($t."syno.txt"))."</p>";
	fclose($myfile);
	?>
	
	</td>
  </tr>
</table>
<p><u><strong></strong></u>
<p align="center"><strong><u>Prediction Result</u></strong>

<table width="900" border="" align="center">
  <tr>
    <td width="180" ><div align="center">Input Drug CID </div></td>
	<td width="180" ><div align="center">Selected Method</div></td>
    <td width="180" ><div align="center">Result </div></td>
    <td width="180" ><div align="center">Positiveness</div></td>
    <td width="180" ><div align="center">Negativeness </div></td>
  </tr>
  
  <tr>
  <td><?php echo "<p align='center'>"."<a href='https://pubchem.ncbi.nlm.nih.gov/compound/$a' target=_blank>".$a."</a>"."</p>"; ?></td>
  <td><?php echo "<p align='center'>".$xgb."</p>"; ?></td>
  <td>
  <?php
	$file = fopen($t."pred.txt", "r");
	while(!feof($file))
  {
  $p22=fgets($file);
  $p22 = trim($p22);
   if ($p22=='[1]')
   {	   
  echo "<p align='center'>"."<font color='blue'>"."Antibiotic Drug"."</font>"."</p>";
   }
   if ($p22=='[0]')
   {	   
  echo "<p align='center'>"."<font color='red'>"."Non-Antibiotic Drug"."</font>"."</p>";
   }
   
 }
fclose($file);
?> 
  </td>
  <td>
	
	<?php
	$file = fopen($t."pos.txt", "r") or die("Unable to open file!");
	while(!feof($file))
  {
  $p2=fgets($file);
  $p2 = trim($p2); 
  $acc= str_replace("[","",$p2);
	$bcc=str_replace("]","",$acc);
  echo "<p align='center'>".$bcc."</p>";
 }
fclose($file);
?> 
	
	
  </td>
  <td>
  
   <?php
  
  $file = fopen($t."neg.txt", "r") or die("Unable to open file!");
	while(!feof($file))
  {
  $p23=fgets($file);
  $p23 = trim($p23); 
  $acc= str_replace("[","",$p23);
	$bcc=str_replace("]","",$acc);
  echo "<p align='center'>".$bcc."</p>";
 }
fclose($file);

?>
  
  </td>
  
  
  </tr>
  
  
  </table>




<?php	

}

if ($b=='RF')
{
	
$t=time();
#echo($t . "<br>");
$b='Random Forest Classifier';	
$a=trim($a);
exec("python3.8 code/test3.py $a $t");
exec("python3.8 code/test2.py $a > $t.csv");


exec("python3.8 code/blind_run_5_fold_best_model_RF.py $t");
?>
<p align="center"><strong><u>Input Drug brief details</u></strong>
<table width="964" border="1" align="center">
  <tr>
    <td width="308"><div align="center">Structure</div></td>
    <td width="640"><div align="center">Synonyms Name </div></td>
  </tr>
  <tr>
    <td width="308">
	<?php
	 $image = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/".$a."/PNG";
	$imageData = base64_encode(file_get_contents($image));
	echo '<img src="data:image/jpeg;base64,'.$imageData.'" width="400" height="300">';
	 ?>    </td>
    <td width="640">
	<?php
	$myfile = fopen($t."syno.txt", "r") or die("Unable to open file!");
	echo "<p align='center'>".fread($myfile,filesize($t."syno.txt"))."</p>";
	fclose($myfile);
	?>
	
	</td>
  </tr>
</table>

<p><u><strong></strong></u>
<p align="center"><strong><u>Prediction Result</u></strong>

<table width="1400" border="" align="center">
  <tr>
    <td width="280" ><div align="center">Input Drug CID </div></td>
	<td width="280" ><div align="center">Selected Method</div></td>
    <td width="280" ><div align="center">Result </div></td>
    <td width="280" ><div align="center">Positiveness</div></td>
    <td width="280" ><div align="center">Negativeness </div></td>
  </tr>
  
  <tr>
  <td><?php echo "<p align='center'>"."<a href='https://pubchem.ncbi.nlm.nih.gov/compound/$a' target=_blank>".$a."</a>"."</p>"; ?></td>
  <td><?php echo "<p align='center'>".$b."</p>"; ?></td>
  <td>
  <?php
	$file = fopen($t."pred.txt", "r");
	while(!feof($file))
  {
  $p22=fgets($file);
  $p22 = trim($p22);
   if ($p22=='[1]')
   {	   
  echo "<p align='center'>"."<font color='blue'>"."Antibiotic Drug"."</font>"."</p>";
   }
   if ($p22=='[0]')
   {	   
  echo "<p align='center'>"."<font color='red'>"."Non-Antibiotic Drug"."</font>"."</p>";
   }
   
 }
fclose($file);
?> 
  </td>
  <td>
	
	<?php
	$file = fopen($t."pos.txt", "r") or die("Unable to open file!");
	while(!feof($file))
  {
  $p2=fgets($file);
  $p2 = trim($p2); 
  $acc= str_replace("[","",$p2);
	$bcc=str_replace("]","",$acc);
  echo "<p align='center'>".$bcc."</p>";
 }
fclose($file);
?> 
	
	
  </td>
  <td>
  
   <?php
  
  $file = fopen($t."neg.txt", "r") or die("Unable to open file!");
	while(!feof($file))
  {
  $p23=fgets($file);
  $p23 = trim($p23); 
  $acc= str_replace("[","",$p23);
	$bcc=str_replace("]","",$acc);
  echo "<p align='center'>".$bcc."</p>";
 }
fclose($file);

?>
  
  </td>
  
  
  </tr>
  
  
  </table>








<?php


	
	
	
	
}


if ($b=='GBC')
{
	
	$t=time();
#echo($t . "<br>");
$b='Gradient Boosting Classifier';	
$a=trim($a);
exec("python3.8 code/test3.py $a $t");
exec("python3.8 code/test2.py $a > $t.csv");


exec("python3.8 code/blind_run_5_fold_best_model_GBC.py $t");
?>	

<p align="center"><strong><u>Input Drug brief details</u></strong>
<table width="964" border="1" align="center">
  <tr>
    <td width="308"><div align="center">Structure</div></td>
    <td width="640"><div align="center">Synonyms Name </div></td>
  </tr>
  <tr>
    <td width="308">
	<?php
	 $image = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/".$a."/PNG";
	$imageData = base64_encode(file_get_contents($image));
	echo '<img src="data:image/jpeg;base64,'.$imageData.'" width="400" height="300">';
	 ?>    </td>
    <td width="640">
	<?php
	$myfile = fopen($t."syno.txt", "r") or die("Unable to open file!");
	echo "<p align='center'>".fread($myfile,filesize($t."syno.txt"))."</p>";
	fclose($myfile);
	?>
	
	</td>
  </tr>
</table>

<p><u><strong></strong></u>
<p align="center"><strong><u>Prediction Result</u></strong>

<table width="1400" border="" align="center">
  <tr>
    <td width="280" ><div align="center">Input Drug CID </div></td>
	<td width="280" ><div align="center">Selected Method</div></td>
    <td width="280" ><div align="center">Result </div></td>
    <td width="280" ><div align="center">Positiveness</div></td>
    <td width="280" ><div align="center">Negativeness </div></td>
  </tr>
  
  <tr>
  <td><?php echo "<p align='center'>"."<a href='https://pubchem.ncbi.nlm.nih.gov/compound/$a' target=_blank>".$a."</a>"."</p>"; ?></td>
  <td><?php echo "<p align='center'>".$b."</p>"; ?></td>
  <td>
  <?php
	$file = fopen($t."pred.txt", "r");
	while(!feof($file))
  {
  $p22=fgets($file);
  $p22 = trim($p22);
   if ($p22=='[1]')
   {	   
  echo "<p align='center'>"."<font color='blue'>"."Antibiotic Drug"."</font>"."</p>";
   }
   if ($p22=='[0]')
   {	   
  echo "<p align='center'>"."<font color='red'>"."Non-Antibiotic Drug"."</font>"."</p>";
   }
   
 }
fclose($file);
?> 
  </td>
  <td>
	
	<?php
	$file = fopen($t."pos.txt", "r") or die("Unable to open file!");
	while(!feof($file))
  {
  $p2=fgets($file);
  $p2 = trim($p2); 
  $acc= str_replace("[","",$p2);
	$bcc=str_replace("]","",$acc);
  echo "<p align='center'>".$bcc."</p>";
 }
fclose($file);
?> 
	
	
  </td>
  <td>
  
   <?php
  
  $file = fopen($t."neg.txt", "r") or die("Unable to open file!");
	while(!feof($file))
  {
  $p23=fgets($file);
  $p23 = trim($p23); 
  $acc= str_replace("[","",$p23);
	$bcc=str_replace("]","",$acc);
  echo "<p align='center'>".$bcc."</p>";
 }
fclose($file);

?>
  
  </td>
  
  
  </tr>
  
  
  </table>






	
	
<?php	
}


if ($b=='DNN')
{
	$t=time();
#echo($t . "<br>");
$b='Deep Neural Network Classifier';	
$a=trim($a);
exec("python3.8 code/test3.py $a $t");
exec("python3.8 code/test2.py $a > $t.csv");


exec("python3.8 code/blind_run_deep_fivefold_dnn.py $t");

#rmdir("$t");
#chdir("$t");

?>

<p align="center"><strong><u>Input Drug brief details</u></strong>
<table width="964" border="1" align="center">
  <tr>
    <td width="308"><div align="center">Structure</div></td>
    <td width="640"><div align="center">Synonyms Name </div></td>
  </tr>
  <tr>
    <td width="308">
	<?php
	 $image = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/".$a."/PNG";
	$imageData = base64_encode(file_get_contents($image));
	echo '<img src="data:image/jpeg;base64,'.$imageData.'" width="400" height="300">';
	 ?>    </td>
    <td width="640">
	<?php
	$myfile = fopen($t."syno.txt", "r") or die("Unable to open file!");
	echo "<p align='center'>".fread($myfile,filesize($t."syno.txt"))."</p>";
	fclose($myfile);
	?>
	
	</td>
  </tr>
</table>


<p><u><strong></strong></u>
<p align="center"><strong><u>Prediction Result</u></strong>

<table width="1400" border="" align="center">
  <tr>
    <td width="280" ><div align="center">Input Drug CID </div></td>
	<td width="280" ><div align="center">Selected Method</div></td>
    <td width="280" ><div align="center">Result </div></td>
    <td width="280" ><div align="center">Positiveness</div></td>
    <td width="280" ><div align="center">Negativeness </div></td>
  </tr>
  
  <tr>
  <td><?php echo "<p align='center'>"."<a href='https://pubchem.ncbi.nlm.nih.gov/compound/$a' target=_blank>".$a."</a>"."</p>"; ?></td>
  <td><?php echo "<p align='center'>".$b."</p>"; ?></td>
  <td>
  <?php
	$file = fopen($t."pred.txt", "r");
	while(!feof($file))
  {
  $p22=fgets($file);
  $p22 = trim($p22);
  $acc1= str_replace("[","",$p22);
  $bcc1=str_replace("]","",$acc1);
  
   if ($p22=='[[ True]]')
   {	   
  echo "<p align='center'>"."<font color='blue'>"."Antibiotic Drug"."</font>"."</p>";
   }
   if ($p22=='[[ False]]')
   {	   
  echo "<p align='center'>"."<font color='red'>"."Non-Antibiotic Drug"."</font>"."</p>";
   }
   
   
    if ($p22=='[[False]]')
   {	   
  echo "<p align='center'>"."<font color='red'>"."Non-Antibiotic Drug"."</font>"."</p>";
   }
   
   
   
 }
fclose($file);
?> 
  </td>
  <td>
	
	<?php
	$file = fopen($t."pos.txt", "r") or die("Unable to open file!");
	while(!feof($file))
  {
  $p2=fgets($file);
  $p2 = trim($p2); 
  $acc= str_replace("[","",$p2);
	$bcc=str_replace("]","",$acc);
  echo "<p align='center'>".$bcc."</p>";
 }
fclose($file);
?> 
	
	
  </td>
  <td>
  
   <?php
  
  $file = fopen($t."neg.txt", "r") or die("Unable to open file!");
	while(!feof($file))
  {
  $p23=fgets($file);
  $p23 = trim($p23); 
  $acc= str_replace("[","",$p23);
	$bcc=str_replace("]","",$acc);
  echo "<p align='center'>".$bcc."</p>";
 }
fclose($file);

?>
  
  </td>
  
  
  </tr>
  
  
  </table>




<?php
}


?>
</p>


<p>
<font size="5">
<b>Note:</b> <br/>
<b>Positiveness:</b> The probability to be Positive [1] &
<b>Negativeness:</b> The probability to be Negative [0] <b>
</font>
</p>

<script>
function myFunction() {
  window.print();
}
</script>
<p align="center"><button onclick="myFunction()">Print this prediction result page</button></p>

<?php


unlink("$t.csv");
unlink($t."pred.txt");
unlink($t."pos.txt");
unlink($t."neg.txt");
unlink($t."syno.txt");

?>

<div class="sticky">
  <div align="center">&copy; ICMR-NICED, Kolkata, 2020. For any queries regarding ABDpred, contact Dr. Santasabuj Das at <a href="mailto:santasabujdas@yahoo.com"> santasabujdas@yahoo.com</a></div>
</div>
</html>