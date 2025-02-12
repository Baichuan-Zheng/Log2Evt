import json
from datetime import datetime
from typing import List

from src.analysis.tree_builder import TreeNode


class ReportGenerator:
    @staticmethod
    def generate(events: List[List[TreeNode]], output_format: str = "text") -> None:
        if output_format == "json":
            ReportGenerator._generate_json(events)
        else:
            ReportGenerator._generate_text(events)

    @staticmethod
    def _generate_text(events: List[List[TreeNode]]) -> None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"data/output/analysis_report_{timestamp}.txt"

        with open(filename, 'w') as f:
            f.write(f"Event Analysis Report ({timestamp})\n\n")
            f.write(f"Found {len(events)} independent events\n")
            f.write("=" * 50 + "\n")

            for idx, event in enumerate(events, 1):
                f.write(f"Event #{idx} (contains {len(event)} logs)\n")
                f.write("Associated Path:\n")
                path = " -> ".join([n.name for n in event[0].get_path()])
                f.write(f"{path}\n")
                f.write("Log Samples:\n")
                for node in event[:3]:
                    f.write(f"- {node.logs[0][:60]}...\n")
                f.write("\n")

    @staticmethod
    def _generate_json(events: List[List[TreeNode]]) -> None:
        report = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_events": len(events)
            },
            "events": []
        }

        for idx, event in enumerate(events, 1):
            event_data = {
                "id": idx,
                "log_count": len(event),
                "representative_log": event[0].logs[0] if event else "",
                "execution_path": [n.name for n in event[0].get_path()],
                "related_nodes": [
                    {
                        "node_name": node.name,
                        "log_count": len(node.logs),
                        "depth": node.depth
                    } for node in event
                ]
            }
            report["events"].append(event_data)

        filename = f"data/output/analysis_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)