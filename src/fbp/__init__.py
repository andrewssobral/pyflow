"""Flow library"""
import json
import time

from .node import Node
from .flow import Flow
from .repository import repository


__version_info__ = (0, 0, 1)
__version__ = ".".join(map(str, __version_info__))


def create_node(spec_id, id, name):
    #print("create_node")
    spec = repository().get("nodespec", spec_id)
    #print("spec",spec)

    if spec is None:
        raise Exception("No such node specification {}".format(spec_id))
    #print(type(spec))
    if type(spec) is not dict:
        try:
            spec_obj = json.loads(spec, strict=False)
        except Exception as e:
            raise Exception("Invalid node specification {}".format(spec))

        anode = Node(id, name, spec_obj)
        return anode
    #print("id",id)
    #print("name",name)
    anode = Node(id, name, spec)
    #print("anode",anode)
    return anode

# Run a flow based on a defined specification of flow
# Todo consider unify the flow definition spec and running spec


def _run_flow(flow_spec):
    #print("_run_flow")
    print("flow_spec",flow_spec)
    flow_spec_obj = None

    if type(flow_spec) is not dict:
        try:
            flow_spec_obj = json.loads(flow_spec, strict=False)
        except Exception as e:
            print("invalid flow specification format")
            raise e
    else:
        flow_spec_obj = flow_spec

    #print("flow_spec_obj",flow_spec_obj)
    aflow = Flow(flow_spec_obj.get("id"), flow_spec_obj.get("name"))
    #print("aflow",aflow)

    end_node = None
    for node_def in flow_spec_obj.get("nodes"):
        #print("node_def",node_def)
        anode = create_node(node_def.get("spec_id"),
                            node_def.get("id"), node_def.get("name"))
        #print("anode",anode)
        aflow.add_node(anode)
        #print("aflow",aflow)
        if "is_end" in node_def.keys() and node_def.get("is_end") == 1:
            end_node = anode
        for port_def in node_def.get("ports"):
            anode.set_inport_value(port_def.get("name"), port_def.get("value"))
        #print("end_node",end_node)
    #print("OK")
    #print(flow_spec_obj.get("links"))
    for link_def in flow_spec_obj.get("links"):
        #print("link_def",link_def)
        source = link_def.get("source").split(":")
        target = link_def.get("target").split(":")

        aflow.link(source[0], source[1], target[0], target[1])

    #print("end_node",end_node)
    stats = aflow.run(end_node)
    #print("stats",json.dumps(stats))

    return stats


def run_flow(flow_spec):
    stats = _run_flow(flow_spec)
    # TODO : support run in async mode
    while not stats.check_stat():
        time.sleep(0.1)
    return [i for i in stats.result()]
