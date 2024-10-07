import cadquery as cq
import math
from cadquery import exporters 

circle1 = 30.0
circle2 = 20.0
circle3 = 18.0
circle4 = 8.0
d = 60.0
angle = math.asin((circle1 - circle2)/d)

X1 = circle1 * math.sin(angle)
Y1 = circle1 * math.cos(angle)

X2 = circle2 * math.sin(angle)
Y2 = circle2 * math.cos(angle)



# 各形状を個別に作成し、ワイヤーを閉じる
Sessen = (
    cq.Workplane("XY")
    .moveTo(0.0, 30.0)
    .radiusArc((X1, Y1), circle1)
    .lineTo(X2 + d, Y2)
    .radiusArc((X2 + d, -Y2), circle2)
    .lineTo(X1, -Y1)
    .radiusArc((0.0, -30.0), circle1)
    .close()
)

result = Sessen.extrude(12)

# ミラーリングして結合
mirrored_result = result.mirror("ZY")

# ミラーした結果を元の形状と結合
combined_result = result.union(mirrored_result)

# 60と-60の位置に穴を開ける
combined_result = combined_result.faces(">Z").workplane().rarray(120, 1, 2, 1).hole(circle4 * 2)

# 中心に直径30の円筒を追加
cylinder = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(circle1)  # 半径15の円を描く
    .extrude(36)  # 円筒の高さを12に設定
)

# 円筒を元の形状に結合
combined_result = combined_result.union(cylinder)

# 円筒に直径18の穴を追加
combined_result = combined_result.faces(">Z").workplane().hole(circle3 * 2)

# STLファイルとして出力
exporters.export(combined_result, 'output.stl')

# 結果を表示
show_object(combined_result)