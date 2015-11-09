function get(name){
   if(name=(new RegExp('[?&]'+encodeURIComponent(name)+'=([^&]*)')).exec(location.search))
      return decodeURIComponent(name[1]);
}

var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 1000 - margin.left - margin.right,
    height = 250 - margin.top - margin.bottom;

var x = d3.scale.linear()
    .domain([0, 9.5])
    .range([width, 0]);

var y = d3.scale.linear()
    .range([height, 0]);

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left");

var line = d3.svg.line()
    .x(function(d) { return x(d.index); })
    .y(function(d) { return y(d.elo); });

var svg = d3.select("#graphContainer").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
    
// Define 'div' for tooltips
var div = d3.select("#graphContainer")
	.append("div")  // declare the tooltip div 
	.attr("class", "tooltip")              // apply the 'tooltip' class
	.style("opacity", 0);  

var wrestlerID = get('ID');
    
d3.json("elograph.php?ID=" + wrestlerID, function(error, data) {
  if (error) throw error;

  data.forEach(function(d, i) {
    d.date = d[3];
    d.elo = d[0];
    d.index = i;
  });
  
  var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")
    .tickFormat(function (d) {
      if (-1 == d || d >= data.length) {
        return "";
      }
      var date = new Date(data[d].date);
      return date.toLocaleDateString();});
  
  y.domain([parseFloat(d3.min(data, function(d) { return d.elo; })) - 5, parseFloat(d3.max(data, function(d) { return d.elo; })) + 5]);
  
  // draw the scatterplot
  svg.selectAll("dot")									
	.data(data)											
	.enter().append("circle")								
	.attr("r", 5)	
	.attr("cx", function(d) { return x(d.index); })		 
	.attr("cy", function(d) { return y(d.elo); })
    .on("mouseover", function(d) {		
            div.transition()
				.duration(500)	
				.style("opacity", 0);
			div.transition()
				.duration(200)	
				.style("opacity", .9);	
			div	.html(
                "<b>" + d[5] + "</b><br/>" +
 				d[4] +
				"<br/>Elo: "  + Math.round(d.elo))
				.style("left", (d3.event.pageX) + "px")			 
				.style("top", (d3.event.pageY - 28) + "px");});

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Elo Rating");

  svg.append("path")
      .datum(data)
      .attr("class", "line")
      .attr("d", line);
});