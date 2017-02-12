クラスタ構造解析アプリケーション(ver0.9)

---

# ファイル構成

- README.md : セットアップ説明ドキュメント
- config.py : 設定ファイル
- enot_main.py : 実行メインスクリプト
- data/ : 入力データ、出力データ用ディレクトリ
	

# クラスタリング実行方法

config.py で設定した後に以下のコマンドで実行して下さい。

```python enot_main.py
```

出力結果はconfig.pyで指定されたファイルとして出力されます。

## config.py

- infile_path : 入力データCSV のパス。データフォーマットは遷移の重さで表し、 [source node id, target node id, weight] で表現(Link list format) *
- infile_directed_type : 入力データの指向性タイプ *
	- 1 : 指向性
	- 2 : 無指向性
- vertices_file_path : ノード名を定義したファイル *
- total_nodes : 全ノード数 *
- outfile : 出力ファイル名
- p_algo_type : Pαの算出方法
	- 1 : Power method
	- 2 : Arnoldi method
- p_conv_threshold : Power methodに於けるPαの収束しきい値 (Rosvall(2010)では 1.0e-15)
- 



# 実行結果

## 出力ファイル



## 可視化HTML


# 入力データフォーマット

# 新規手法の導入方法

1.quarity.py内の__new__関数内に新たな分岐をつくる

```
def __new__(cls):
	if cf.quality_method == 1: # use map equation for communities' quality estimation
    	import mapequation as mp
       new_cls = mp.Map
	elif cf.quality_method == 2: # use modularity for communities' quality estimation
		import modularity as ml
       new_cls = ml.Modularity
   	elif cf.quality_method == 3: #新規評価方法に対して、新しい番号をふる。config,py内 quality_methodの値に対応。
   		import someNewMethod as sn
   		new_cls = sn.someNewMethod
  	else:
   		print("error: in config.py, undefined number of quality_method was selected.")
   		sys.exit(1)
```

2.評価式を実装するモジュール(.py)をlibフォルダ内に作成

実装に求められること:
bool check_network_got_better(self, ql_before, ql_after)
bool check_network_converged(self, ql_before, ql_after)
float get_quality_value(self, __modules, w, p_a)
の３つの関数が必要。
実際に実装する場合は、util/someNewMethod.pyにサンプルファイルを用意したのでこれを修正、libフォルダに移動して使用する。


---

# 変更点

### ver 0.9 

- MapEquation と Modurarity によるクラスタ構造解析処理実装
- クラスタリング結果可視化処理実装
