class Node:
    __node_id = 0 # ノードID
    __belongs_to_module_id = 0 # 属するモジュールのID
    
    def __init__(self, node_id):
        print("generate node : " + str(node_id))
        self.__node_id = node_id

    def set_module_id(self, module_id):
        self.__belongs_to_module_id = module_id


