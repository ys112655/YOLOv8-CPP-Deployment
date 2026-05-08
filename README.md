# 🚀 YOLOv8 C++ Real-Time Inference Engine
![C++](https://img.shields.io/badge/C++-17-blue.svg) ![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg) ![ONNXRuntime](https://img.shields.io/badge/ONNXRuntime-1.25.1-orange.svg) ![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
本项目是一个极其轻量、硬核的 YOLOv8 端侧 C++ 部署引擎。完全脱离 Python 环境，仅依赖 `OpenCV` 和 `ONNXRuntime`，实现了从 PC 摄像头读取实时视频流、构建张量、执行推理到 NMS 后处理的**端到端全链路闭环**。
## 🌟 核心亮点 (Key Features)
- **纯 C++ 底层操控**：拒绝调包，手动实现底层图像内存到深度学习张量的转换。
- **内存排布降维打击**：深刻理解并手动实现了 `HWC` 到 `CHW` 的像素级转换。
- **规避指针陷阱**：创新性地引入 `cv::Mat::t()` 矩阵转置，将复杂的一维指针偏移转化为安全的矩阵行读取。
- **精度保卫战**：完整经历了 INT8 量化导致的置信度断崖式丢失现象，最终采用标准 FP32 引擎，兼顾推理速度与绝对识别精度。
- **工业级后处理**：基于 OpenCV DNN 模块实现了标准的非极大值抑制（NMS）。
## 🚀 极速构建与运行 (Build & Run)
```powershell
cd build
cmake --build . --config Release
cd ..
.\build\Release\YoloDeployTest.exe
