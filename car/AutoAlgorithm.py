import cv2
import time
import numpy as np


class AutoAlgorithm:
    def __init__(self, entry: dict) -> None:
        self.entry: dict = entry

    def execute(self) -> list[dict]:
        cap = self.entry['cap']
        ret, frame = cap.read()

        if not ret:
            return []

        angle, processedFrame = self.doExecute(frame)

        cv2.imshow('Original frame', frame)
        cv2.imshow('Processed frame', processedFrame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            return []

        lastTime: float | None = self.entry['lastTime']

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

        # Преобразование в оттенки серого
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Размытие для уменьшения шума
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Бинаризация изображения (настройте порог)
        _, binary = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)

        # Определяем центральную область для анализа
        roi = binary[int(height * 0.6):, :]

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
