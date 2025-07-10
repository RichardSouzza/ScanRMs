# Scanner de Termos de Uso

## Execução

### Pré-requisitos

- Ter o [Python](https://www.python.org/downloads) e o [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) instalados.
- Ter os [dados de treinamento do Tesseract](https://github.com/tesseract-ocr/tessdata/raw/main/por.traineddata)
    instalados na pasta apontada por `TESSDATA_PREFIX`.

### Atendendo aos pré-requisitos

1. Instalar o Python e o Tesseract via Scoop:

```sh
scoop install main/python
scoop install main/tesseract
```

2. Baixe os dados de treinamento por meio do link:
\
<https://github.com/tesseract-ocr/tessdata/raw/main/por.traineddata>

3. Mova os dados de treinamento para a pasta:
\
`C:\Users\richards\scoop\apps\tesseract\current\tessdata`

### Etapas para execução

1. Mova os termos de uso para a pasta "pdfs".

2. Abra o terminal na pasta do projeto.

3. Instale as dependências:

```sh
pip install -r requirements.txt
```

4. Execute o script:

```sh
python main.py
```

5. No menu que foi iniciado, selecione o termo de entrega de onde deseja extrair os dados.

6. O script copiará automaticamente o SQL gerado para a área de transferência.
