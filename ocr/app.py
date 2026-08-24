from pathlib import Path
from PIL import Image, ImageOps
import pytesseract
import fitz  # PyMuPDF
import sys
import time


# ============================================================
# CONFIGURAÇÕES
# ============================================================

INPUT_DIR = Path("/app/documentos")
OUTPUT_DIR = Path("/app/output")

IDIOMA_OCR = "por+eng"

EXTENSOES_IMAGEM = {
    ".png",
    ".jpg",
    ".jpeg",
    ".tif",
    ".tiff",
    ".bmp",
    ".webp",
}

EXTENSAO_PDF = ".pdf"


# ============================================================
# PREPROCESSAMENTO DA IMAGEM
# ============================================================

def preparar_imagem(imagem: Image.Image) -> Image.Image:
    """
    Faz um pré-processamento simples para melhorar o OCR.
    """

    # Converte para RGB
    if imagem.mode != "RGB":
        imagem = imagem.convert("RGB")

    # Escala de cinza
    imagem = ImageOps.grayscale(imagem)

    # Aumenta contraste
    imagem = ImageOps.autocontrast(imagem)

    return imagem


# ============================================================
# OCR DE UMA IMAGEM
# ============================================================

def extrair_texto_imagem(imagem: Image.Image) -> str:
    """
    Executa o Tesseract em uma imagem.
    """

    imagem = preparar_imagem(imagem)

    config = "--oem 1 --psm 3"

    texto = pytesseract.image_to_string(
        imagem,
        lang=IDIOMA_OCR,
        config=config
    )

    return texto.strip()


# ============================================================
# PROCESSAR IMAGEM
# ============================================================

def processar_imagem(arquivo: Path) -> str:

    print(f"   Tipo: imagem")

    with Image.open(arquivo) as imagem:
        texto = extrair_texto_imagem(imagem)

    return texto


# ============================================================
# PROCESSAR PDF
# ============================================================

def processar_pdf(arquivo: Path) -> str:

    print(f"   Tipo: PDF")

    documento = fitz.open(arquivo)

    total_paginas = len(documento)

    print(f"   Páginas: {total_paginas}")

    textos_paginas = []

    try:

        for numero_pagina, pagina in enumerate(documento, start=1):

            print(
                f"   Processando página "
                f"{numero_pagina}/{total_paginas}..."
            )

            # Renderiza a página em resolução maior.
            # 2.0 = aproximadamente 144 DPI.
            matriz = fitz.Matrix(2.0, 2.0)

            pixmap = pagina.get_pixmap(
                matrix=matriz,
                alpha=False
            )

            # Converte para PIL
            imagem = Image.frombytes(
                "RGB",
                [pixmap.width, pixmap.height],
                pixmap.samples
            )

            texto = extrair_texto_imagem(imagem)

            textos_paginas.append(
                f"\n{'=' * 70}\n"
                f"PÁGINA {numero_pagina}\n"
                f"{'=' * 70}\n\n"
                f"{texto}"
            )

    finally:
        documento.close()

    return "\n".join(textos_paginas).strip()


# ============================================================
# PROCESSAR UM ARQUIVO
# ============================================================

def processar_arquivo(arquivo: Path):

    inicio = time.time()

    print()
    print("=" * 70)
    print(f"Arquivo: {arquivo.name}")
    print("=" * 70)

    try:

        extensao = arquivo.suffix.lower()

        if extensao == EXTENSAO_PDF:

            texto = processar_pdf(arquivo)

        elif extensao in EXTENSOES_IMAGEM:

            texto = processar_imagem(arquivo)

        else:

            print(f"   Ignorado: extensão não suportada")
            return

        # Nome do arquivo de saída
        arquivo_saida = OUTPUT_DIR / f"{arquivo.stem}.txt"

        arquivo_saida.write_text(
            texto,
            encoding="utf-8"
        )

        duracao = time.time() - inicio

        print()
        print(f"   ✓ Concluído")
        print(f"   Saída: {arquivo_saida.name}")
        print(f"   Caracteres: {len(texto):,}")
        print(f"   Tempo: {duracao:.2f}s")

    except Exception as erro:

        print()
        print(f"   ✗ ERRO")
        print(f"   {erro}")

        # Continua processando os outros arquivos.
        # Um PDF com problema não interrompe os demais.


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 70)
    print("OCR - TESSERACT")
    print("=" * 70)

    # Verifica diretórios
    INPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    # Verifica Tesseract
    try:

        versao = pytesseract.get_tesseract_version()

        print(f"Tesseract: {versao}")

    except Exception as erro:

        print("ERRO: Tesseract não encontrado.")
        print(erro)

        sys.exit(1)

    # Procura arquivos
    arquivos = sorted(
        arquivo
        for arquivo in INPUT_DIR.rglob("*")
        if arquivo.is_file()
        and (
            arquivo.suffix.lower() == ".pdf"
            or arquivo.suffix.lower() in EXTENSOES_IMAGEM
        )
    )

    print(f"Diretório de entrada: {INPUT_DIR}")
    print(f"Diretório de saída:  {OUTPUT_DIR}")
    print(f"Idioma OCR:          {IDIOMA_OCR}")
    print()
    print(f"Arquivos encontrados: {len(arquivos)}")

    if not arquivos:

        print()
        print("Nenhum arquivo encontrado.")
        return

    # Processamento
    inicio_total = time.time()

    for indice, arquivo in enumerate(arquivos, start=1):

        print()
        print(f"[{indice}/{len(arquivos)}]")

        processar_arquivo(arquivo)

    duracao_total = time.time() - inicio_total

    print()
    print("=" * 70)
    print("PROCESSAMENTO FINALIZADO")
    print("=" * 70)
    print(f"Arquivos processados: {len(arquivos)}")
    print(f"Tempo total: {duracao_total / 60:.2f} minutos")
    print("=" * 70)


if __name__ == "__main__":
    main()