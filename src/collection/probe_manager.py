class ProbeGenerator:
    @staticmethod
    def generate_vfs_probe(config: dict) -> str:
        return f"""global target_inode = {config['target_inode']}
probe kernel.function("vfs_write").call {{
    if ($file->f_inode->i_ino == target_inode) {{
        msg = user_string_quoted($buf, $count)
        printf("%%s|||%%s\\n", msg, sprint_ubacktrace())
    }}
}}
probe begin {{ println("VFS监控启动 (inode=%d)" % target_inode) }}
probe end {{ println("VFS监控停止") }}"""

    @staticmethod
    def generate_framework_probe(config: dict) -> str:
        return f"""probe process("{config['library_path']}").function("{config['function_name']}") {{
    msg = user_string($arg2)
    printf("%%s|||%%s\\n", msg, sprint_ubacktrace())
}}
probe begin {{ Framework log monitoring started ({config['function_name']})") }}
probe end {{ println("Framework monitoring stopped") }}"""