# coding:utf-8
# 用于生成neo4j图数据库数据
from py2neo import Graph, Node, Relationship
import re

# 连接neo4j数据库，输入地址、用户名、密码
graph = Graph('http://localhost:7474', auth=("neo4j", "test"))
graph.delete_all()


def CreateReport(PhoneReport, CalculatorConfig, PhoneSupportComb):
    node_CombCap = Node('CombCap', name="CombCap")
    graph.create(node_CombCap)

    node_task_all = Node('TaskAll', name="TaskAll")
    graph.create(node_task_all)
    graph.create(Relationship(node_CombCap, 'embody', node_task_all))
    for task in PhoneReport.keys():
        node_task = Node('Task', name=task)
        graph.create(node_task)
        graph.create(Relationship(node_task_all, 'embody', node_task))
        for rpt in PhoneReport[task].keys():
            node_rpt = Node('Rpt', name=rpt)
            graph.create(node_rpt)
            graph.create(Relationship(node_task, 'embody', node_rpt))
            for i in range(len(PhoneReport[task][rpt]["CellGpID"])):
                cell_gp_id = PhoneReport[task][rpt]["CellGpID"][i]
                node_cell_gp_id = Node('CellGpID', name=cell_gp_id)
                graph.create(node_cell_gp_id)

                cell_id = PhoneReport[task][rpt]["CellID"][i]
                node_cell_id = Node('CellID', name=cell_id)
                graph.create(node_cell_id)

                cell_rslt = PhoneReport[task][rpt]["CellRslt"][i]
                node_cell_rslt = Node('CellRslt', name=cell_rslt)
                graph.create(node_cell_rslt)

                graph.create(Relationship(node_rpt, 'embody', node_cell_gp_id))
                graph.create(Relationship(
                    node_cell_gp_id, 'independence', node_cell_id))
                graph.create(Relationship(
                    node_cell_id, 'independence', node_cell_rslt))

    node_gp_id_all = Node('GpID', name="GpID")
    graph.create(node_gp_id_all)
    graph.create(Relationship(node_CombCap, 'embody', node_gp_id_all))
    for gp_id in CalculatorConfig.keys():
        node_gp_id = Node('gp_id', name=gp_id)
        graph.create(node_gp_id)
        graph.create(Relationship(node_gp_id_all, 'embody', node_gp_id))
        for i in range(len(CalculatorConfig[gp_id]["CellID"])):
            cell_id = CalculatorConfig[gp_id]["CellID"][i]
            node_cell_id = Node('CellID', name=cell_id)
            graph.create(node_cell_id)

            bw = CalculatorConfig[gp_id]["Bw"][i]
            node_bw = Node('Bw', name=bw)
            graph.create(node_bw)

            layer = CalculatorConfig[gp_id]["Layer"][i]
            node_layer = Node('Layer', name=layer)
            graph.create(node_layer)

            graph.create(Relationship(node_gp_id, 'embody', node_cell_id))
            graph.create(Relationship(
                node_cell_id, 'independence', node_bw))
            graph.create(Relationship(
                node_bw, 'independence', node_layer))

    node_comb_all = Node('Comb', name="Comb")
    graph.create(node_comb_all)
    graph.create(Relationship(node_CombCap, 'embody', node_comb_all))
    for comb in PhoneSupportComb.keys():
        node_comb = Node('comb', name=comb)
        graph.create(node_comb)
        graph.create(Relationship(node_comb_all, 'embody', node_comb))
        for i in range(len(PhoneSupportComb[comb]["CellGpID"])):
            cell_gp_id = PhoneSupportComb[comb]["CellGpID"][i]
            node_cell_gp_id = Node('CellGpID', name=cell_gp_id)
            graph.create(node_cell_gp_id)
            graph.create(Relationship(node_comb, 'embody', node_cell_gp_id))
            support_bw = PhoneSupportComb[comb]["SupportBw"][i]
            node_support_bw_i_list = []
            for support_bw_i in support_bw:
                node_support_bw_i = Node('SupportBw', name=support_bw_i)
                graph.create(node_support_bw_i)
                graph.create(Relationship(
                    node_cell_gp_id, 'independence', node_support_bw_i))
                node_support_bw_i_list.append(node_support_bw_i)
            support_layer = PhoneSupportComb[comb]["SupportLayer"][i]
            for support_layer_i in support_layer:
                node_support_layer_i = Node(
                    'SupportLayer', name=support_layer_i)
                graph.create(node_support_layer_i)
                for node_support_bw_i in node_support_bw_i_list:
                    graph.create(Relationship(
                        node_support_bw_i, 'independence', node_support_layer_i))


def CreateData():
    PhoneReport, CalculatorConfig, PhoneSupportComb = {}, {}, {}
    PhoneReport["Task1"] = {"Rpt1": {"CellGpID": [1, 1], "CellID": [11, 12], "CellRslt": [10, 8]},
                            "Rpt2": {"CellGpID": [2], "CellID": [22], "CellRslt": [20]},
                            "Rpt3": {"CellGpID": [4], "CellID": [41], "CellRslt": [9]}}
    CalculatorConfig = {1: {"CellID": [11, 12], "Bw": [20, 20], "Layer": [4, 2]},
                        2: {"CellID": [21, 22], "Bw": [15, 15], "Layer": [4, 4]},
                        4: {"CellID": [41], "Bw": [5], "Layer": [2]}}
    PhoneSupportComb = {"Comb1": {"CellGpID": [1, 2, 4], "SupportBw": [[20, 15], [15, 10], [20, 5]], "SupportLayer": [[2], [2], [2]]},
                        "Comb2": {"CellGpID": [2, 1], "SupportBw": [[15, 10], [20, 15]], "SupportLayer": [[4, 2], [4, 2]]}}
    return PhoneReport, CalculatorConfig, PhoneSupportComb


PhoneReport, CalculatorConfig, PhoneSupportComb = CreateData()
CreateReport(PhoneReport, CalculatorConfig, PhoneSupportComb)
