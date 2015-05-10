
REM Frozen BookMate under Windows platform

C:\Python27\Scripts\pyinstaller -w  ..\..\src\bookmate.py
copy ..\..\src\images dist\bookmate\
rd /q /s build
del /q bookmate.spec

md dist\doc
copy ..\..\doc\user_notes dist\doc\user_notes.txt
copy ..\..\README dist\doc\README.txt
move dist bookmate-win

del /q bookmate-win.tar.gz
"C:\Program Files\7-Zip\7z.exe" a -r bookmate-win.zip bookmate-win
rd /s /q bookmate-win

