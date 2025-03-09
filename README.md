# VRMNXついてくん

## 概要
「ついてくん」は「[鉄道模型シミュレーターNX](http://www.imagic.co.jp/hobby/products/vrmnx/ "鉄道模型シミュレーターNX")」（VRMNX）の編成自動追尾スクリプトです。

## ダウンロード
- [follow_train.py](https://raw.githubusercontent.com/CaldiaNX/vrmnx-follow_train/main/follow_train.py)

## 利用方法
レイアウトファイルと同じフォルダ階層に「follow_train.py」ファイルを配置します。  

フォルダ構成：
```
C:\VRMNX（一例）
├ follow_train.py
└ VRMNXレイアウトファイル.vrmnx
```

自動追尾したい編成スクリプトに以下の★内容を追記します。  

```py
import vrmapi
import follow_train # ★スクリプトインポート

def vrmevent(obj,ev,param):
    follow_train.vrmevent(obj,ev,param) # ★ メインスクリプト
    if ev == 'init':
        dummy = 1
# (省略) #
```

ファイル読み込みに成功するとビュワー起動直後にスクリプトログへ下記メッセージが表示されます。

```
import ついてくん Ver.x.x
```

## 利用方法
「ついてくん」は前方に居る編成に対して最小距離から最大距離の間で自動追尾します。  
VRMNXスクリプトの「SearchForwardTrainID」を利用して以下の動作を毎フレーム判断します。

|前方編成との距離|動作|
|----------------|----|
|最大距離 以上   |最高速度で走行|
|最大～最小距離  |最小距離で現行速度から0.9倍で減速|
|最小距離 未満   |最小距離÷2の距離で停止。最大距離以上離れると再度走行|

### 標準距離を変更
スクリプトの標準距離は最小距離(標準60.0mm)と最大距離(標準100.0mm)です。  
変更する場合は「follow_train.py」の以下★を変更してください。  
最小距離と最大距離が小さければ精度高く追尾し、大きいとばらつきのある速度で追尾します。

```py
# main
def vrmevent(obj,ev,param):
    if ev == 'init':
        # 初期化
        di = obj.GetDict()
        di['ft_search_min'] = 60.0  #★最小距離
        di['ft_search_max'] = 100.0 #★最大距離
```

### 距離を自分で定義（vrmevent_init）
編成ごとに標準距離以外で追尾する場合は編成スクリプトに「vrmevent」ではなく「vrmevent_init」を記載して引数を定義してください。  
距離の数値はfloatです。

```py
def vrmevent(obj,ev,param):
    # ★最小距離100.0mm、最大距離200.0mmで追尾させる場合
    follow_train.vrmevent_init(obj,ev,param,100.0,200.0)
    if ev == 'init':
        dummy = 1
# (省略) #
```
