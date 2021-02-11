#!/usr/bin/env python3

# Copyright (c) 2021 Takao Akaki
# modify from assistant_grpc_demo.py

# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google Assistant GRPC recognizer. """

import argparse
import locale
import logging
import signal
import subprocess
import sys

from aiy.assistant.grpc import AssistantServiceClientWithLed
from aiy.board import Board
from aiy.leds import *
from gpiozero import GPIODevice
from aiy.pins import PIN_A, PIN_B, PIN_C, PIN_D
from aiy.voice import tts

def volume(string):
    value = int(string)
    if value < 0 or value > 100:
        raise argparse.ArgumentTypeError('Volume must be in [0...100] range.')
    return value

def locale_language():
    language, _ = locale.getdefaultlocale()
    return language

def data_recieve(aiy_gpios):
    recv_buf = 0
    value = 0
    while True:
        if aiy_gpios[0].value == 1:
            value += 1
        if aiy_gpios[1].value == 1:
            value += 2
        if aiy_gpios[2].value == 1:
            value += 4
        if aiy_gpios[3].value == 1:
            value += 8
        if value != 0:
            # 誤作動を防ぐため２回チェック
            if recv_buf == value:
                return str(recv_buf)
            recv_buf = value
            value = 0
            


def main():
    leds = Leds()
    logging.basicConfig(level=logging.DEBUG)
    signal.signal(signal.SIGTERM, lambda signum, frame: sys.exit(0))

    parser = argparse.ArgumentParser(description='Assistant service example.')
    parser.add_argument('--language', default=locale_language())
    parser.add_argument('--volume', type=volume, default=100)
    args = parser.parse_args()

    aiy_gpios = [GPIODevice(PIN_A), GPIODevice(PIN_B), GPIODevice(PIN_C), \
                GPIODevice(PIN_D)]

    with Board() as board:
        assistant = AssistantServiceClientWithLed(board=board,
                                                  volume_percentage=args.volume,
                                                  language_code=args.language)
        while True:
            logging.info('Press button to start conversation...')
            recv_str = "0"
            while recv_str == "0":
                recv_str = data_recieve(aiy_gpios)
                logging.info('Recieved Data :' + recv_str + ':')
                break
            if recv_str == "1":
                logging.info('Conversation started!')
                assistant.conversation()

            elif recv_str == "2":
                leds.update(Leds.rgb_on(Color.RED))
            
            elif recv_str == "3":
                leds.update(Leds.rgb_on(Color.BLUE))

# 拡張用のサンプル
#            elif recv_str == "4":
#                leds.update(Leds.rgb_on(Color.GREEN))
#                subprocess.call('sudo shutdown -h now', shell=True)
#
#            elif recv_str == "5":
#                leds.update(Leds.rgb_on(Color.YELLOW))
#                subprocess.call('sudo reboot', shell=True)

if __name__ == '__main__':
    main()
