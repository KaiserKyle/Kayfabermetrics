png("elograph.png", height=400, width=800);

# Load the winner csv file
mydata <- read.csv("c:\\python34\\winner_scores_2.csv");

# Pick the first column in vector form for input into histogram
mydata1 <- mydata[,1];

# Create the histogram
histdata1 <- hist(mydata1, xlim=c(0,1), breaks=c(seq(0,1,0.05)));

print("average");
mean(mydata1);

histvalues1 <- histdata1$breaks;
histcounts1 <- histdata1$counts;

headers <- vector(mode="numeric", length=0);
values <- vector(mode="numeric", length=0);
diffs <- vector(mode="numeric", length=0);
totals <- vector(mode="numeric", length=0);

for (i in 1:(length(histcounts1)/2))
{
  numRight <- histcounts1[length(histcounts1) + 1 - i];
  header = (histvalues1[length(histvalues1) - i] + histvalues1[length(histvalues1) - i + 1]) / 2;
  total <- histcounts1[i] + numRight;
  percentCorrect <- numRight / total;
  headers <- append(headers, header);
  values <- append(values, percentCorrect);
  diffs <- append(diffs, (percentCorrect - header) * total);
  totals <- append(totals, total);
}

datatable = rbind(headers, values, totals);
datatable;
#layout(rbind(c(1),c(2)), heights=c(1,1));
#layout(matrix(c(1,1), 2, 1, byrow=TRUE));
par(mfrow = c(1, 2))
df.bar <- barplot(values, names.arg=headers, ylim=c(0.4,1), xpd=FALSE, col=c("darkblue"), main="Actual Win Percentage per Bucket vs. Expected", beside=TRUE);
#legend("topright", legend=c("Old","New"), fill=c("darkred","darkgreen"));
lines(x = df.bar, y = headers);
points(x = df.bar, y = headers, col="black", bg="yellow", pch=21);
barplot(totals, names.arg=headers, ylim=c(0, 5000), col=c("darkblue"), main="Number of Matches per Bucket", beside=TRUE);
#legend("topleft", legend=c("Old","New"), fill=c("darkred","darkgreen"));

totalMatches = length(mydata)
totalMatches
sum(diffs) / totalMatches

# output histogram to disk and open it up
garbage <- dev.off();
browseURL("elograph.png");
