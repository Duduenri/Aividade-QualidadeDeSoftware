
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

## Estrutura
- src/utils.py
- tests/unit/test_utils.py
- tests/system/test_login_system.py
- tests/system/test_cart_system.py
- .github/workflows/tests.yml

---
## Integração Contínua (GitHub Actions)
O workflow em `.github/workflows/tests.yml` vai:
- Configurar Python 3.11 e instalar Google Chrome;
- Rodar pytest (unit + system);
- Publicar o `report.html` como artefato.
