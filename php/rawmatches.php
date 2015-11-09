<!DOCTYPE html>
<html>
<meta charset="utf-8">
<title>Raw Matches By Wrestler</title>
<style>

#circle circle {
  fill: none;
  pointer-events: all;
}

.group path {
  fill-opacity: .5;
}

#tooltip {
        position: absolute;
        width: auto;
        height: auto;
        padding: 10px;
        background-color: white;
        -webkit-border-radius: 10px;
        -moz-border-radius: 10px;
        border-radius: 10px;
        -webkit-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
        -moz-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
        box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
        pointer-events: none;
}

#tooltip.hidden {
        display: none;
}

#tooltip p {
        margin: 0;
        font-family: sans-serif;
        font-size: 16px;
        line-height: 20px;
}

#winlosstooltip {
        position: absolute;
        width: auto;
        height: auto;
        padding: 10px;
        background-color: white;
        -webkit-border-radius: 10px;
        -moz-border-radius: 10px;
        border-radius: 10px;
        -webkit-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
        -moz-box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
        box-shadow: 4px 4px 10px rgba(0, 0, 0, 0.4);
        pointer-events: none;
}

#winlosstooltip.hidden {
        display: none;
}

#winlosstooltip p {
        margin: 0;
        font-family: sans-serif;
        font-size: 16px;
        line-height: 20px;
}

path.chord {
  stroke: #000;
  stroke-width: .25px;
}

#circle:hover path.fade {
  opacity: 0;
}

</style>
<script src="http://d3js.org/d3.v3.min.js"></script>

<div id="checkboxes" style="text-align:center">
  <label><input type="checkbox" title="Raw" id="raw" onchange="checkBoxClicked()" checked/>Raw</label>
  <label><input type="checkbox" title="Smackdown" id="smackdown" onchange="checkBoxClicked()"/>Smackdown</label>
  <label><input type="checkbox" title="PPV" id="ppv" onchange="checkBoxClicked()"/>PPV</label>
</div>
<div id="graphContainer" style="text-align:center">
  <div id="tooltip" class="hidden">
        <p><b><span id="name">Important Label Heading</span></b></p>
        <p><span id="value">100</span></p>
  </div>
  <div id="winlosstooltip" class="hidden">
        <p><span id="source">Important Label Heading</span></p>
        <p><span id="target">100</span></p>
  </div>
</div>
<p style="text-align:center">Built with <a href="http://d3js.org/">d3.js</a></p>
<p style="text-align:center">Data from <a href="http://www.profightdb.com/">profightdb.com</a></p>
<script>

var width = 1200,
    height = 1280,
    outerRadius = Math.min(width, height) / 2 - 100,
    innerRadius = outerRadius - 24;
    
var color = d3.scale.category20();

var formatPercent = d3.format(".1%");

var arc = d3.svg.arc()
    .innerRadius(innerRadius)
    .outerRadius(outerRadius);

function getDefaultLayout() {
    return d3.layout.chord()
    .padding(0.02)
    .sortSubgroups(d3.descending)
    .sortChords(d3.ascending);
} 
    
//var layout = d3.layout.chord()
//    .padding(.02)
//    .sortSubgroups(d3.descending)
//    .sortChords(d3.ascending);

var path = d3.svg.chord()
    .radius(innerRadius);

var svg = d3.select("#graphContainer").append("svg")
    .attr("width", width)
    .attr("height", height)
  .append("g")
    .attr("id", "circle")
    .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

var last_layout;
var current_data;
    
svg.append("circle")
    .attr("r", outerRadius);
    
renderData("/wp-content/uploads/2015/05/rawmatchesphp.php?showname=Raw");

