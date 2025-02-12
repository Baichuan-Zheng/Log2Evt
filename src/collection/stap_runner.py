import tempfile
import subprocess
from config.settings import Settings
from src.collection.probe_manager import ProbeGenerator


class StapRunner:
    def __init__(self, config_type: str):
        self.config = Settings.LOG_TYPES[config_type]
        self.script_generators = {
            "vfs": ProbeGenerator.generate_vfs_probe,
            "pam": ProbeGenerator.generate_framework_probe
        }

    def run(self) -> None:
        """Execute SystemTap monitoring"""
        script = self._build_script()
        with tempfile.NamedTemporaryFile(mode='w', suffix='.stp') as f:
            f.write(script)
            f.flush()
            cmd = [
                "sudo", Settings.STAP_PATH,
                "-v",
                "-g",  # Enable guru mode
                "-DMAXSTRINGLEN=4096",
                f.name,
                "-o", self.config['output_file']
            ]
            subprocess.run(cmd, check=True)

    def _build_script(self) -> str:
        """Build the complete SystemTap script"""
        if "target_inode" in self.config:
            return ProbeGenerator.generate_vfs_probe(self.config)
        return ProbeGenerator.generate_framework_probe(self.config)