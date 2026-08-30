.PHONY: all help install-cli check-deps test clean

all: help

help:
	@echo "=========================================="
	@echo "  ABNT UNISA — Automação de Documentos   "
	@echo "=========================================="
	@echo "Alvos disponíveis:"
	@echo "  make install-cli  - Instala format-doc e abnt-unisa em ~/.local/bin"
	@echo "  make check-deps   - Verifica dependências de sistema (Chrome, LibreOffice, Python)"
	@echo "  make test         - Testa a compilação do documento de exemplo"
	@echo "  make clean        - Remove arquivos intermediários gerados nos testes"

install-cli:
	@./bin/abnt-unisa install-cli

check-deps:
	@./bin/abnt-unisa check-deps

test:
	@echo "📄 Executando teste de compilação..."
	@./bin/abnt-unisa examples/exemplo_resenha.md
	@echo "✅ Teste concluído com sucesso! Verifique examples/exemplo_resenha.pdf"

clean:
	@rm -f examples/*.html examples/*.pdf examples/*.docx
	@echo "🧹 Arquivos de teste limpos."
