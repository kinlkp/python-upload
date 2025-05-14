#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
The script is used to suppress the sitescope monitoring
"""
 
import pyautogui
import time

while True:
	o = pyautogui.click(2200, 1000)
	print("********** Clicked mouse ===============")
	time.sleep(10)
	o = pyautogui.click(250, 200)
	time.sleep(10)

