# Galeria de aniversário — base inicial

Projeto inicial em **Python + Streamlit + Supabase**. Os convidados podem enviar fotos (sem código), ver a galeria coletiva e escrever uma legenda. A área administrativa permite excluir publicações.

## O que esta base faz

- Layout adaptável para celular e computador.
- Upload múltiplo de JPG, JPEG, PNG e WEBP.
- Redimensiona imagens para até 2000 × 2000 pixels e converte para JPEG.
- Limite de 10 MB por arquivo antes da conversão.
- Guarda arquivos no Supabase Storage e metadados na tabela `photos`.
- Galeria com filtro por nome/legenda.
- Área administrativa protegida por um código simples.


## Estrutura

```text
galeria_aniversario/
├── app.py
├── requirements.txt
├── supabase_setup.sql
├── README.md
├── .gitignore
└── .streamlit/
    └── secrets.toml.example
```
