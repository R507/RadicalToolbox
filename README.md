# README #

Note: This repo is in very work in progress state

This is a platform and collection of tools for it, for various tasks.

Contents:

    rt - Radical Toolbox - Radical tools collection
    rt.platform - scheduler to run all tools
    rt.platform_ui - main web interface
    rt.monitor - tool to monitor prices, atm support only citilink.ru
    rt.monitor_ui - ui for the monitor
    rt_trash - some garbage for test purposes

How to use it:

run bin/deploy_db.py script, which should deploy sqllite main.db with some entries for test purposes.

bin/run_platform.py runs the platform, which runs the platform, which runs the monitors, which collect the values.
