# macOS
mkdir icon.iconset

sips -z 16 16     input.png --out icon.iconset/icon_16x16.png
sips -z 32 32     input.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     input.png --out icon.iconset/icon_32x32.png
sips -z 64 64     input.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   input.png --out icon.iconset/icon_128x128.png
sips -z 256 256   input.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   input.png --out icon.iconset/icon_256x256.png
sips -z 512 512   input.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   input.png --out icon.iconset/icon_512x512.png
cp input.png                icon.iconset/icon_512x512@2x.png

iconutil -c icns icon.iconset -o plastl.icns
rm -rf icon.iconset

# Windows
convert input.png -define icon:auto-resize=256,128,64,48,32,16 plastl.ico