
import cv2
import numpy as np


# ==============================
# 1. 滑块需要的空函数
# ==============================
def nothing(x):
    pass


# ==============================
# 2. 用来保存当前这一帧的 HSV 图像
# 鼠标点击时会读取这里面的颜色数据
# ==============================
current_hsv = None


# ==============================
# 3. 鼠标点击函数
# 当你点击摄像头画面时，
# 程序会读取那个位置的 HSV 数值
# ==============================
def mouse_callback(event, x, y, flags, param):
    global current_hsv

    # 判断是不是鼠标左键点击
    if event == cv2.EVENT_LBUTTONDOWN:

        # 如果还没有 HSV 图像，就什么都不做
        if current_hsv is None:
            return

        # 读取你点击位置的 HSV 数值
        hsv_value = current_hsv[y, x]

        h = int(hsv_value[0])
        s = int(hsv_value[1])
        v = int(hsv_value[2])

        # 在 PyCharm 下方控制台打印出来
        print("========================")
        print("你点击的位置：", x, y)
        print("H =", h)
        print("S =", s)
        print("V =", v)
        print("========================")


# ==============================
# 4. 打开摄像头
# 0 一般代表电脑默认摄像头
# ==============================
cap = cv2.VideoCapture(0)


# ==============================
# 5. 创建窗口
# ==============================

# HSV 滑块窗口
cv2.namedWindow("HSV Control", cv2.WINDOW_NORMAL)


# 摄像头画面窗口
cv2.namedWindow("OpenCV Color Tracking")

# 给摄像头窗口绑定鼠标点击函数
cv2.setMouseCallback(
    "OpenCV Color Tracking",
    mouse_callback
)


# ==============================
# 6. 创建 6 个 HSV 滑块
# ==============================

# H 范围：0 ~ 179
cv2.createTrackbar(
    "H Min",
    "HSV Control",
    35,
    179,
    nothing
)

cv2.createTrackbar(
    "H Max",
    "HSV Control",
    85,
    179,
    nothing
)

# S 范围：0 ~ 255
cv2.createTrackbar(
    "S Min",
    "HSV Control",
    20,
    255,
    nothing
)

cv2.createTrackbar(
    "S Max",
    "HSV Control",
    255,
    255,
    nothing
)

# V 范围：0 ~ 255
cv2.createTrackbar(
    "V Min",
    "HSV Control",
    40,
    255,
    nothing
)

cv2.createTrackbar(
    "V Max",
    "HSV Control",
    255,
    255,
    nothing
)


# ==============================
# 7. 主循环
# ==============================
while True:

    # 从摄像头读取一帧画面
    ret, frame = cap.read()

    # 如果摄像头读取失败，就退出
    if not ret:
        print("摄像头读取失败")
        break


    # ==============================
    # 8. BGR 转 HSV
    # ==============================
    hsv = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2HSV
    )

    # 保存当前 HSV 图像
    # 鼠标点击时会读取它
    current_hsv = hsv.copy()


    # ==============================
    # 9. 读取滑块现在的位置
    # ==============================

    h_min = cv2.getTrackbarPos(
        "H Min",
        "HSV Control"
    )

    h_max = cv2.getTrackbarPos(
        "H Max",
        "HSV Control"
    )

    s_min = cv2.getTrackbarPos(
        "S Min",
        "HSV Control"
    )

    s_max = cv2.getTrackbarPos(
        "S Max",
        "HSV Control"
    )

    v_min = cv2.getTrackbarPos(
        "V Min",
        "HSV Control"
    )

    v_max = cv2.getTrackbarPos(
        "V Max",
        "HSV Control"
    )


    # ==============================
    # 10. 创建 HSV 最小值和最大值
    # ==============================
    lower = np.array(
        [h_min, s_min, v_min]
    )

    upper = np.array(
        [h_max, s_max, v_max]
    )


    # ==============================
    # 11. 根据 HSV 范围生成 Mask
    #
    # 符合范围：
    # 变成白色
    #
    # 不符合：
    # 变成黑色
    # ==============================
    mask = cv2.inRange(
        hsv,
        lower,
        upper
    )


    # ==============================
    # 12. 简单去噪
    # ==============================
    kernel = np.ones(
        (5, 5),
        np.uint8
    )

    # 去除小白点
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_OPEN,
        kernel
    )

    # 填补一些小黑洞
    mask = cv2.morphologyEx(
        mask,
        cv2.MORPH_CLOSE,
        kernel
    )


    # ==============================
    # 13. 找白色区域的轮廓
    # ==============================
    contours, _ = cv2.findContours(
        mask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )


    # ==============================
    # 14. 检查每一个轮廓
    # ==============================
    for contour in contours:

        # 计算面积
        area = cv2.contourArea(
            contour
        )

        # 小于 500 的区域忽略
        if area > 500:

            # 得到外接矩形
            x, y, w, h = cv2.boundingRect(
                contour
            )

            # 画绿色矩形框
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # 计算中心点
            center_x = x + w // 2
            center_y = y + h // 2

            # 画蓝色中心点
            cv2.circle(
                frame,
                (center_x, center_y),
                5,
                (255, 0, 0),
                -1
            )

            # 显示面积
            cv2.putText(
                frame,
                f"Area: {int(area)}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

            # 显示中心点坐标
            cv2.putText(
                frame,
                f"Center: ({center_x},{center_y})",
                (x, y - 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )


    # ==============================
    # 15. 在画面左上角显示当前 HSV 范围
    # ==============================
    cv2.putText(
        frame,
        f"H: {h_min}-{h_max}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"S: {s_min}-{s_max}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    cv2.putText(
        frame,
        f"V: {v_min}-{v_max}",
        (10, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )


    # ==============================
    # 16. 显示摄像头画面
    # ==============================
    cv2.imshow(
        "OpenCV Color Tracking",
        frame
    )


    # ==============================
    # 17. 显示黑白 Mask
    # ==============================
    cv2.imshow(
        "Mask",
        mask
    )


    # ==============================
    # 18. 按 q 退出程序
    # ==============================
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


# ==============================
# 19. 释放摄像头
# ==============================
cap.release()


# ==============================
# 20. 关闭所有窗口
# ==============================
cv2.destroyAllWindows()