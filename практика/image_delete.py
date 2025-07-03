import os
import glob

def delete_image():
    # Путь к папке, где лежат изображения
    folder_path = r"C:\Users\nurmukhamed.timuruly\OneDrive - Freedom Holding Corporation\Рабочий стол\практика\practice_pars_and_ml\image"

    # Список шаблонов расширений, которые будем удалять
    extensions = ("*.jpg", "*.jpeg", "*.png", "*.gif", "*.bmp", "*.tiff", "*")

    for ext in extensions:
        # Собираем все файлы по шаблону
        pattern = os.path.join(folder_path, ext)
        for file_path in glob.glob(pattern):
            try:
                os.remove(file_path)            
            except Exception as e:
                print(f"Не удалось удалить {file_path}: {e}")
