cd ../

rm -rf build/*

pyinstaller --onefile client.py
pyinstaller --onefile server.py

rm -rf build/*

mv dist/client build
mv dist/server build
cp -r assets build/assets

mkdir -p build/configs

echo '{
  "ip": "0.0.0.0",
  "port": 1289
}' > build/configs/host.json

rm client.spec
rm server.spec
rm -r dist