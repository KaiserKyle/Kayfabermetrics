png("elograph.png", height=400, width=800);

# Load the winner csv file
mydata <- read.csv("c:\\python34\\winner_scores_2.csv");

# Pick the first column in vector form for input into histogram
mydata1 <- mydata[,1];
mydata2 <- mydata[,2];

# Create the histogram
histdata1 <- hist(mydata1, xlim=c(0,1), breaks=c(seq(0,1,0.05)));
histdata2 <- hist(mydata2, xlim=c(0,1), breaks=c(seq(0,1,0.05)));

print("average");
mean(mydata1);
mean(mydata2);

histvalues1 <- histdata1$breaks;
histcounts1 <- histdata1$counts;
histvalues2 <- histdata2$breaks;
histcounts2 <- histdata2$counts;

headers <- vector(mode="numeric", length=0);
values <- vector(mode="numeric", length=0);
diffs <- vector(mode="numeric", length=0);
totals <- vector(mode="numeric", length=0);
values2 <- vector(mode="numeric", length=0);
diffs2 <- vector(mode="numeric", length=0);
totals2 <- vector(mode="numeric", length=0);

for (i in 1:(length(histcounts1)/2))
{
  numRight <- histcounts1[length(histcounts1) + 1 - i];
  numRight2 <- histcounts2[length(histcounts2) + 1 - i];
  header = (histvalues1[length(histvalues1) - i] + histvalues1[length(histvalues1) - i + 1]) / 2;
  total <- histcounts1[i] + numRight;
  total2 <- histcounts2[i] + numRight2;
  percentCorrect <- numRight / total;
  percentCorrect2 <- numRight2 / total2;
  headers <- append(headers, header);
  values <- append(values, percentCorrect);
  values2 <- append(values2, percentCorrect2);
  diffs <- append(diffs, (percentCorrect - header) * total);
  totals <- append(totals, total);
  diffs2 <- append(diffs2, (percentCorrect2 - header) * total2);
  totals2 <- append(totals2, total2);
}

datatable = rbind(headers, values, values2, totals);
datatable;
#layout(rbind(c(1),c(2)), heights=c(1,1));
#layout(matrix(c(1,1), 2, 1, byrow=TRUE));
par(mfrow = c(1, 2))
df.bar <- barplot(rbind(values, values2), names.arg=headers, ylim=c(0.4,1), xpd=FALSE, col=c("darkred","darkgreen"), main="Actual Win Percentage per Bucket vs. Expected", beside=TRUE);
legend("topright", legend=c("Old","New"), fill=c("darkred","darkgreen"));
colMeans(df.bar);
lines(x = colMeans(df.bar), y = headers);
points(x = colMeans(df.bar), y = headers, col="black", bg="yellow", pch=21);
barplot(rbind(totals, totals2), names.arg=headers, ylim=c(0, 5000), col=c("darkred","darkgreen"), main="Number of Matches per Bucket", beside=TRUE);
legend("topleft", legend=c("Old","New"), fill=c("darkred","darkgreen"));

totalMatches = length(mydata)
totalMatches
sum(diffs) / totalMatches

# output histogram to disk and open it up
garbage <- dev.off();
browseURL("elograph.png");
