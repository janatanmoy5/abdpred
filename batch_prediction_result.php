<!DOCTYPE html>
<html>
<title>ABDpred</title>
<link rel="icon" href="image/abdpred_logo.jpg" type="image/jpg"/>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
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
  <li><a href="index.php" class="active" >Home</a></li>
  <li><a href="about.php">About</a></li>
  <li><a href="help.php" >Help</a></li>
  <li><a href="download.php">Download</a></li>
  <li><a href="team.php">Team</a></li>
  <li><a href="link.php">Link</a></li>
</ul>

<p>
<?php



$b=$_POST["methods"];
#echo $b;


if ($b=='XGB')

{
$b="XGBoost classifier";
$t=time();

$myfile = fopen($t."check_id.csv", "w") or die("Unable to open file!");
$a=$_POST["batch"];
fwrite($myfile, $a);
fclose($myfile);

#echo $t;
#echo "XGB";

system("python3.8 code/extract.py $t > $t.csv");
system("python3.8 code/Batch_prediction_XGB_pred.py $t");
system("python3.8 code/Batch_prediction_XGB_positiveness.py $t");
}

if ($b=='RF')

{
$b="Random Forest classifier";
$t=time();

$myfile = fopen($t."check_id.csv", "w") or die("Unable to open file!");
$a=$_POST["batch"];
fwrite($myfile, $a);
fclose($myfile);

#echo $t;
#echo "XGB";

system("python3.8 code/extract.py $t > $t.csv");
system("python3.8 code/Batch_prediction_RF_pred.py $t");
system("python3.8 code/Batch_prediction_RF_positiveness.py $t");
}


if ($b=='GBC')

{
$b="Gradient Boosting Classifier";
$t=time();

$myfile = fopen($t."check_id.csv", "w") or die("Unable to open file!");
$a=$_POST["batch"];
fwrite($myfile, $a);
fclose($myfile);


system("python3.8 code/extract.py $t > $t.csv");
system("python3.8 code/Batch_prediction_GBC_pred.py $t");
system("python3.8 code/Batch_prediction_GBC_positiveness.py $t");
}


if ($b=='DNN')

{
$b="Deep Neural Network Classifier";
$t=time();

$myfile = fopen($t."check_id.csv", "w") or die("Unable to open file!");
$a=$_POST["batch"];
fwrite($myfile, $a);
fclose($myfile);


system("python3.8 code/extract.py $t > $t.csv");
system("python3.8 code/blind_run_deep_fivefold_dnn_pred.py $t");

}






?>







<p align="center"><strong><u>Prediction Result</u></strong>


<table width="1000" border="" align="center">
  <tr>
    <td width="200" ><div align="center">Input Drug CID </div></td>
	<td width="200" ><div align="center">Selected Method</div></td>
    <td width="200" ><div align="center">Result </div></td>
    <td width="200" ><div align="center">Positiveness </div></td>
    <td width="200" ><div align="center">Negativeness </div></td>
  </tr>
  
  <tr>
  <td >
<?php

$file= fopen($t."check_id.csv", "r") or exit("Unable to open file!");
while(!feof($file))
  {
  $p1=fgets($file);
  $p1 = trim($p1); 
  if ($p1=='CID')
  {
  }
  else
  {
	  echo "<a href='https://pubchem.ncbi.nlm.nih.gov/compound/$p1'>".$p1."</a>"."<br/>";
  }

 }
fclose($file);
	
	
	
	
	
?> 

  
  </td>
 
  
  <td><?php echo $b;?></td>
  <td width="330">
<?php
	$file = fopen($t."pred.txt", "r") or die("Unable to open file!");
	while(!feof($file))
  {
  $p22=fgets($file);
  $p22 = trim($p22);
   if ($p22=='pos' OR $p22=='[ True]' OR $p22=='[[ True]')
   {	   
  echo "<font color='blue'>"."Antibiotic Drug"."</font>"."<br/>";
   }
   if ($p22=='neg' OR $p22=='[False]' OR $p22=='[False]]' OR $p22=='[[False]]')
   {	   
  echo "<font color='red'>"."Not Antibiotic Drug"."</font>"."<br/>";
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
  echo $bcc."<br/>";
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
  echo $bcc."<br/>";
 }
fclose($file);

?>


</td>
</tr>
</table>


</p>
<p align="center"><button onclick="myFunction()">Print this prediction result page</button></p>

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

<?php

unlink("$t.csv");
unlink($t."pred.txt");
unlink($t."pos.txt");
unlink($t."neg.txt");
unlink($t."check_id.csv");



?>

<p>&nbsp;</p>
<div class="sticky">
  <div align="center">&copy; ICMR-NICED, Kolkata, 2020. For any queries regarding ABDpred, contact Dr. Santasabuj Das at <a href="mailto:santasabujdas@yahoo.com"> santasabujdas@yahoo.com</a></div>
</div>
</body>
</html>