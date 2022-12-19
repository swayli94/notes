WSL
====================


简介
-----------------------

Windows Subsystem for Linux, 建议使用 WSL2。


基础操作
-----------------------

Windows CMD 命令

.. code-block:: bash
   :linenos:

   # 查看安装的系统
   wsl -l -v

   # 卸载对应的系统
   wsl --unregister Ubuntu-22.04

   # 关闭 WSL
   wsl --shutdown

Linux 命令

.. code-block:: bash
   :linenos:

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


