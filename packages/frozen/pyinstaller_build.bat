
REM Frozen BookMate under Windows platform

C:\Python27\Scripts\pyinstaller -w  ..\..\src\bookmate.py
xcopy ..\..\src\images dist\bookmate\images\
copy ..\..\src\bookmate.cfg dist\bookmate\
rd /q /s build
del /q bookmate.spec

md dist\doc
copy ..\..\doc\user_notes dist\doc\user_notes.txt
copy ..\..\README dist\doc\README.txt
move dist bookmate-win

del /q bookmate-win.tar.gz
REM "C:\Program Files\7-Zip\7z.exe" a -r bookmate-win.zip bookmate-win
REM "C:\Program Files (x86)\7-Zip\7z.exe" a -r bookmate-win.zip bookmate-win
7z.exe a -r bookmate-win.zip bookmate-win
rd /s /q bookmate-win

