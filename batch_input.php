<!DOCTYPE html>
<html>
<title>ABDpred</title>
<link rel="icon" href="image/amdpred_logo.jpg" type="image/jpg"/>
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


<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
<script>
$(document).ready(function(){
   
    $("#btn1").click(function(){
        $("#batch").text("CID \n45267103\n12560\n13791\n3308\n4688");
       
    }
);

$("#reset").click(function(){
        $("#batch").text("");
    }
);

});
</script>




<script type="text/javascript">
<!--
// Form validation code will come here.
function validate()
{

  
if( document.main.batch.value =="") 
   {
    
     alert( "Please fill provide more than one PubChem CIDs of Drugs followed by 'CID'. Please click to example for better input" );
      document.main.batch.focus() ;
     return false;
   }
else{
  
  return true;
 }


}
</script>



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

<div>
<p>The Antibiotic Drug Prediction Server<strong> (ABDpred) </strong> allows users to predict the antibiotic drugs accurately in less time.</p>
<p align="center">For batch option kindly provide inputs &lt; 10 at a single time for better prediction result without an error.</p>
<p>
<table align="center" width="820" border="0">
<form name="main" method="POST" action="batch_prediction_result.php" onsubmit="return(validate());"> 
  <tr>
    <td>Input PubChem CID of Drugs</td>
    <td><textarea name="batch" id="batch" rows="10" cols="50"></textarea></td>	
  </tr>

  <tr>
    <td><span style="cursor:pointer"><font color="blue" size="4"><u id="btn1">EXAMPLE</u></font> </span></td>
    <td>&nbsp;</td>
  </tr>
  <tr>
    <td>Select (Machine learning) ML model</td>
    <td>
		<input type="radio" name="methods" value="XGB" checked="checked"> 
		XGB (XGBoost Classifier)<br>
        <input type="radio" name="methods" value="RF"> 
        RF (Random Forest Classifier) <br>
        <input type="radio" name="methods" value="GBC"> 
        GBC (Gradient Boosting Classifier)<br>
		<input type="radio" name="methods" value="DNN">
		DNN (Deep Neural Network Classifier)</td>
  </tr>
  <tr>
  <td colspan="2"><p align="center"><input type="submit" name="Submit" value="Submit" /><button type="reset" value="Reset" id="reset">Reset</button></p></td>
  </tr>
  </form>
</table>
</p>

</div>
<div class="sticky">
  <div align="center">&copy; ICMR-NICED, Kolkata, 2020. For any queries regarding ABDpred, contact Dr. Santasabuj Das at <a href="mailto:santasabujdas@yahoo.com"> santasabujdas@yahoo.com</a></div>
</div>

</body>
</html>