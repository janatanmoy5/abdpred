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
$t=time();
$a=trim($a);
echo $t;
#exec("python3.8 mul.py");

exec("python3.8 code/test3.py $a $t");
system("python3.8 code/test2.py $a > $t.csv");

#exec("python3.8 code/blind_run_5_fold_best_model_XGB.py $t");
#exec("python3.8 code/blind_run_5_fold_best_model_RF.py $t");
#exec("python3.8 code/blind_run_5_fold_best_model_GBC.py $t");
#exec("python3.8 code/blind_run_deep_fivefold_dnn.py $t");
#exec("python3.8 code/similarity.py $a > $t.txt");
#exec("python3.8 code/drugaabbility_check.py $a > $t.txt.txt");

?>


</body>
</html>