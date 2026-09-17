# opencv-color-tracking
OpenCV real-time color tracking practice project

一个基于 OpenCV 的实时颜色目标检测与定位学习项目。

1. 项目简介
程序读取摄像头实时画面，将 BGR 图像转换到 HSV 颜色空间，
通过 HSV 阈值完成目标颜色分割，并结合形态学处理和轮廓检测，
实现目标区域框选以及中心坐标计算。

2. 功能
- 摄像头实时图像读取
- BGR → HSV 颜色空间转换
- HSV 阈值实时调节
- 鼠标点击读取像素 HSV 值
- HSV 颜色区域分割
- 开运算 / 闭运算去噪
- 轮廓检测与面积筛选
- 目标外接框绘制
- 目标中心坐标计算
- 实时显示目标面积和中心位置

3. 技术流程
Camera Input
↓
BGR → HSV
↓
HSV Threshold
↓
Mask
↓
Morphological Processing
↓
Contour Detection
↓
Area Filtering
↓
Bounding Box & Center Position

4. 开发与学习过程
本项目为个人 OpenCV 学习实践。
初版程序在 AI 辅助下完成，在此基础上进行了：
- 本地 Python / OpenCV 环境配置
- 程序运行与摄像头测试
- HSV 参数调节与实际目标测试
- 图像处理流程理解
- 代码调试与运行结果验证
- 项目代码与实验结果整理
通过该项目学习了 HSV 颜色空间、二值化、
形态学处理、轮廓检测以及基础目标定位方法。

5. 运行
安装依赖：
pip install -r requirements.txt
运行：
python main.py
按 `q` 退出程序。

6. 说明
该项目主要用于 OpenCV 与计算机视觉基础学习，
并非复杂目标检测算法。