// data is as follows
// [0] is the wrestlers list with number of matches
// [1] is the wins matrix
// [2] is the match matrix
function renderData(url) {
d3.json(url, function(data) {
  
    current_data = data;

    layout = getDefaultLayout();
    // Compute the chord layout.
    layout.matrix(data[2]);
    
    var oldGroup = svg.selectAll(".group").data(layout.groups(), function (d) {
            return d.index; 
            //use a key function in case the 
            //groups are sorted differently between updates
        });
    
    oldGroup.exit()
        .transition()
            .duration(1000)
            .attr("opacity", 0)
            .remove(); //remove after transitions are complete

    // Add a group per neighborhood.
    var group = oldGroup
      .enter().append("g")
      .attr("class", "group");

    //group.append("title");
        
    // Add a mouseover title.
    //oldGroup.select("title").text(function(d, i) {
    //  return data[0][i].name + ": " + data[0][i].nummatches + " matches";
    //});

    // Add the group arc.
    group.append("path")
        .attr("id", function(d, i) { return "group" + i; })
        .style("fill", function(d, i) { return color(data[0][i].name); })
        .on("mouseover", function(d, i) {
                
					//Get this bar's x/y values, then augment for the tooltip
                    var bbox = this.getBBox();
                    var matrix = this.getScreenCTM();
                    var pt = document.getElementsByTagName("svg")[0].createSVGPoint();
				    pt.x = bbox.x;
                    pt.y = bbox.y;
                    var origin = pt.matrixTransform(matrix);
                    origin.x = origin.x + document.documentElement.scrollLeft || document.body.scrollLeft;
                    origin.y = origin.y + document.documentElement.scrollTop || document.body.scrollTop;

					//Update the tooltip position and value
					d3.select("#tooltip")
						.style("left", origin.x + "px")
						.style("top", origin.y + "px")						
						.select("#value")
						.text(current_data[0][i].nummatches + " matches");
                    d3.select("#tooltip")
                        .select("#name")
                        .text(current_data[0][i].name);
			   
					//Show the tooltip
					d3.select("#tooltip").classed("hidden", false);

			   })
			   .on("mouseout", function() {
			   
					//Hide the tooltip
					d3.select("#tooltip").classed("hidden", true);
					
			   });
        
        //update the paths to match the layout
    oldGroup.select("path") 
        .transition()
            .duration(1000)
            //.attr("opacity", 0.5) //optional, just to observe the transition
        .attrTween("d", arcTween( last_layout ))
           // .transition().duration(100).attr("opacity", 1) //reset opacity
        ;
    
    group.append("svg:text")
      .attr("xlink:href", function (d, i) {
              return "#group" + data[0][i].name;
          })
      .attr("dy", ".35em")
      .text(function(d, i) { return data[0][i].name; });
      
      //position group labels to match layout
    oldGroup.select("text")
        .transition()
            .duration(1000)
            .text(function(d, i) { return data[0][i].name; })
            .attr("transform", function(d) {
                d.angle = (d.startAngle + d.endAngle) / 2;
                //store the midpoint angle in the data object
                
                return "rotate(" + (d.angle * 180 / Math.PI - 90) + ")" +
                    " translate(" + (innerRadius + 26) + ")" + 
                    (d.angle > Math.PI ? " rotate(180)" : " rotate(0)"); 
                //include the rotate zero so that transforms can be interpolated
            })
            .attr("text-anchor", function (d) {
                return d.angle > Math.PI ? "end" : "begin";
            });


    // Add the chords.
    var chord = svg.selectAll("path.chord")
        .data(layout.chords(), chordKey);
        
    var newChords = chord
      .enter().append("path")
        .attr("class", "chord")
        .on("mouseover", function(d, i) {
            if (this.className.baseVal == "chord")
            {  
              var origin = d3.mouse(this);
  
              //Update the tooltip position and value
              d3.select("#winlosstooltip")
                  .style("left", d3.event.x + "px")
                  .style("top", d3.event.y + "px")						
                  .select("#target")
                  .text(current_data[0][d.target.index].name + ": " + data[1][d.target.index][d.source.index] + " wins");
              d3.select("#winlosstooltip")
                  .select("#source")
                  .text(current_data[0][d.source.index].name + ": " + data[1][d.source.index][d.target.index] + " wins");
         
              //Show the tooltip
              d3.select("#winlosstooltip").classed("hidden", false);
            }
       })
       .on("mouseout", function() {
       
            //Hide the tooltip
            d3.select("#winlosstooltip").classed("hidden", true);
            
       });;    
//.attr("d", path);
        
    newChords.append("title");

    // Add an elaborate mouseover title for each chord.
    chord.select("title").text(function(d) {
      return data[0][d.source.index].name
          + ": " + data[1][d.source.index][d.target.index]
          + " wins, "
          + "\n" + data[0][d.target.index].name 
          + ": " + data[1][d.target.index][d.source.index]
          + " wins";
    });
    
    //handle exiting paths:
    chord.exit().transition()
        .duration(1500)
        .attr("opacity", 0)
        .remove();
        
        //update the path shape
    chord.transition()
        .duration(1500)
        //.attr("opacity", 0.5) //optional, just to observe the transition
        .style("fill", function(d) { return color(data[0][d.source.index].name); })
        .attrTween("d", chordTween(last_layout))
        //.transition().duration(100).attr("opacity", 1) //reset opacity
    ;
    
    //oldGroup.on("mouseover", mouseover);
    oldGroup.on("mouseover", function(d) {
        chord.classed("fade", function (p) {
            //returns true if *neither* the source or target of the chord
            //matches the group that has been moused-over
            return ((p.source.index != d.index) && (p.target.index != d.index));
        });
    });
    
    last_layout = layout; //save for next update

    function mouseover(d, i) {
      chord.classed("fade", function(p) {
        return p.source.index != i
            && p.target.index != i;
      });

    }
  });
};

