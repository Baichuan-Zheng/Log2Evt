import os


class Settings:
    # SystemTap configuration
    STAP_PATH = "/usr/bin/stap"
    KERNEL_DEBUGINFO = "/usr/lib/debug/lib/modules/$(uname -r)"

    # Log collection configuration
    LOG_TYPES = {
        "vfs": {
            "target_inode": 123456,  # Replace with actual inode
            "output_file": os.path.abspath("data/output/vfs_traces.log")
        },
        "pam": {
            "library_path": "/lib64/libsecurity/pam_unix.so",
            "function_name": "pam_vsyslog",
            "output_file": os.path.abspath("data/output/pam_traces.log")
        }
    }

    # Event analytics configuration
    LCA_RATIO = 0.8
    MIN_EVENT_LENGTH = 3
    MAX_STACK_DEPTH = 20