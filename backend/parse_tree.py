import re
import json

def get_level(line):
    count = 0
    while line.startswith("|   "):
        count += 1
        line = line[4:]
    return count

def clean_line(line):
    cleaned = re.sub(r"^(?:\| {3})*\|---\s*", "", line)
    return cleaned.strip()

def parse_node(content):
    leaf_match = re.match(r"^class:\s*([\d\.]+)$", content)
    if leaf_match:
        return {"class": float(leaf_match.group(1))}
    
    decision_match = re.match(r"^(.*?)\s*(<=|>)\s*([\d\.]+)$", content)
    if decision_match:
        feature = decision_match.group(1).strip()
        operator = decision_match.group(2)
        threshold = float(decision_match.group(3))
        return {"feature": feature, "operator": operator, "threshold": threshold, "children": []}

    return {"content": content}

def parse_tree(text):
    lines = text.strip().split("\n")
    top_nodes = []  
    stack = []      
    
    for line in lines:
        if not line.strip():
            continue
        level = get_level(line)
        content = clean_line(line)
        node = parse_node(content)
        
        if level == 0:
            stack = [(0, node)]
            top_nodes.append(node)
        else:
            while stack and stack[-1][0] >= level:
                stack.pop()
            if stack:
                parent = stack[-1][1]
                if "children" not in parent:
                    parent["children"] = []
                parent["children"].append(node)
            else:
                top_nodes.append(node)
            stack.append((level, node))
    
    if len(top_nodes) == 1:
        return top_nodes[0]
    else:
        return {"name": "Root", "children": top_nodes}

if __name__ == "__main__":
    with open("tree_2_rules.txt", "r", encoding="utf-8") as f:
        tree_text = f.read()

    tree = parse_tree(tree_text)

    with open("../frontend/tree.json", "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2, ensure_ascii=False)

    print("✅ JSON exported to frontend/tree.json")
