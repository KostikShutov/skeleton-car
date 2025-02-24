import cv2
import time
import numpy as np
from typing import Optional
from car.CameraCapturer import CameraCapturer


class AutoAlgorithm:
    def __init__(self, entry: dict) -> None:
        self.entry: dict = entry

    def execute(self) -> list[dict]:
        ret, originalFrame = CameraCapturer().cap.read()

        if not ret:
            CameraCapturer().release()
            cv2.destroyAllWindows()
            time.sleep(1)
            CameraCapturer().init()

            raise RuntimeError('Camera problem')

        angle, processedFrame = self.doExecute(originalFrame)

        if self.entry['needShowFrames']:
            cv2.imshow('Original frame', originalFrame)
            cv2.imshow('Processed frame', processedFrame)
            cv2.waitKey(1)

        lastTime: Optional[float] = self.entry['lastTime']

        if lastTime is not None and time.time() - lastTime < 1:
            return []

        if abs(angle) < 5:
            return [{
                'commandName': 'FORWARD',
                'speed': 60,
                'duration': 0.1,
            }]
        else:
            return [
                {
                    'commandName': 'TURN',
                    'steering': round(float(angle), 2),
                },
                {
                    'commandName': 'FORWARD',
                    'speed': 60,
                    'duration': 0.1,
                },
            ]

    def doExecute(self, frame):
        height, width, _ = frame.shape

        # Преобразование в HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Определение границ красного цвета
        lower_red1 = np.array([0, 120, 70])
        upper_red1 = np.array([10, 255, 255])
        lower_red2 = np.array([170, 120, 70])
        upper_red2 = np.array([180, 255, 255])

        # Создание маски для красного цвета
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        red_mask = cv2.bitwise_or(mask1, mask2)

        # Оставляем только нижнюю часть изображения
        roi = red_mask[int(height * 0.6):, :]

        # Находим контуры
        contours, _ = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        outputFrame = frame.copy()

        if contours:
            # Выбираем самый большой контур (предположительно линия)
            largestContour = max(contours, key=cv2.contourArea)

            # Рисуем контур на изображении
            cv2.drawContours(outputFrame[int(height * 0.6):, :], [largestContour], -1, (0, 255, 0), 2)

            # Вычисляем центр линии
            M = cv2.moments(largestContour)

            if M['m00'] != 0:
                cx = int(M['m10'] / M['m00'])
            else:
                cx = width // 2  # Если центр не найден, держимся середины

            # Отклонение от центра
            deviation = cx - width // 2

            # Определение угла поворота (грубое приближение)
            angle = np.clip(deviation / (width // 2) * 45, -45, 45)

            return angle, outputFrame

        return 0, outputFrame  # Если линия не найдена, едем прямо
