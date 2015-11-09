<?php
error_reporting(E_ALL ^ E_NOTICE);
date_default_timezone_set('UTC');

include 'sqldata.php';

$usertable="SankeyData";
$fedtable = "Federations";
$elotable="ELO_ratings";

$link = mysqli_connect($hostname,$username, $password, $dbname);

//$query = "SELECT wrestlers_temp.Name, Federations.Name, Federations.Abbr, SankeyData.FedID, SankeyData.Dates, f2.Name AS DestName, f2.Abbr AS DestAbbr, SankeyData.DestID FROM SankeyData LEFT JOIN Federations ON SankeyData.FedID=Federations.ID
//LEFT JOIN wrestlers_temp ON SankeyData.WrestlerID=wrestlers_temp.RecordID
//LEFT JOIN Federations f2 ON SankeyData.DestID=f2.ID";
//echo $query;
$query = "SELECT FedID, DestID, COUNT(*) AS Count FROM SankeyData GROUP BY FedID, DestID";
$sankeyresult = mysqli_query($link, $query);

$query = "SELECT * FROM Federations";
$fedresult = mysqli_query($link, $query);

$sankeyjson = array();
$fedarray = array();
$sankeyarray = array();

if ($fedresult)
{
    $index = 0;
    while($row = mysqli_fetch_array($fedresult))
    {
        $fedarray[$index] = array("name" => $row['Abbr'], "fullname" => $row['Name']);
        $index++;
    }
}
$sankeyjson[0] = array("nodes" => $fedarray);

if($sankeyresult)
{
    $index = 0;
    while($row = mysqli_fetch_array($sankeyresult))
    {
        $sankeyarray[$index] = array("source" => (int)$row['FedID'], "target" => (int)$row['DestID'], "value" => (int)$row['Count']);
        $index++;
    }
}

$sankeyjson[1] = array("links" => $sankeyarray);

echo json_encode($sankeyjson);
?>