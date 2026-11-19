<!DOCTYPE html>
<html>
<title>ABDpred</title>
<link rel="icon" href="image/abdpred_logo.jpg" type="image/jpg"/>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">

<style> 
input[type=text] {
  width: 100%;
  padding: 12px 20px;
  margin: 8px 0;
  box-sizing: border-box;
  border: none;
  background-color: #3CBC8D;
  color: white;
}
</style>

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

<script type="text/javascript">
<!--
// Form validation code will come here.
function validateForm()
{
var x=document.forms["myForm"]["CID"].value;
if (x==null || x==""||x=='')
  {
  alert("Please enter PubChem CID for Drug to be searched");
  return false;
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
<p>The Antibiotic Drug Prediction Server<strong> (ABDpred) </strong> allows users to predict the antibiotic drugs accurately in less time using XGBoost Classifier, Random Forest Classifier, Gradient Boosting Classifier, and Deep Neural Network Classifier. The web frame of the server has been designed using PHP and Python (Python 3.8.6). The web frame of the server has been designed using Apache, PHP, and Python (Python 3.8.6) inside Cent OS.  <br/>
</p>
<p>Users can type the PubChem CID of the desired drug to check whether the input drug is an antibiotic drug or non-antibiotic drug. An example of one antibiotic drug named "Gramicidin D" (45267103), known antibiotic drug has given. 
<!--Then users can  click the &#39; predict &#39; option. For more input users can select the URL of the bottom of the page.--></p>
<p></p>
<p>
<p>&nbsp;</p>
<p>&nbsp;</p>
<table align="center" border="0">
<form name="myForm" method="POST" action="prediction_result1.php" onSubmit="return(validateForm());">
  <tr>
    <td>Input Drug PubChem CID</td>
    <td><input name=CID type=text value="45267103"></input></td>
  </tr>
  <tr>
    <td>&nbsp;</td>
    <td>&nbsp;</td>
  </tr>
  <td colspan="2"><p align="center"><input type="submit" name="Predict" value="Predict"/>&nbsp;
      <button type="reset" value="Reset">Reset</button></p></td>
  </tr>
  </form>
</table>
</p>
<!--<p align="center">
<a href="batch_input.php">For batch inputs please click</a>
</p>-->
<p>&nbsp;</p>
</div>
<div class="sticky">
  <div align="center">&copy; ICMR-NICED, Kolkata, 2021. For any queries regarding ABDpred, contact Dr. Santasabuj Das at <a href="mailto:santasabujdas@yahoo.com"> santasabujdas@yahoo.com</a></div>
</div>

</body>
</html>