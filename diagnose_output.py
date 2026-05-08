"""diagnose_output.py - 独立诊断脚本
直接在 Python 中加载 ONNX 模型，运行推理，打印输出。
不依赖任何 C++ 代码，避免指针混乱干扰。
"""

import onnxruntime as ort
import numpy as np
import cv2

# 1. 加载模型
print("[1] Loading model ...")
session = ort.InferenceSession("yolov8n_int8.onnx", providers=["CPUExecutionProvider"])

# 获取输入输出信息
for i, inp in enumerate(session.get_inputs()):
    print(f"  Input[{i}]: name={inp.name}, shape={inp.shape}, type={inp.type}")
for i, out in enumerate(session.get_outputs()):
    print(f"  Output[{i}]: name={out.name}, shape={out.shape}, type={out.type}")

# 2. 读取图片并预处理
print("\n[2] Reading test.jpg ...")
img = cv2.imread("test.jpg")
if img is None:
    print("ERROR: Cannot read test.jpg")
    exit(1)
orig_h, orig_w = img.shape[:2]
print(f"  Original: {orig_w} x {orig_h}")

target_w, target_h = 640, 640
resized = cv2.resize(img, (target_w, target_h))
rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)

# 归一化 + HWC->CHW
rgb_norm = rgb.astype(np.float32) / 255.0
chw = np.transpose(rgb_norm, (2, 0, 1))  # (3, 640, 640)
input_tensor = np.expand_dims(chw, axis=0).astype(np.float32)  # (1, 3, 640, 640)
print(f"  Input tensor shape: {input_tensor.shape}")

# 3. 运行推理
print("\n[3] Running inference ...")
outputs = session.run(["output0"], {"images": input_tensor})
output = outputs[0]
print(f"  Output shape: {output.shape}")
print(f"  Output dtype: {output.dtype}")

# 4. 分析输出
print(f"\n[4] Analyzing output ...")
print(f"  Total elements: {output.size}")
print(f"  Output ranges: min={output.min():.6f}, max={output.max():.6f}, mean={output.mean():.6f}")

# 输出是 [1, 84, 8400]
data = output[0]  # (84, 8400)

# print first anchor
print(f"\n  Anchor[0] via data[:, 0]:")
print(f"    bbox (cx,cy,w,h): {data[0,0]:.4f}, {data[1,0]:.4f}, {data[2,0]:.4f}, {data[3,0]:.4f}")
print(f"    class scores [4:14]: {data[4:14, 0]}")

# print a few random anchors
print(f"\n  Checking best scores across all 8400 anchors ...")
best_scores = np.max(data[4:, :], axis=0)  # max class score for each anchor
print(f"  Best score stats: min={best_scores.min():.6f}, max={best_scores.max():.6f}, mean={best_scores.mean():.6f}")
print(f"  Number of anchors with best_score > 0.25: {np.sum(best_scores > 0.25)}")

# find the top anchors
top_indices = np.argsort(best_scores)[-10:][::-1]
print(f"\n  Top 10 anchors by class score:")
for idx in top_indices:
    cx, cy, w, h = data[0, idx], data[1, idx], data[2, idx], data[3, idx]
    score = best_scores[idx]
    class_id = np.argmax(data[4:, idx])
    print(f"    Anchor[{idx}]: score={score:.6f}, class={class_id}, "
          f"bbox=({cx:.2f}, {cy:.2f}, {w:.2f}, {h:.2f})")

# yolo export model=yolov8n.pt format=onnx opset=12; cd yolo_cpp/build; cmake --build . --config Release; cd ../..; .\yolo_cpp\build\Release\YoloDeployTest.exe