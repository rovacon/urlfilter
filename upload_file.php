<?php
if (($_FILES["file"]["type"] == "text/plain") && ($_FILES["file"]["size"] < 1841975))
  {
  if ($_FILES["file"]["error"] > 0)
    {
    echo "Return Code: " . $_FILES["file"]["error"] . "<br />";
    }
  else
    {
    echo "Upload: " . $_FILES["file"]["name"] . "<br />";
    echo "Type: " . $_FILES["file"]["type"] . "<br />";
    echo "Size: " . ($_FILES["file"]["size"] / 1024) . " Kb<br />";
    echo "Temp file: " . $_FILES["file"]["tmp_name"] . "<br />";

    if (file_exists("upload/" . $_FILES["file"]["name"]))
      {
      echo $_FILES["file"]["name"] . " already exists. ";
      }
    else
      {
         if (move_uploaded_file($_FILES["file"]["tmp_name"],"/home/nemo/luohg/phantomjs-1.9.7-linux-i686/urllist.txt"))
         {echo "Stored in: " . "urllist.txt";}
      }
    }
  }
else
  {
  echo "Invalid file";
  }
exec("cd /home/nemo/luohg/phantomjs-1.9.7-linux-i686;./needrun.sh >log.log 2>&1")
?>
