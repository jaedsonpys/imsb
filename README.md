# IMSB - Backup de dados

O IMSB é um programa open-source que realiza o backup de diretórios
e arquivos do seu computador para um único arquivo que pode ser usado
posteriormente para recuperar seus dados.

- [Funcionamento](#Funcionamento)

# Funcionamento

Imagine a seguinte estrutura de um diretório:

```
first/
    readme.md
    app.py
    second/
        test.txt
        test_2.txt
```

O IMSB fará a leitura de cada um desses diretórios, e percorrerá todos os
subdiretórios e arquivos. Ao encontrar um arquivo, o conteúdo é lido em
bytes e transformado em **base64**, após isso, é guardado em um
dicionário com a chave sendo o nome do arquivo e o valor o próprio
**base64**:

```json
{
  "app.py": "ey7AKS93mHso..."
}
```

Quando não há mais arquivos no diretório que está sendo lido, todos os
dados que foram guardados no dicionário são salvos em um arquivo JSON,
com a chave principal sendo o nome do diretório percorrido. Veja um exemplo:

````json
{
  "first": {
    "readme.md": "ey27d4nH830...",
    "app.py": "ey7AKS93mHso..."
  },
  "first/second": {
    "test.txt": "ey93i4858fjs...",
    "test_2.txt": "eyPisMwjc34..."
  }
}
````

Isso continua ocorrendo até o diretório seja finalizado.