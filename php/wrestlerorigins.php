<!DOCTYPE html>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="/wp-content/themes/justwrite/style.css">
  </head>
  <style>
#chart {
  height: 1000px;
}

.node rect {
  cursor: move;
  fill-opacity: .9;
  shape-rendering: crispEdges;
}

.node text {
  pointer-events: none;
  text-shadow: 0 1px 0 #fff;
}

.link {
  fill: none;
  stroke: #000;
  stroke-opacity: .2;
}

.link:hover {
  stroke-opacity: .5;
}

</style>

  <body>
    <div id="chart"></div>
<script src="http://d3js.org/d3.v2.min.js?2.9.1"></script>
<script src="sankey.js"></script>
<script>

var margin = {top: 10, right: 10, bottom: 10, left: 10},
    width = 1000 - margin.left - margin.right,
    height = 1000 - margin.top - margin.bottom;

var formatNumber = d3.format(",.0f"),
    format = function(d) { return formatNumber(d) + " Wrestlers"; },
    color = d3.scale.category20();

var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var sankey = d3.sankey()
    .nodeWidth(15)
    .nodePadding(10)
    .size([width, height]);

var path = sankey.link();

d3.json("sankey.php", function(energy) {

  sankey
      .nodes(energy[0].nodes)
      .links(energy[1].links)
      .layout(32);

  var link = svg.append("g").selectAll(".link")
      .data(energy[1].links)
    .enter().append("path")
      .attr("class", "link")
      .attr("d", path)
      .style("stroke-width", function(d) { return Math.max(1, d.dy); })
      .sort(function(a, b) { return b.dy - a.dy; });

  link.append("title")
      .text(function(d) { return d.source.name + " to " + d.target.name + ": " + d.value + " wrestler(s)"; });

  var node = svg.append("g").selectAll(".node")
      .data(energy[0].nodes)
    .enter().append("g")
      .attr("class", "node")
      .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; })
    .call(d3.behavior.drag()
      .origin(function(d) { return d; })
      .on("dragstart", function() { this.parentNode.appendChild(this); })
      .on("drag", dragmove))
    .on("mouseover", mouseover);

  node.append("rect")
      .attr("height", function(d) { return d.dy; })
      .attr("width", sankey.nodeWidth())
      .style("fill", function(d) { return d.color = color(d.name.replace(/ .*/, "")); })
      .style("stroke", function(d) { return d3.rgb(d.color).darker(2); })
    .append("title")
      .text(function(d) { return d.name + "\n" + format(d.value); });

  node.append("text")
      .attr("x", -6)
      .attr("y", function(d) { return d.dy / 2; })
      .attr("dy", ".35em")
      .attr("text-anchor", "end")
      .attr("transform", null)
      .text(function(d) { return d.name; })
    .filter(function(d) { return d.x < width / 2; })
      .attr("x", 6 + sankey.nodeWidth())
      .attr("text-anchor", "start");

  function dragmove(d) {
    d3.select(this).attr("transform", "translate(" + d.x + "," + (d.y = Math.max(0, Math.min(height - d.dy, d3.event.y))) + ")");
    sankey.relayout();
    link.attr("d", path);
  }
  
  function mouseover(d) {
    var infoDiv = d3.select("#info");
    var infoImg = d3.select("#infoimg");
    infoDiv[0][0].style.textAlign = "center";
    infoDiv[0][0].innerHTML = "<p style=\"font-size:24px\"><b>" + d.fullname + "</b></p>";
    infoDiv[0][0].innerHTML += "<img id=\"infoimg\" style=\"float:right;height:225px;width:250px;padding-right:25px\" src=\"http://media.graytvinc.com/images/600*600/wwe_world_wrestling_entertainment_logo_square.jpg\"/>";
  }
});

</script>
<div id="info" style="width:1000px;height:300px;-webkit-border-radius: 20px;-moz-border-radius: 20px;border-radius: 20px;border:2px solid #000000;background:rgba(42,136,176,0.9);"><img id="infoimg" style="float:right"/></div>
</body>
</html> 