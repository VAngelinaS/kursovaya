rem ��������� ������� ����
for /f "tokens=1-4 delims=/-\. " %%a in ('date /t') do (
set day=%%a
set month=%%b
set year=%%c
)
rem ��� ������ ����� ��������� ������� ����
set mydate=%year%%month%%day%
set dbname="kino"
 
c:\xampp\mysql\bin\mysqldump.exe -uroot -hlocalhost %dbname% >%dbname%_%mydate%.sql -vvv
