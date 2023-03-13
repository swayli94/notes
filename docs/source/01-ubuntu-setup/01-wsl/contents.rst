WSL
====================


简介
-----------------------

Windows Subsystem for Linux, 建议使用 WSL2。


基础操作
-----------------------

Windows CMD 命令

.. code-block:: bash

    # 查看安装的系统
    wsl -l -v

    # 卸载对应的系统
    wsl --unregister Ubuntu-22.04

    # 更新 WSL（可能需要连接 VPN）
    wsl --update

    # 关闭 WSL
    wsl --shutdown

    # 进入 root 用户（管理员权限运行）
    wsl --user root


Linux 命令

.. code-block:: bash

    # 临时更改 hostname 为 WSL
    sudo hostname WSL
    vim /etc/hostname
    vim /etc/hosts

    # 永久更改 hostname 为 WSL
    # https://learn.microsoft.com/en-us/windows/wsl/wsl-config
    vim /etc/wsl.conf

    # 写入
    # [network]
    # hostname = WSL
    # generateHosts = true
    # 重启 WSL

    # 在 Windows 中打开 WSL
    explorer.exe .

    # 打开 Windows C:\
    cd /mnt/c

    # 更新发行版中的包
    sudo apt update


在 WSL2 上运行 Linux GUI 应用
---------------------------------

安装过程参见
`对 Linux GUI 应用的安装支持 <https://learn.microsoft.com/zh-cn/windows/wsl/tutorials/gui-apps>`_ 。

一些常用的 GUI 应用：

.. code-block:: bash

    # Gedit 是 GNOME 桌面环境的默认文本编辑器
    gedit ~/.bashrc

    # Nautilus 也称为 GNOME Files，是 GNOME 桌面的文件管理器
    nautilus

    # VLC 是一种免费的多媒体播放器，可播放大多数多媒体文件
    vlc

    # X11 是 Linux 窗口管理系统
    # https://www.x.org/wiki/UserDocumentation/GettingStarted/
    xcalc
