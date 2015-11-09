<?php
error_reporting(E_ALL ^ E_NOTICE);
date_default_timezone_set('UTC');

// Get ID from page
$id = 1134;
$id = $_GET['ID'];
$name = '';
$othernames = '';
$currentELO = 0;
$lastMatch = '';
$nummatches = 0;
$wins = 0;
$losses = 0;
$draws = 0;

include 'sqldata.php';

$usertable="wrestlers_temp";
$elotable="ELO_ratings";

$link = mysqli_connect($hostname,$username, $password, $dbname);

# Check If Record Exists

$query = "SELECT * FROM $usertable WHERE ID = $id";
//echo $query;
$result = mysqli_query($link, $query);

if($result)
{
    while($row = mysqli_fetch_array($result))
    {
        if ($row["IsPrimary"] == 1)
        {
            $name = $row["Name"];
        }
        else
        {
            $othernames += $row["Name"] + '; ';
        }
    }
}

$query = "SELECT * FROM $elotable WHERE wrestlerid = $id ORDER BY epochtime DESC LIMIT 10";
$result = mysqli_query($link, $query);
if ($result)
{
    while($row = mysqli_fetch_array($result))
    {
        if (0 == $currentELO)
        {
            $currentELO = round($row['rating'], 0);
        }
        if ('' == $lastMatch)
        {
            $lastMatch = date("F j, Y", $row['epochtime']);
        }
    }
}

$query = "SELECT result, COUNT(*) AS count FROM $elotable WHERE wrestlerid = $id GROUP BY result";
$result = mysqli_query($link, $query);
if ($result)
{
    while($row = mysqli_fetch_array($result))
    {
        $nummatches += $row[1];
        if ("W" == $row[0])
        {
            $wins = $row[1];
        }
        else if ("L" == $row[0])
        {
            $losses = $row[1];
        }
        else
        {
            $draws = $row[1];
        }
    }
}

echo "<div class=\"page-template-normal single-template-1\">";
echo "<h2 class=\"title\">" . $name . "</h2>";
if ('' != $othernames)
{
    echo "Also known as: " . $othernames;
}
echo "<h2 class = \"title\">" . $wins . "-" . $losses . "-" . $draws . "</h2>";
echo "<span>Last Match: " . $lastMatch . "</span><br>";
echo "<span>Total number of matches: " . $nummatches . "</span><br>";
echo "</div>";
echo "<div class=\"bigbox\" style=\"background-color:#3300CC;\">Current Elo Rating:<br><span style=\"font-size:75px;display:inline-block;line-height:150px\">" . $currentELO . "</span></div>";
?>