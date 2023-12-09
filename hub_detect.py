import torch
# 模型
model = torch.hub.load("./", "custom", path="runs/train/exp3/weights/best.pt", source="local")
# 图片
img = "datasets/images/train/43_215.jpg"
# 推理
results = model(img)
# 显示结果
results.show()

results.render()[0]
# 统计检测到的人数
num_people = len(results.xyxy)
print(f"检测到的人数：{num_people}")
