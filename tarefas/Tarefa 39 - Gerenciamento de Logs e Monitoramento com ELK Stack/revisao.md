# Revisão da Tarefa

Todas as tasks foram implementadas e validadas no arquivo `logstash.conf`.

| Task | Descrição | Status |
|---|---|---|
| Criar `logstash.conf` | Criar o arquivo principal de configuração do Logstash. | OK |
| Definir `input` | Configurar a fonte dos logs com `file` + `tcp` (codec json). | OK |
| Configurar `filter` com `grok` | Extrair campos específicos (timestamp, logger, level, HTTP info). | OK |
| Configurar `filter` com `date` | Ajustar corretamente os timestamps com ISO8601. | OK |
| Configurar `output` para Elasticsearch | Enviar logs para `localhost:9200` com índice datado. | OK |
| Garantir parsing correto | Tratar JSON (json filter) e texto plano (grok com 3 patterns). | OK |
| Revisar entrega | Arquivo criado, validado e revisado — pronto para submissão. | OK |
