from typing import List, Dict, Tuple
from collections import deque

from config.settings import Settings
from src.analysis.tree_builder import ExecutionTreeBuilder, TreeNode


class EventAnalyzer:
    def __init__(self, tree_builder: ExecutionTreeBuilder):
        self.tree = tree_builder
        self.highlight_nodes = tree_builder.find_highlight_nodes()
        self.parent_map = self._build_parent_map()

    def _build_parent_map(self) -> Dict[TreeNode, TreeNode]:
        parent_map = {}
        queue = deque([self.tree.root])
        while queue:
            node = queue.popleft()
            for child in node.children.values():
                parent_map[child] = node
                queue.append(child)
        return parent_map

    def find_lca(self, node1: TreeNode, node2: TreeNode) -> TreeNode:
        # Find LCA using path lifting method
        path1 = self._get_path_to_root(node1)
        path2 = self._get_path_to_root(node2)

        lca = self.tree.root
        for p1, p2 in zip(reversed(path1), reversed(path2)):
            if p1 == p2:
                lca = p1
            else:
                break
        return lca

    def _get_path_to_root(self, node: TreeNode) -> List[TreeNode]:
        path = []
        while node != self.tree.root:
            path.append(node)
            node = self.parent_map[node]
        path.append(self.tree.root)
        return path

    def analyze_events(self) -> List[List[str]]:
        if len(self.highlight_nodes) < 2:
            return []

        # Calculate the LCA depth of adjacent nodes
        lca_depths = []
        for i in range(len(self.highlight_nodes) - 1):
            lca = self.find_lca(self.highlight_nodes[i], self.highlight_nodes[i + 1])
            lca_depths.append(lca.depth)

        # Event segmentation
        avg_depth = sum(lca_depths) / len(lca_depths)
        threshold = avg_depth * Settings.LCA_RATIO
        events = []
        current_event = []

        for i, depth in enumerate(lca_depths):
            current_event.append(self.highlight_nodes[i])
            if depth < threshold and len(current_event) >= Settings.MIN_EVENT_LENGTH:
                events.append(current_event)
                current_event = []

        if current_event:
            events.append(current_event)

        return events