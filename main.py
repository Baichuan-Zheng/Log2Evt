import sys
from config.settings import Settings
from src.collection.stap_runner import StapRunner
from src.utils.log_parser import LogParser
from src.analysis.tree_builder import ExecutionTreeBuilder
from src.analysis.event_integration import EventAnalyzer
from src.reporting.report_generator import ReportGenerator


def main():
    try:
        # Phase 1: Data Collection
        print("Starting log collection...")
        collector = StapRunner("vfs")
        collector.run()

        # Phase 2: Data Parsing
        print("\nParsing log data...")
        traces = LogParser.parse_trace_file(Settings.LOG_TYPES["vfs"]["output_file"])

        # Phase 3: Building Execution Tree
        print("Building execution path tree...")
        tree_builder = ExecutionTreeBuilder()
        tree_builder.build(traces)

        # Phase 4: Event Analysis
        print("Performing event integration analysis...")
        analyzer = EventAnalyzer(tree_builder)
        events = analyzer.analyze_events()

        # Phase 5: Generating Report
        print("Generating final report...")
        ReportGenerator.generate(events)

        print(f"\nAnalysis complete! Results saved in {Settings.LOG_TYPES['vfs']['output_file']}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()