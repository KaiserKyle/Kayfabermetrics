 (function () {
  var margins = {
    top: 12,
    left: 48,
    right: 24,
    bottom: 24
},
legendPanel = {
    width: 180
};
var width = 750 - margins.left - margins.right - legendPanel.width;
var height = 150 - margins.top - margins.bottom;

var wrestlerID = get('ID');

// Define 'div' for tooltips
var div = d3.select("#barContainer")
	.append("div")  // declare the tooltip div 
	.attr("class", "tooltip")              // apply the 'tooltip' class
	.style("opacity", 0);  
    
d3.json("winloss.php?ID=" + wrestlerID, function(error, data) {
  if (error) throw error;
  
  function getTooltip(d) {
    var tooltip = d.x + " ";
    if (d.y == "W") {
      tooltip += "wins by ";
    }
    else if (d.y == "L") {
      tooltip += "losses by ";
    }
    else
    {
      tooltip += "draws";
      return tooltip;
    }
    
    if (d.series == "pin") {
      tooltip += "pinfall";
    }
    else if (d.series == "sub") {
      tooltip += "submission";
    }
    else if (d.series == "KO") {
      tooltip += "knock out";
    }
    else if (d.series == "DQ"){
      tooltip += "disqualification";
    }
    
    return tooltip;
  }
  
  var dataset = data;
  var series = dataset.map(function (d) {
          return d.name;
      });
  
  dataset = dataset.map(function (d, i) {
          return d.data.map(function (o, i2) {
              // Structure it so that your numeric
              // axis (the stacked amount) is y
              return {
                  y: parseInt(o.count),
                  x: o.result,
                  series: series[i]
              };
          });
      }),
      stack = d3.layout.stack();
  
  stack(dataset);
  
  var dataset = dataset.map(function (group) {
      return group.map(function (d) {
          // Invert the x and y values, and y0 becomes x0
          return {
              x: d.y,
              y: d.x,
              x0: d.y0,
              series: d.series
          };
      });
  }),
      svg2 = d3.select('#barContainer')
          .append('svg')
          .attr('width', width + margins.left + margins.right + legendPanel.width)
          .attr('height', height + margins.top + margins.bottom)
          .append('g')
          .attr('transform', 'translate(' + margins.left + ',' + margins.top + ')')
          .on("mouseout", function(d) {
            div.transition()
				.duration(200)	
				.style("opacity", 0);
          });
          
          
      var xMax = d3.max(dataset, function (group) {
          return d3.max(group, function (d) {
              return d.x + d.x0;
          });
      }),
      xScale = d3.scale.linear()
          .domain([0, xMax])
          .range([0, width]),
      months = dataset[0].map(function (d) {
          return d.y;
      }),
      _ = console.log(months),
      yScale = d3.scale.ordinal()
          .domain(months)
          .rangeRoundBands([0, height], .1),
      xAxis = d3.svg.axis()
          .scale(xScale)
          .orient('bottom'),
      yAxis = d3.svg.axis()
          .scale(yScale)
          .orient('left'),
      colours = d3.scale.category10(),
      groups = svg2.selectAll('g')
          .data(dataset)
          .enter()
          .append('g')
          .style('fill', function (d, i) {
          return colours(i);});
          
      var rects = groups.selectAll('rect')
          .data(function (d) {
          return d;
      })
          .enter()
          .append('rect')
          .attr('x', function (d) {
          return xScale(d.x0);
      })
          .attr('y', function (d, i) {
          return yScale(d.y);
      })
          .attr('height', function (d) {
          return yScale.rangeBand();
      })
          .attr('width', function (d) {
          return xScale(d.x);
      }).on("mouseover", function(d) {		
            div.transition()
				.duration(500)	
				.style("opacity", 0);
			div.transition()
				.duration(200)	
				.style("opacity", .9);	
			div	.html(getTooltip(d))
                .style("left", (d3.event.pageX) + "px")			 
				.style("top", (d3.event.pageY - 28) + "px");});
  
      svg2.append('g')
          .attr('class', 'axis')
          .attr('transform', 'translate(0,' + height + ')')
          .call(xAxis);
  
  svg2.append('g')
      .attr('class', 'axis')
      .call(yAxis);
  
  svg2.append('rect')
      .attr('fill', 'yellow')
      .attr('width', 160)
      .attr('height', 30 * dataset.length)
      .attr('x', width + margins.left)
      .attr('y', 0);
  
  series.forEach(function (s, i) {
      svg2.append('text')
          .attr('fill', 'black')
          .attr('x', width + margins.left + 8)
          .attr('y', i * 24 + 24)
          .text(s);
      svg2.append('rect')
          .attr('fill', colours(i))
          .attr('width', 60)
          .attr('height', 20)
          .attr('x', width + margins.left + 90)
          .attr('y', i * 24 + 6);
});
});})();