import cv2
import os
from tqdm import tqdm  # 引入 tqdm 套件

def video_to_images(video_path, image_format, frame_interval):
    """
    讀取影片並將每隔指定幀保存為圖片，輸出目錄為影片標題。

    :param video_path: 影片檔案路徑。
    :param image_format: 圖片格式 (如 jpg, png)。
    :param frame_interval: 提取圖片的影格間隔。
    """
    # 獲取影片標題作為輸出資料夾名稱
    video_title = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = video_title

    # 確保輸出資料夾存在
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"已建立輸出資料夾: {output_dir}")
    else:
        print(f"輸出資料夾已存在: {output_dir}")

    print(f"影片路徑: {video_path}")
    print(f"輸出資料夾: {output_dir}")
    print(f"圖片格式: {image_format}")
    print(f"影格間隔: 每 {frame_interval} 幀保存一張圖片")

    # 開啟影片檔案
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"無法開啟影片: {video_path}")
        return

    # 獲取影片的總幀數
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    frame_count = 0
    saved_count = 0

    # 使用 tqdm 進度條
    with tqdm(total=total_frames // frame_interval, desc="處理進度", unit="張圖片") as pbar:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 每隔指定影格保存一張圖片
            if frame_count % frame_interval == 0:
                frame_path = os.path.join(output_dir, f"frame_{frame_count:06d}.{image_format}")
                cv2.imwrite(frame_path, frame)
                saved_count += 1
                pbar.update(1)  # 更新進度條

            frame_count += 1

    cap.release()
    print(f"完成！總共保存 {saved_count} 張圖片到 {output_dir}。")

if __name__ == "__main__":
    # 輸入影片路徑
    video_path = input("請輸入影片路徑: ").strip()

    # 輸入圖片格式
    image_format = input("請輸入輸出圖片格式 (例如 jpg, png): ").strip().lower()
    if image_format not in ["jpg", "png"]:
        print("不支援的格式，默認使用 jpg")
        image_format = "jpg"

    # 輸入影格間隔
    try:
        frame_interval = int(input("請輸入影格間隔 (例如 3 表示每 3 幀提取一張圖片): ").strip())
        if frame_interval < 1:
            raise ValueError
    except ValueError:
        print("輸入無效，默認使用間隔 1")
        frame_interval = 1

    # 開始處理影片
    video_to_images(video_path, image_format, frame_interval)
