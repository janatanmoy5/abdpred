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

<script type="text/javascript">
function newPopup(url) {
	popupWindow = window.open(
		url,'popUpWindow','height=600,width=900,left=10,top=10,resizable=yes,scrollbars=yes,toolbar=yes,menubar=no,location=no,directories=no,status=yes')
}
</script>

<script>
function dd_scrolltotop(duration){
	duration = duration || 500
	var rootel = (document.compatMode =="BackCompat")? document.body : document.documentElement
	if (rootel.scrollTop == 0) // in some browsers such as Chrome, use document.body instead of document.documentElement
		rootel = document.body
	var curscrolltop = rootel.scrollTop, scrolltimer, elapsedtime, starttime = new Date().getTime(), animatedegree = 0
	var totaldis = curscrolltop
	clearTimeout(scrolltimer)
	function jumptop(){
		elapsedtime = new Date().getTime() - starttime
		if (elapsedtime < duration){
			rootel.scrollTop = totaldis - (totaldis * (1-Math.cos((elapsedtime/duration)*Math.PI)) / 2)
			scrolltimer = setTimeout(function(){jumptop()}, 10)
		}
	}
	jumptop()
}
</script>
<link rel="stylesheet" type="text/css" href="gooeymenu.css" />


<style type="text/css">
<!--
.style1 {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 13px; color: #ffffff}
.style2 {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 12px}
.style2 a:link { text-decoration: none }
.style2 a:link {color:forestgreen;}
.style2 a:visited {color:seagreen;}
.style2 a:hover {text-decoration:none;color:yellowgreen;font-weight:bold;}
.style2 a:active {color:red;text-decoration: none}
.style3 {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 10px; font-weight: bold}
.style4 {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 10px}
.style4 a:link { text-decoration: none }
.style4 a:link {color:forestgreen;}
.style4 a:visited {color:seagreen;}
.style4 a:hover {text-decoration:none;color:yellowgreen;font-weight:bold;}
.style4 a:active {color:red;text-decoration: none}
.style5 {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 14px}
.style6 {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 10px; font-weight: bold; color: #12a306}
.style7 {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 13px}
.style7 a:link { text-decoration: none }
.style7 a:link {color:forestgreen;}
.style7 a:visited {color:seagreen;}
.style7 a:hover {text-decoration:none;color:yellowgreen;font-weight:bold;}
.style7 a:active {color:yellowgreen;text-decoration: none}
.style8 {font-family: Verdana, Arial, Helvetica, sans-serif; font-size: 12px}
.style8 a:hover { cursor: help }
-->
</style>
</head>
<body>

<div class="header">
  <h2 align="center"><img src="image/abdpred.png" height="80" width="120">ABDpred: Antibiotic Drug Prediction Server</h2>
</div>


<ul>
  <li><a href="index.php">Home</a></li>
  <li><a href="about.php">About</a></li>
  <li><a href="help.php" class="active" >Help</a></li>
  <li><a href="download.php">Download</a></li>
  <li><a href="team.php">Team</a></li>
  <li><a href="link.php">Link</a></li>
</ul>
<p>ABDpred server capable to predict the input drug is antibiotic drug or non-antibiotic drug. <br/>

<font color="red"><b>Input:</b></font>
Users must provide the PubChem CID of the input Drug. <br/>
<font color="red"><b>Output:</font></b> After pressing "Predict button", The ABDpred server would return five different results of input drug. Here example of input drug is Gramicidin D (45267103). Those are: i) Input Drug brief details, ii) Druglikeness and Bioavailability profile checking of Input Drug, iii) Prediction Results given by different Machine Learning (ML) Classifiers (such as: XGB, RF, GBC and DNN), iv) Aggregation of prediction results obtaining from four Machine Learning (ML) Classifiers (namely, XGB, RF, GBC AND DNN) using soft voting technique and  v) Simialrity Searching result of Input Drug to known Antibiotic Drugs based on Tanimoto Coefficient scores. </b></font>
<p> <b>Step1:</b> Filled up the required information. </p>
<p class="style4"><a href="JavaScript:newPopup('image/help1.jpg');"><img src="image/help1.jpg" width="400" height="227"></a><br/></p>


<p> <b>Step2 </b>: Press the "Predict" Button. If the data is required for reset value, then press reset button. </p>
<p> <b>Step3</b>: Prediction result as output:</p>

<p>i) <b>First Output Section:</p>
<p class="style4"><a href="JavaScript:newPopup('image/help2.jpg');"><img src="image/help2.jpg" width="400" height="227"></a><br/></p>

<p>ii) <b>Second Output Section: </b> </p>
<p class="style4"><a href="JavaScript:newPopup('image/help3.jpg');"><img src="image/help3.jpg" width="400" height="227"></a><br/></p>
<p>iii) <b>Third Output Section: </b></p>
<p class="style4"><a href="JavaScript:newPopup('image/helpp4.jpg');"><img src="image/helpp4.jpg" width="400" height="227"></a><br/></p>
<p>iv) <b>Fourth Output Section: </b></p>
<p class="style4"><a href="JavaScript:newPopup('image/help5.jpg');"><img src="image/help5.jpg" width="400" height="227"></a><br/></p>
<p>v) <b>Fifth Output Section: </b></p>
<p class="style4"><a href="JavaScript:newPopup('image/help6.jpg');"><img src="image/help6.jpg" width="400" height="227"></a><br/></p>
<div class="sticky">
  <div align="center">&copy; ICMR-NICED, Kolkata, 2021. For any queries regarding ABDpred, contact Dr. Santasabuj Das at <a href="mailto:santasabujdas@yahoo.com"> santasabujdas@yahoo.com</a></div>
</div>

</body>
</html>