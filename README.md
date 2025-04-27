# Monitoramento de Caminhões com YOLOv8

Este repositório contém um script em Python que utiliza a Inteligência Artificial (IA) para monitorar uma câmera de segurança em tempo real, com o objetivo de identificar caminhões passando em uma área específica. O foco é detectar caminhões-tanque, que são usados por postos de combustível para abastecer seus clientes.

## Funcionalidades

- **Detecção em tempo real**: O script usa o modelo YOLOv8 para detectar caminhões em vídeo ao vivo, conectado a uma câmera via RTSP.
- **Área monitorada**: Apenas caminhões que passam dentro de uma área específica da imagem são registrados.
- **Registro de deteções**: Quando um caminhão é detectado, uma captura de tela é salva e registrada com o timestamp no arquivo de log.
- **Detecção de caminhões de diferentes tipos**: O modelo YOLOv8 é treinado para detectar caminhões de qualquer tipo, mas está em processo de coleta de imagens para treinamento específico de caminhões-tanque.

## Como Funciona

1. **Conexão com a Câmera**: O script se conecta a uma câmera RTSP e captura frames em tempo real.
2. **Detecção de Caminhões**: Utilizando o modelo YOLOv8, o script detecta objetos na imagem e filtra para detectar apenas caminhões (classe 7).
3. **Filtro de Confiança e Proporção**: Somente detecções com uma confiança maior que 70% e com proporções que indicam caminhões são consideradas.
4. **Registro e Monitoramento**: Se o caminhão estiver dentro da área monitorada, uma imagem é salva e registrada no log.

## Requisitos

- Python 3.8+
- Bibliotecas necessárias:
  - OpenCV (`opencv-python`)
  - NumPy (`numpy`)
  - Ultralytics YOLOv8 (`ultralytics`)

### Instalação das Dependências

```bash
pip install opencv-python numpy ultralytics
```

### Uso

1. Certifique-se de ter a câmera configurada corretamente e o link RTSP disponível.

2. Altere a variável rtsp_url com o endereço da sua câmera.

3. Execute o script:

```bash
python monitoramento_cam.py
```

O script exibirá a detecção em tempo real e salvará as imagens de caminhões detectados dentro da área monitorada.

## Logs e Imagens

As imagens de caminhões detectados serão salvas com um timestamp no diretório do script. Além disso, um arquivo de log caminhoes_detectados.txt será atualizado a cada detecção.

## Contribuindo

Contribuições são bem-vindas! Se você deseja melhorar a detecção de caminhões-tanque ou adicionar novos recursos, fique à vontade para abrir um pull request.

## Licença

Este projeto está licenciado sob a MIT License.

## Contato

e-mail - gab_matheus@hotmail.com
