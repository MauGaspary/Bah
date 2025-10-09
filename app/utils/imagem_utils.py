import base64


def transformar_imagem_para_base64(caminho_imagem: str) -> str:
    with open(caminho_imagem, "rb") as imagem_file:
        imagem_bytes = imagem_file.read()
        imagem_base64 = base64.b64encode(imagem_bytes).decode("utf-8")
        return imagem_base64
