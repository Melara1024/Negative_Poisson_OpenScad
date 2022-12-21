from solid import *
from solid.utils import *
import numpy as np
import cmath
import math


# 点と点をつなぐリンクを作成する
def connect_hex(p1=[0.0, 0.0], p2=[10.0, 10.0]):
    # リンクの長さ
    L = norm(p1, p2)
    # リンクの幅
    T = 1.5 if L > 8 else L/4

    # ここにリンクを構成する点を入れていく
    hexpt = [[0.0, 0.0],
             [(2 * T), 0.0 + (T / 2)],
             [L - (2 * T), 0.0 + (T / 2)],
             [L, 0.0],
             [L - (2 * T), 0.0 - (T / 2)],
             [(2 * T), 0.0 - (T / 2)]]

    # リンクの傾き
    theta = math.atan2((p2[1] - p1[1]), (p2[0] - p1[0]))

    # リンクの回転量を計算
    for pt in hexpt:
        x = pt[0]
        y = pt[1]
        # xの回転
        pt[0] = x * math.cos(theta) - y * math.sin(theta)
        # yの回転
        pt[1] = x * math.sin(theta) + y * math.cos(theta)
    hex = polygon(hexpt)

    hex += joint(p1)
    hex += joint(p2)

    return color("red")(linear_extrude(2)(hex))

def joint(center=(0, 0)):
    octpt = [[0, 1],[1.414/2, 1.414/2],[1, 0],[1.414/2, -1.414/2],[0, -1],[-1.414/2, -1.414/2],[-1, 0],[-1.414/2, 1.414/2]]
    return (translate(center))(polygon(octpt))


# ノルムを計算，多分mathとかにあるだろうけど
def norm(p1=[0.0, 0.0], p2=[1.0, 1.0]):
    return math.sqrt((p1[0] - p2[0]) ** 2.0 + (p1[1] - p2[1]) ** 2.0)



def main():
    # 全体構造の大きさを決定するパラメータ
    line = 3  # 行数
    columun = 4  # 列数

    # 単位構造の大きさを決定するパラメータ
    a = 10
    b = 14


    # map = [[0.5, 0.5, 0.5, 0.5],
    #        [0.5, 0.5, 0.5, 0.5],
    #        [0.5, 0.5, 0.5, 0.5]]

    # map = [[0.3, 0.3, 0.3, 0.3],
    #        [0.3, 0.3, 0.3, 0.3],
    #        [0.3, 0.3, 0.3, 0.3]]


    # map = [[1, 1, 1, 1],
    #        [1, 1, 1, 1],
    #        [1, 1, 1, 1]]

    map = [[0, 0, 0, 0],
           [0, 0, 0, 0],
           [0, 0, 0, 0]]

    # map = [[0.5, 0.6, 0.8, 1, 1, 1, 0.5, 0, 0, 0 ,0.5 ,1, 1, 1, 0.8 ,0.6, 0.5],
    #        [0.5, 0.6, 0.8, 1, 1, 1, 0.5, 0, 0, 0 ,0.5 ,1, 1, 1, 0.8 ,0.6, 0.5],
    #        [0.5, 0.6, 0.8, 1, 1, 1, 0.5, 0, 0, 0 ,0.5 ,1, 1, 1, 0.8 ,0.6, 0.5],
    #        [0.5, 0.6, 0.8, 1, 1, 1, 0.5, 0, 0, 0 ,0.5 ,1, 1, 1, 0.8 ,0.6, 0.5]]

    # 全体構造の大きさを決定するパラメータ
    line = len(map)  # 行数
    columun = len(map[0])  # 列数

    expect_poisson = []

    theta = 0
    # 各区間におけるポアソン比を算出する
    for l in range(len(map)):
        new_line = []
        for c in range(len(map[l])):
            # thetaになるまで引っ張ったときの横のび量
            dL = (math.sqrt(a**2 + b**2)/2)*math.cos(theta) - a/2
            L = a/2
            # thetaになるまで引っ張ったときの縦の縮み量
            dD = (1-2*map[l][c])*(math.sqrt(a**2 + b**2)/4)
            D = b/2

            print(f"dL = {dL}, L = {L}, dD = {dD}, D = {D}")

            new_line.append((dD/D)/(dL/L))

        expect_poisson.append(new_line)
    print(expect_poisson)


    object = cube(size=0, center=False)

    # Todo 最初にジグザグ構造を作る
    for l in range(line):
        for c in range(columun):
            x0 = a * c
            y0 = b * l

            hex1 = connect_hex([0, 0], [a / 2, b / 4])
            hex2 = connect_hex([0, 0], [a / 2, - b / 4])

            # 構造右上
            x_offset = 0
            y_offset = b / 4
            object += (translate([x0 + x_offset, y0 + y_offset]))(hex1)
            # 構造左上
            x_offset = -a / 2
            y_offset = b / 2
            object += (translate([x0 + x_offset, y0 + y_offset]))(hex2)
            # 構造右下
            x_offset = 0
            y_offset = 0
            object += (translate([x0 + x_offset, y0 + y_offset]))(hex2)
            # 構造左下
            x_offset = - a / 2
            y_offset = - b / 4
            object += (translate([x0 + x_offset, y0 + y_offset]))(hex1)

    # Todo mapを参照して腕構造を張る
    for l in range(line):
        for c in range(columun):
            x0 = a * c
            y0 = b * l

            hex = connect_hex([0, 0], [0, b*(2*map[l][c]+1)/4])

            # 構造右
            x_offset = + a*map[l][c]/2
            y_offset = - b / 4 + b/2 - b*(map[l][c]+1)/4
            object += (translate([x0 + x_offset, y0 + y_offset]))(hex)
            # 構造左
            x_offset =  - a*map[l][c]/2
            y_offset = - b / 4 + b/2 - b*(map[l][c]+1)/4
            object += (translate([x0 + x_offset, y0 + y_offset]))(hex)
            # 構造右
            x_offset = a*(1-map[l][c])/2
            y_offset = 3*b/4 - b*(map[l][c]+1)/4
            object += (translate([x0 + x_offset, y0 + y_offset]))(hex)
            # 構造左
            x_offset =  - a*(1-map[l][c])/2
            y_offset = 3*b/4 - b*(map[l][c]+1)/4
            object += (translate([x0 + x_offset, y0 + y_offset]))(hex)


    scad_render_to_file(object, "output.scad", include_orig_code=False)


main()
