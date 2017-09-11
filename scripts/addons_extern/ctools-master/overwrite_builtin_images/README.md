# blender-OverwriteBuiltinImages
blenderのスプラッシュとアイコンの画像を変更する為のpythonスクリプト  

## overwrite_builtin_images.py
バイナリを書き換えるスクリプト。Windows / Linux  

1. overwrite_builtin_images.pyと下記の画像をblenderの実行ファイル(blender.exe)と同じフォルダに配置。  
  * splash.png (501x282)
  * splash_2x.png (1002x564)
  * icons16.png (602x640)
  * icons32.png (1204x1280)

  変更する画像だけ用意すればいい。  
  フォーマットは png, jpeg, jpeg2000, tiff が使用可。  
  拡張子は '.png', '.jpg', '.jpeg', '.jpe', '.tif', '.tiff', '.jp2', '.jpc', '.j2k' 。  
  圧縮率と透過を扱えるという点でjpeg2000を推奨。(blenderが対応しているか確認しておくこと)

2. コマンドプロンプト(端末)からスクリプトを実行して書き換える。  
`python3 overwrite_builtin_images.py`


* 埋め込まれた元画像よりファイルサイズが大きい物は使用出来ない。  

* `--extract`オプションを付けて実行すると現在使用している画像が splash_builtin.png, splash_2x_builtin.png, icons16_builtin.png, icons32_builtin.png として出力される。  
`python3 overwrite_builtin_images.py --extract`  

## wm_overwrite_builtin_images.py
Linux専用のアドオン  
blender起動中にctypesでメモリ上の値を変更する。
