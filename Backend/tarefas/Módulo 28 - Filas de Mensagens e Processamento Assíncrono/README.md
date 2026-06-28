# Ambiente Kafka Local com Docker Compose

Este projeto sobe um ambiente Kafka local com três serviços:

- **ZooKeeper** — coordenador do Kafka
- **Kafka** — message broker
- **Kafka-UI** — interface gráfica para monitoramento

## Pré-requisitos

- Docker e Docker Compose instalados

## Como executar

```bash
docker compose up -d --build
```

## Acesso

| Serviço  | Endereço                     |
|----------|------------------------------|
| Kafka    | `localhost:9092`              |
| Kafka-UI | [http://localhost:8080](http://localhost:8080) |

## Parar os serviços

```bash
docker compose down
```

## Notas

- Imagens utilizadas: `confluentinc/cp-zookeeper:7.3.2`, `confluentinc/cp-kafka:7.3.2`, `provectuslabs/kafka-ui:latest`
- A versão `7.3.2` do Kafka mantém compatibilidade com ZooKeeper (modo tradicional)
