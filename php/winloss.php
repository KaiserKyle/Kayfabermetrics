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

include 'sqldata.php';

$usertable="wrestlers_temp";
$elotable="ELO_ratings";

$link = mysqli_connect($hostname,$username, $password, $dbname);

# Check If Record Exists

$names = array();
$data = array();

$query = "SELECT * FROM $usertable WHERE ID = $id";
//echo $query;
$result = mysqli_query($link, $query);

if($result)
{
    while($row = mysqli_fetch_array($result))
    {
        array_push($names, $row["Name"]);
    }
}

$query = "SELECT $elotable.result, $elotable.subresult, COUNT(*) AS count FROM $elotable WHERE $elotable.wrestlerid = $id GROUP BY $elotable.result, $elotable.subresult";
$result = mysqli_query($link, $query);
if ($result)
{
    while($row = mysqli_fetch_array($result))
    {
        $found = false;
        foreach($data as &$datum)
        {
            if ($datum["name"] == $row[1])
            {
                foreach($datum["data"] as &$resulttype)
                {
                    if ($resulttype["result"] == $row[0])
                    {
                        $resulttype["count"] = $row[2];
                    }
                    unset($resulttype);
                }
                $found = true;
            }
            unset($datum);
        }
        if (!$found)
        {
            $datum = ["name" => $row[1], "data" => array()];
            $results = ["result" => "W", "count" => 0];
            array_push($datum["data"], $results);
            $results = ["result" => "L", "count" => 0];
            array_push($datum["data"], $results);
            $results = ["result" => "D", "count" => 0];
            array_push($datum["data"], $results);
            foreach($datum["data"] as &$resulttype)
            {
                if ($resulttype["result"] == $row[0])
                    {
                        $resulttype["count"] = $row[2];
                    }
                unset($resulttype);
            }
            $data[] = $datum;
        }
    }
}
else
{
    echo mysqli_error($link);
}
echo json_encode($data);
?>