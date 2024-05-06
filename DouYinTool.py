#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import sys
import time
WORK_SPACE = os.path.dirname(sys.path[0])
sys.path.append(os.path.join(WORK_SPACE))
from f2.cli.cli_console import RichConsoleManager as RCManager


if __name__ == "__main__":
    RCManager = RCManager()

    if len(sys.argv) <= 1:
        RCManager.rich_console.print(
            "[bold red]请通过命令行启动并提供必要的参数, 输入[bold green] TikTokTool -h [/bold green]查看不同平台帮助。[/bold red]"
        )
        from f2.utils import __version__

        RCManager.rich_console.print(
            f"[bold white]F2 Version:{__version__._version}[/bold white]"
        )
        time.sleep(3)
        sys.exit(1)

    from f2.apps.douyin.cli import douyin
    douyin()
