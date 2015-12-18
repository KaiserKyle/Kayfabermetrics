png("elograph.png", height=800, width=400);

# Load the winner csv file
mydata <- read.csv("c:\\python34\\winner_scores.csv");

# Pick the first column in vector form for input into histogram
mydata <- mydata[,1];

# Create the histogram
histdata <- hist(mydata, xlim=c(0,1), breaks=c(seq(0,1,0.05)));

histvalues <- histdata$breaks;
histcounts <- histdata$counts;

headers <- vector(mode="numeric", length=0);
values <- vector(mode="numeric", length=0);
diffs <- vector(mode="numeric", length=0);
totals <- vector(mode="numeric", length=0);

for (i in 1:(length(histcounts)/2))
{
  numRight <- histcounts[length(histcounts) + 1 - i];
  header = (histvalues[length(histvalues) - i] + histvalues[length(histvalues) - i + 1]) / 2;
  total <- histcounts[i] + numRight;
  percentCorrect <- numRight / total;
  headers <- append(headers, header);
  values <- append(values, percentCorrect);
  diffs <- append(diffs, (percentCorrect - header) * total);
  totals <- append(totals, total);
}

datatable = rbind(headers, values, totals);
datatable;
layout(rbind(c(1),c(2)), heights=c(1,1));
df.bar <- barplot(values, names.arg=headers, ylim=c(0.4,1), xpd=FALSE);
lines(x = df.bar, y = headers);
points(x = df.bar, y = headers);
barplot(totals, names.arg=headers, ylim=c(0, 5000));

totalMatches = length(mydata)
totalMatches
sum(diffs) / totalMatches

# output histogram to disk and open it up
garbage <- dev.off();
browseURL("elograph.png");
