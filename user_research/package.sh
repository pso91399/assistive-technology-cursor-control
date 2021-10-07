filename=$1
name=${filename%.py}
pyinstaller --noconsole --onefile --add-data="modules;mediapipe/modules" $filename
mv dist/$name.exe .
rm -r dist
rm -r build
rm -r __pycache__
rm $name.spec
echo Created $name.exe
