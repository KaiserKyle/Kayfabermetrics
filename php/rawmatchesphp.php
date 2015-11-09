<?php
//Sample Database Connection Syntax for PHP and MySQL.
//Connect To Database
error_reporting(E_ALL ^ E_NOTICE);
date_default_timezone_set('UTC');

$showname = $_GET['showname'];
if (null === $showname)
{
  $showname = 'Raw';
}

$showfilter = '';
if ('Raw' == $showname)
{
  $showfilter = "show_name LIKE '%Raw%'";
}
else if ('Smackdown' == $showname)
{
  $showfilter = "show_name LIKE '%Smackdown%'";
}
else if ('RawSmackdown' == $showname)
{
  $showfilter = "(show_name LIKE '%Raw%' OR show_name LIKE '%Smackdown%')";
}
else if ('PPV' == $showname)
{
  $showfilter = "ppv = 'yes'";
}
else if ('PPVRaw' == $showname)
{
  $showfilter = "(show_name LIKE '%Raw%' OR ppv = 'yes')";
}
else if ('PPVSmackdown' == $showname)
{
  $showfilter = "(show_name LIKE '%Smackdown%' OR ppv = 'yes')";
}
else if ('All' == $showname)
{
  $showfilter = "(show_name LIKE '%Raw%' OR show_name LIKE '%Smackdown%' OR ppv = 'yes')";
}

$epochtime =  time();
$oneyear = 365 * 24 * 60 * 60;
$lastyear = $epochtime - $oneyear;

//echo date(DATE_RFC2822, $lastyear / 1000);

$namereplace  = array('Xavier' => 'Xavier Woods',
               'Adrian Neville' => 'Neville',
               'AJ' => 'A. J. Lee',
               'R-Ziggler'=>'R-Truth',
               'Alexander Rusev'=>'Rusev',
               'Damien Sandow'=>'Damien Mizdow',
               'Papi C'=>'Local Jobbers',
               'Socorro'=>'Local Jobbers',
               'Bu Ku Dao'=>'Local Jobbers',
               'Kevin Kross'=>'Local Jobbers',
               'Mad 1' => 'Local Jobbers',
               "Lance Anoa'i" => 'Local Jobbers',
               'Spartan' => 'Local Jobbers',
               'Rhett Titus' => 'Local Jobbers',
               'Titan'=>'Local Jobbers',
               'Tamina Snuka' => 'Tamina',
               'Bad News Barrett' => 'Wade Barrett',
               'King Barrett' => 'Wade Barrett');

$matchcount = array();
//$datelist = array();

include 'sqldata.php';

$usertable="wwematches2";
$yourfield = "match_link";

$link = mysqli_connect($hostname,$username, $password, $dbname);

# Check If Record Exists

$query = "SELECT * FROM $usertable WHERE $showfilter AND epochtime > $lastyear AND match_type != 'dark'";
//echo $query;
$result = mysqli_query($link, $query);

if($result)
{
  //echo "<h3>" + mysqli_num_rows($result) + "</h3>";
 while($row = mysqli_fetch_array($result))
  {
    //if (!in_array($row["epochdate"], $datelist))
    //{
    //  array_push($datelist, $row["epochdate"]);
    //}
    $winners = explode("; ", $row["match_link"]);
    $losers = explode("; ", $row["match_3_link"]);
    foreach($winners as &$winner)
    {
      if (array_key_exists($winner, $namereplace))
      {      
        $winner = $namereplace[$winner];
      }
      if (array_key_exists($winner, $matchcount))
      {
        $matchcount[$winner]++;
      }
      else
      {
        $matchcount[$winner] = 1;
      }
    }
    foreach($losers as &$winner)
    {
      if (array_key_exists($winner, $namereplace))
      {
        $winner = $namereplace[$winner];
      }
      if (array_key_exists($winner, $matchcount))
      {
        $matchcount[$winner]++;
      }
      else
      {
        $matchcount[$winner] = 1;
      }
    }
  }
  arsort($matchcount);
  $numwrestlers = count($matchcount);
  $wrestlerlist = array_keys($matchcount);
  //echo $wrestlerlist;
  //echo var_dump($matchcount);
  //echo json_encode($matchcount);
  //arsort($datelist);
  //foreach ($datelist as &$dater)
  //{
  //  echo "<p>".date(DATE_RFC2822, $dater / 1000)."</p>";
  //}
  
  $winsmatrix = array_fill(0, $numwrestlers, array_fill(0, $numwrestlers, 0));
  $matchmatrix = array_fill(0, $numwrestlers, array_fill(0, $numwrestlers, 0));
  
  mysqli_data_seek($result, 0);
  while($row = mysqli_fetch_array($result))
  {  
    $winners = explode("; ", $row["match_link"]);
    $losers = explode("; ", $row["match_3_link"]);
    foreach($winners as &$winner)
    {
      if (array_key_exists($winner, $namereplace))
      {      
        $winner = $namereplace[$winner];
      }
      foreach($losers as &$loser)
      {
        if (array_key_exists($loser, $namereplace))
        {
          $loser = $namereplace[$loser];
        }
        //echo "$winner def $loser";
        $winnerindex = array_search($winner, $wrestlerlist);
        $loserindex = array_search($loser, $wrestlerlist);
        if ( FALSE === $winnerindex || FALSE === $loserindex)
        {
          echo "Not found";
        }
        else
        {
          if (strpos($row["match_2"], 'draw') === false)
          { 
            $winsmatrix[$winnerindex][$loserindex] += 1;
          }
          $matchmatrix[$winnerindex][$loserindex] += 1;
          $matchmatrix[$loserindex][$winnerindex] += 1;
        }
      }
    }
  }
  
  //echo json_encode($winsmatrix);
  //echo json_encode($matchmatrix);
  $indexedmatchcount = array();
  $index = 0;
  foreach($matchcount as $key => $value)
  {
    $indexedmatchcount[$index] = array ('name' => $key, 'nummatches' => $value);
    $index++;
  }
  
  $jsonobject = array($indexedmatchcount, $winsmatrix, $matchmatrix);
  echo json_encode($jsonobject);
}
else
{
  //echo "No result";
}
?>
 
