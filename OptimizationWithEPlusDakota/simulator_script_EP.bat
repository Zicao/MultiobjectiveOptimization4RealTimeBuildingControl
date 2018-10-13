rem  PRE-PROCESSING


python %~dp0/inputfilter.py %1% in.idf work.idf

rem COPY ros.idf %~dp0\work.idf

python %~dp0\runEPlusScript.py


rem  ---------------
rem  POST-PROCESSING 
rem  ---------------


python %~dp0writeoutput.py work.csv workTable.csv results.out

rem ren results.tmp %2%
