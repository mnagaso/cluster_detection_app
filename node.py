class Node:
    __id = 0 # ノードID
    __moduleId = 0 # 属するモジュールのID
    __edges = [] # 接続エッジ情報リスト

class Edge:
    connectedToNodeId = 0 # 接続先のノードID
    weight = 0 # 重み