function arcTween(oldLayout) {
        var oldGroups = {};
        if (oldLayout) {
            oldLayout.groups().forEach( function(groupData) {
                oldGroups[ groupData.index ] = groupData;
            });
        }
        
        return function (d, i) {
            var tween;
            var old = oldGroups[d.index];
            if (old) { //there's a matching old group
                tween = d3.interpolate(old, d);
            }
            else {
                //create a zero-width arc object
                var emptyArc = {startAngle:d.startAngle,
                                endAngle:d.startAngle};
                tween = d3.interpolate(emptyArc, d);
            }
            
            return function (t) {
                return arc( tween(t) );
            };
        };
    }
    
function chordKey(data) {
    return (data.source.index < data.target.index) ?
        data.source.index  + "-" + data.target.index:
        data.target.index  + "-" + data.source.index;
}

function chordTween(oldLayout) {
    //this function will be called once per update cycle
    
    //Create a key:value version of the old layout's chords array
    //so we can easily find the matching chord 
    //(which may not have a matching index)
    
    var oldChords = {};
    
    if (oldLayout) {
        oldLayout.chords().forEach( function(chordData) {
            oldChords[ chordKey(chordData) ] = chordData;
        });
    }
    
    return function (d, i) {
        //this function will be called for each active chord
        
        var tween;
        var old = oldChords[ chordKey(d) ];
        if (old) {
            //old is not undefined, i.e.
            //there is a matching old chord value
            
            //check whether source and target have been switched:
            if (d.source.index != old.source.index ){
                //swap source and target to match the new data
                old = {
                    source: old.target,
                    target: old.source
                };
            }
            
            tween = d3.interpolate(old, d);
        }
        else {
            //create a zero-width chord object
            if (oldLayout) {
                var oldGroups = oldLayout.groups().filter(function(group) {
                        return ( (group.index == d.source.index) ||
                                 (group.index == d.target.index) )
                    });
                old = {source:oldGroups[0],
                           target:oldGroups[1] || oldGroups[0] };
                    //the OR in target is in case source and target are equal
                    //in the data, in which case only one group will pass the
                    //filter function
                    
                if (old.source) {
                  if (d.source.index != old.source.index ){
                      //swap source and target to match the new data
                      old = {
                          source: old.target,
                          target: old.source
                      };
                  }
                }
                else old = d;
            }
            else old = d;
                
            var emptyChord = {
                source: { startAngle: old.source.startAngle,
                         endAngle: old.source.startAngle},
                target: { startAngle: old.target.startAngle,
                         endAngle: old.target.startAngle}
            };
            tween = d3.interpolate( emptyChord, d );
        }

        return function (t) {
            //this function calculates the intermediary shapes
            return path(tween(t));
        };
    };
}

function checkBoxClicked() {
  var rawCheck = document.getElementById("raw");
  var sdCheck = document.getElementById("smackdown");
  var ppvCheck = document.getElementById("ppv");
  
   
  if (ppvCheck.checked && sdCheck.checked && rawCheck.checked) {
    renderData("/wp-content/uploads/2015/05/rawmatchesphp.php?showname=All");
  }
  else if (rawCheck.checked && sdCheck.checked) {
    renderData("/wp-content/uploads/2015/05/rawmatchesphp.php?showname=RawSmackdown");
  }
  else if (ppvCheck.checked && rawCheck.checked) {
    renderData("/wp-content/uploads/2015/05/rawmatchesphp.php?showname=PPVRaw");
  }
  else if (ppvCheck.checked && sdCheck.checked) {
    renderData("/wp-content/uploads/2015/05/rawmatchesphp.php?showname=PPVSmackdown");
  }
  else if (rawCheck.checked) {
    renderData("/wp-content/uploads/2015/05/rawmatchesphp.php?showname=Raw");
  }
  else if (sdCheck.checked) {
    renderData("/wp-content/uploads/2015/05/rawmatchesphp.php?showname=Smackdown");
  }
  else if (ppvCheck.checked) {
    renderData("/wp-content/uploads/2015/05/rawmatchesphp.php?showname=PPV");
  }
  else {
    alert("none");
  }
}

</script>