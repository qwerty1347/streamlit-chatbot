import base64


def get_base64_image(image_path: str) -> str:
    """
    이미지 파일을 base64 인코딩하여 문자열로 반환

    Parameters:
        image_path (str): 이미지 파일 경로

    Returns:
        str: base64 인코딩된 이미지 문자열
    """
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()