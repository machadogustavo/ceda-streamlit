# Documentação do Projeto Streamlit: Data Extract from CEDA

## Introdução

Este projeto é um aplicativo desenvolvido em Streamlit para extrair e processar dados de estações climáticas e compará-los com datasets climáticos disponíveis. Ele é projetado para trabalhar com dados do CEDA e INMET, utilizando ferramentas como Google Sheets e AWS S3 para armazenamento e processamento.

### Autor

- Gustavo Machado - UNIFESSPA
- Repositório: [CEDA Streamlit](https://github.com/machadogustavo/ceda-streamlit)
- Versão: 1.0.0

---

## Funcionalidades

O aplicativo possui as seguintes páginas:

### 1. **Data Extract from CEDA**

#### a. **Sobre**

Seção inicial com apresentação e descrição geral do projeto.

#### b. **Início**

Guia o usuário pelo aplicativo, explicando a finalidade de cada aba e fornecendo orientações gerais sobre como utilizá-lo.

### 2. **Estações**

Apresenta as estações disponíveis com as seguintes informações:

- DC_NOME
- Cidade
- Sigla do Estado (SG_ESTADO)
- Latitude (VL LATITUDE)
- Longitude (VL LONGITUDE)
- Bioma

### 3. **Tabela de Estações**

Exibe os dados das estações em formato tabular, permitindo visualização e gerenciamento das estações.

### 4. **Dados**

Seção geral para visualização dos dados de captação das coordenadas de temperatura e precipitação, subdividida em:

#### a. **Dados CEDA**

Contém informações processadas a partir do dataset **cru_ts4.08.1901.2023.pre.dat.nc** (Precipitação) e do dataset **cru_ts4.08.1901.2023.tem.dat.nc** (Temperatura) disponível em:  
[https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.08/cruts.2406270035.v4.08](https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.08/cruts.2406270035.v4.08)

#### b. **Dados INMET**

Apresenta dados reais de estações INMET para visualização.

### 5. **Comparativo**

Seção de comparação entre os dados do CEDA e do INMET.

#### a. **Comparativo KGE**

Utiliza o coeficiente Kling-Gupta Efficiency (KGE) para análise de similaridade entre os datasets processados e os dados reais das estações.

---

## Configuração do Projeto

### Pré-requisitos

- Python 3.8 ou superior
- Biblioteca Streamlit
- Conta no Google Cloud com acesso ao Google Sheets API
- AWS S3 configurado para armazenamento de datasets

### Estrutura do Projeto

```bash
project/
├── app.py              # Código principal do Streamlit
├── tabs/               # Pastas com as abas das páginas
├── pages/
├── utils/
├── README.md           # Documentação do projeto
├── requirements.txt
```

### Configuração do `secrets.toml`

Crie o arquivo [`secrets.toml`](https://docs.streamlit.io/develop/api-reference/connections/secrets.toml) para armazenar informações sensíveis, como credenciais de APIs e configuração de AWS S3.

```toml
[connections.gsheets]
spreadsheet= ""
worksheet = ""
project_id = ""
client_email = "seu-email-do-google-cloud"
private_key = "sua-chave-privada"

[ceda_credentials]
username = ""
password = ""
access_token = ""
```

---

## Como Rodar Localmente

1. Clone o repositório:
   ```bash git clone https://github.com/machadogustavo/ceda-streamlit.git cd ceda-streamlit```

2. Instale as dependências:
   ```bash pip install -r requirements.txt```

3. Certifique-se de que o arquivo `secrets.toml` está configurado corretamente.

4. Execute o aplicativo:
   ```bash streamlit run app.py```

5. Acesse o aplicativo em:  
   `http://localhost:8501`

---

## Deploy

O aplicativo pode ser implantado em serviços como Streamlit Cloud, AWS ou outros provedores.

### Implantação no Streamlit Cloud

1. Faça login no [Streamlit Cloud](https://share.streamlit.io/).
2. Crie um novo aplicativo e conecte o repositório GitHub.
3. Certifique-se de adicionar as variáveis do `secrets.toml` na seção de configurações do aplicativo no Streamlit Cloud.

---

## Referências

- [Streamlit Documentation](https://docs.streamlit.io/)
- [Google Sheets API](https://docs.streamlit.io/develop/tutorials/databases/private-gsheet)
- [AWS S3 Integration](https://docs.streamlit.io/develop/tutorials/databases/aws-s3)
- [Dataset CEDA](https://crudata.uea.ac.uk/cru/data/hrg/cru_ts_4.08/cruts.2406270035.v4.08/pre/)
- [KGE - Kling-Gupta Efficiency](https://permetrics.readthedocs.io/en/latest/pages/regression/KGE.html)
