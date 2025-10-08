
# Projeto de Testes Automatizados (Python + Pytest + Selenium)

## Como executar localmente
```bash
python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\activate
pip install -r requirements.txt
pytest -q --maxfail=1 --disable-warnings --html=report.html --self-contained-html
```

> Observação: o projeto usa `webdriver-manager` para baixar o ChromeDriver automaticamente, mas é necessário ter o Google Chrome instalado localmente.

### Rodar apenas a suíte local
```bash
pytest -q
```

## Estrutura
- src/utils.py
- tests/unit/test_utils.py
- tests/system/test_login_system.py
- tests/system/test_cart_system.py
- .github/workflows/tests.yml

## Testes Cobertos
- **Unitários (`tests/unit/test_utils.py`)**: valida utilidades de e-mail, slug e status de prazo com casos felizes, inválidos e extremos.
- **Sistemas - Login (`tests/system/test_login_system.py`)**: cobre login válido, senha incorreta e usuário bloqueado no SauceDemo.
- **Sistemas - Carrinho (`tests/system/test_cart_system.py`)**: inclui adicionar itens, remover, persistência do carrinho após continuar comprando e tentativa de checkout sem preencher dados (cenário inválido).

---
## Integração Contínua (GitHub Actions)
O workflow em `.github/workflows/tests.yml` vai:
- Configurar Python 3.11 e instalar Google Chrome;
- Rodar pytest (unit + system);
- Publicar o `report.html` como artefato.
