Write-Host "Construindo imagem OCR..." -ForegroundColor Cyan

docker build -f Dockerfile.ocr -t dav-automation-ocr .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro ao construir a imagem." -ForegroundColor Red
    exit 1
}

Write-Host "Iniciando OCR..." -ForegroundColor Cyan

docker run --rm `
    -v "${PWD}\documentos:/app/documentos" `
    -v "${PWD}\output:/app/output" `
    dav-automation-ocr

if ($LASTEXITCODE -ne 0) {
    Write-Host "Erro durante o OCR." -ForegroundColor Red
    exit 1
}

Write-Host "OCR concluido! Resultados em .\output\" -ForegroundColor Green