from typing import List, Tuple


class TreeNode:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent
        self.children = {}
        self.depth = parent.depth + 1 if parent else 0
        self.logs = []
        self.highlight = False

    def add_child(self, name: str) -> 'TreeNode':
        if name not in self.children:
            self.children[name] = TreeNode(name, self)
        return self.children[name]

    def add_log(self, message: str) -> None:
        self.logs.append(message)
        self.highlight = True


class ExecutionTreeBuilder:
    def __init__(self):
        self.root = TreeNode("root")
        self.current_path = []
        self.node_index = {}

    def build(self, traces: List[Tuple[str, List[str]]]) -> None:
        prev_stack = []
        for msg, stack in traces:
            current_node = self.root
            divergence_index = 0

            # Find the common prefix with the previous path
            while divergence_index < len(prev_stack) and divergence_index < len(stack):
                if stack[divergence_index] != prev_stack[divergence_index]:
                    break
                current_node = current_node.children.get(stack[divergence_index], current_node)
                divergence_index += 1

            # Build new branches
            for func in stack[divergence_index:]:
                current_node = current_node.add_child(func)

            # Mark log nodes
            if stack:
                leaf_node = current_node
                leaf_node.add_log(msg)

            prev_stack = stack

    def find_highlight_nodes(self) -> List[TreeNode]:
        return self._dfs_find_highlight(self.root)

    def _dfs_find_highlight(self, node: TreeNode) -> List[TreeNode]:
        nodes = []
        if node.highlight:
            nodes.append(node)
        for child in node.children.values():
            nodes.extend(self._dfs_find_highlight(child))
        return nodes