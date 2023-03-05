# -*- coding: utf-8 -*-
from py2neo import Node, Graph, Relationship
from ltp_data import ltp_data

class DataToNeo4j(object):
    """将excel中数据存入neo4j"""

    def __init__(self):
        """建立连接"""
        link = Graph("http://localhost:7474/", username="neo4j", password="leobewin1")
        self.graph = link
        # self.graph = NodeMatcher(link)
        self.graph.delete_all()

    def create_node(self, name_node, type_node):
        """创建节点"""
        nodes = []
        for i in range(len(name_node)):
            node = Node(type_node[i], name = name_node[i])
            self.graph.create(node)
            nodes.append(node)

        print('节点创建成功')
        return nodes


    def create_relation(self, rel):
        """创建联系"""
        for triple in rel:
            try:
                # 关系要转化成字符串格式
                r = Relationship(triple[0],str(triple[2]),triple[1])
                self.graph.create(r)
            except AttributeError as e:
                print(e)

        print('关系创建成功')

def node_extraction(seg, pos):
    """从语义依存图中提取出节点的名字和节点类型"""
    seg[0] = [str(i) for i in seg[0]]
    pos[0] = [str(i) for i in pos[0]]

    return seg[0], pos[0]

def relation_extraction(sdp,nodes):
    pass
    """
    提取出节点间的关系，将节点与关于整合成三元组，并存放在列表中。
    （node1,node2,relation)
    """
    rel = []
    for tuple in sdp[0]:
        # 根据索引提取出节点和关系
        index1 = int(tuple[0]) - 1
        index2 = int(tuple[1]) - 1
        node1 = nodes[index1]
        node2 = nodes[index2]
        relation = str(tuple[2])

        # 将节点和关系添加到3元组中
        triple = []
        triple.append(node1)
        triple.append(node2)
        triple.append(relation)

        # 将3元组整合到列表中
        rel.append(triple)
    return rel

if __name__ == '__main__':
    sdp, pos, seg = ltp_data()
    create_data = DataToNeo4j()

    # 建立节点
    node_name, node_type = node_extraction(seg, pos)
    nodes = create_data.create_node(node_name, node_type)

    # 建立联系
    rel = relation_extraction(sdp, nodes)
    create_data.create_relation(rel)
