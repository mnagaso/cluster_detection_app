class Module:
    __module_id = 0 # ノードID
    __belongs_to_module_id = 0 # 属するモジュールのID
    
    def __init__(self, module_id):
        print("generate module : " + str(module_id))
        self.__module_id = module_id

    def include_node(self, node):
        node.set_module_id(self.__module_id)
