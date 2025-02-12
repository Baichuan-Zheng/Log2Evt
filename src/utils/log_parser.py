from typing import List, Tuple
import re

from config.settings import Settings


class LogParser:
    @staticmethod
    def parse_trace_file(filename: str) -> List[Tuple[str, List[str]]]:
        traces = []
        stack_pattern = re.compile(r'0x[0-9a-f]+ : (.+)\+0x[0-9a-f]+')

        with open(filename, 'r') as f:
            for line in f:
                if '|||' not in line:
                    continue

                msg_part, stack_part = line.strip().split('|||', 1)
                stack_frames = []

                for frame in stack_part.split('\n'):
                    match = stack_pattern.search(frame)
                    if match:
                        func_name = match.group(1).split(' (')[0]
                        stack_frames.append(func_name)

                # Retain the most recent MAX_STACK_DEPTH layers of the call stack
                stack_frames = stack_frames[:Settings.MAX_STACK_DEPTH]
                traces.append((msg_part, stack_frames[::-1]))  # Reverse the call order

        return traces