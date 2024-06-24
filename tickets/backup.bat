rem формирует текущую дату
for /f "tokens=1-4 delims=/-\. " %%a in ('date /t') do (
set day=%%a
set month=%%b
set year=%%c
)
rem имя архива будет содержать текущую дату
set mydate=%year%%month%%day%
set dbname="kino"
 
c:\xampp\mysql\bin\mysqldump.exe -uroot -hlocalhost %dbname% >%dbname%_%mydate%.sql -vvv
