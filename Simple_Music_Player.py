from datetime import datetime
import pygame
import time
import os
import re


def read_lyric(lrc_path):
    lyric_dict = {}
    zh_cn_lyric_dict = {}
    try:

        with open(lrc_path, "r", encoding="utf-8") as open_lyric:
            lyric_list = open_lyric.readlines()
        for lyric_line in lyric_list:
            get_lyric_time = re.search(r"\[[0-9]*:[0-9.]*]", lyric_line)
            get_lyric = re.sub(r"\[[0-9]*:[0-9.]*]", "", lyric_line).replace("\n", "")
            if get_lyric_time is not None:
                get_lyric_time = datetime.strptime(get_lyric_time.group().replace("[", "").replace("]", ""), "%M:%S.%f")
                get_lyric_time = get_lyric_time.strftime("%M:%S.") + f"{int(get_lyric_time.microsecond / 10000):02d}"
                if get_lyric_time not in lyric_dict:
                    lyric_dict.setdefault(get_lyric_time, get_lyric)
                else:
                    zh_cn_lyric_dict.setdefault(get_lyric_time, get_lyric)
    except FileNotFoundError:
        print("未找到lrc文件")
    return [lyric_dict, zh_cn_lyric_dict]


def play_music(music_path):
    lyric, zh_cn_lyric = read_lyric(
        f"{os.path.dirname(music_path)}/{os.path.splitext(os.path.basename(music_path))[0]}.lrc")
    lyric_cache = ""
    zh_cn_lyric_cache = ""
    pygame.mixer.init()
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        get_play_time = pygame.mixer.music.get_pos() / 1000.0
        play_time = time.strftime("%M:%S", time.gmtime(get_play_time)) + f".{int(get_play_time % 1 * 100):02d}"
        out_lyric = lyric.get(play_time)
        out_zh_cn_lyric = zh_cn_lyric.get(play_time)
        if out_lyric is not None:
            if lyric_cache != out_lyric:
                print("--------------------")
                print(out_lyric)
                lyric_cache = out_lyric
        if out_zh_cn_lyric is not None:
            if zh_cn_lyric_cache != out_zh_cn_lyric:
                print(out_zh_cn_lyric)
                zh_cn_lyric_cache = out_zh_cn_lyric


play_music(input("请输入歌曲文件路径: "))
