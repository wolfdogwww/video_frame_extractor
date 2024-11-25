import cv2
import os

def video_to_images(video_path, image_format):
    """
    讀取影片並將每一幀保存為圖片，輸出目錄為影片標題。

    :param video_path: 影片檔案路徑。
    :param image_format: 圖片格式 (如 jpg, png)。
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

    # 開啟影片檔案
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"無法開啟影片: {video_path}")
        return

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # 保存每一幀為圖片
        frame_path = os.path.join(output_dir, f"frame_{frame_count:06d}.{image_format}")
        cv2.imwrite(frame_path, frame)
        frame_count += 1

    cap.release()
    print(f"完成！總共保存 {frame_count} 張圖片到 {output_dir}。")

if __name__ == "__main__":
    # 輸入影片路徑
    video_path = input("請輸入影片路徑: ").strip()

    # 輸入圖片格式
    image_format = input("請輸入輸出圖片格式 (例如 jpg, png): ").strip().lower()
    if image_format not in ["jpg", "png"]:
        print("不支援的格式，默認使用 jpg")
        image_format = "jpg"

    # 開始處理影片
    video_to_images(video_path, image_format)
