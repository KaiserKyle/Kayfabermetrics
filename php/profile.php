<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="/wp-content/themes/justwrite/style.css">
  </head>
<style>
.axis path,
.axis line {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.x.axis path {
  display: none;
}

.line {
  fill: none;
  stroke: steelblue;
  stroke-width: 1.5px;
}

div.tooltip {
  position: absolute;	
  text-align: center;	
  width: 125px;	
  height: autp;		
  padding: 2px;	
  font: 12px sans-serif;	
  background: lightsteelblue;	
  border: 0px;					
  border-radius: 8px;
 /*  pointer-events: none;	This line needs to be removed */
	
}

.bigbox {   
    float: left;
    width: 250px;
    height: 150px;
    margin: 5px 5px 5px 5px;
    padding: 5px;
    border-width: 3px;
    border-style: solid;
    border-color: rgba(0,0,0,.2);
    text-align: center;
    vertical-align: middle;
    color: white;
}

body {
    background-color: #eaeaea;
}

</style>   
<body>
<?php include 'profilephp.php'?>
<div id="barContainer"></div>
<div id="graphContainer" style="clear:both"></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"></script>
<script src="elograph.js"></script>
<script src="winloss.js"></script>
</body>
</html> 