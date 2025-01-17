# Pacotes
import os
import time
import subprocess
import json
import logging
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload  
import paho.mqtt.client as mqtt
from inference_sdk import InferenceHTTPClient
import supervision as sv
import cv2

# Variáveis globais
SERVICE_ACCOUNT_FILE = '/home/tccunip/python_scripts/pavision-428222-25bf95f32da1.json'  # Substitua pelo caminho do seu arquivo JSON
PHOTO_DIRECTORY_not_process = '/home/tccunip/fotos'
PHOTO_DIRECTORY_analyzed = '/home/tccunip/fotos_analisadas'
TARGET_FOLDER_ID_not_process = ''  # Substitua pelo ID da sua pasta no Google Drive
TARGET_FOLDER_ID_analyzed = '' # Substitua pelo ID da sua pasta no Google Drive
taking_pictures = False

# Configurações do log

logging.basicConfig(level=logging.DEBUG, format = '%(asctime)s - %(levelname)s - %(message)s',
                   handlers=[
                        logging.FileHandler('app.log'),
                        logging.StreamHandler()
                   ])
logger = logging.getLogger(__name__)

logger.debug('Iniciando app')

logger.info('Conectando ao broker MQTT')

# Função para autenticar no Google Drive
def authenticate():
    try:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive'])
        return creds
        logger.debug(f'Autentiação API Google realizada com sucesso')
    except Exception as e:
        logger.error(f'Erro ao autenticar, verifique as variáveis globais: {str(e)}')

# Função para enviar um arquivo para o Google Drive
def upload_file_to_drive(file_path, folder_id):
    try:
        service = build('drive', 'v3', credentials=authenticate())
        file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
        media = MediaFileUpload(file_path, mimetype='image/jpeg', resumable=True)  
        file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
        logger.debug(f'Foto enviado para a cloud')
    except Exception as e:
        logger.error(f'Erro ao enviar a imagem via API {str(e)}')

# Função que ativa a câmera e tira a foto
def take_photo(file_path):
    try:
        subprocess.run(["libcamera-still", "-o", file_path, "--nopreview"], check=True, timeout=25)
        upload_file_to_drive(file_path, TARGET_FOLDER_ID_not_process)
        logger.debug(f'Diferença de distância detectada, foto tirada e salva')
    except Exception as e:
        logger.error(f'Erro ao tirar a foto, verifique o funcionamento da câmera {str(e)}')

# Função para análise da imagem
def image_analyzer(image_send, x):
    
    # define the image url to use for inference
    image_file = image_send
    image = cv2.imread(image_file)

    try:
        # load a pre-trained yolov8n model
        CLIENT = InferenceHTTPClient(
            api_url="https://outline.roboflow.com",
            api_key="riL3EMHt2qsMel1fp3D1"
        )

        # run inference on our chosen image, image can be a url, a numpy array, a PIL image, etc.
        results = CLIENT.infer(image_file, model_id="patologias-pavimento-2/1")

        # load the results into the supervision Detections api
        detections = sv.Detections.from_inference(results)

        # create supervision annotators
        bounding_box_annotator = sv.BoxAnnotator()
        label_annotator = sv.LabelAnnotator()

        # annotate the image with our inference results
        annotated_image = bounding_box_annotator.annotate(
            scene=image, detections=detections)
        annotated_image = label_annotator.annotate(
            scene=annotated_image, detections=detections)
        logger.debug(f'Foto analizada')
    except Exception as e:
        logger.error(f'Erro ao analisar a foto, verifique o funcionamento do modelo {str(e)}')

    try:
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        
        os.chdir(PHOTO_DIRECTORY_analyzed)
        filename = f'foto_{timestamp}_{x}_analyzed.png'
        cv2.imwrite(filename, annotated_image)

        file_path_analyzed = os.path.join(PHOTO_DIRECTORY_analyzed, f'foto_{timestamp}_{x}_analyzed.png')
        upload_file_to_drive(file_path_analyzed, TARGET_FOLDER_ID_analyzed)
        logger.debug(f'Foto analizada e enviada')
    except Exception as e:
        logger.error(f'Erro ao enviar a foto analizada, verifique o funcionamento do envio {str(e)}')

# Função para conectar no contexto do ESP32
def on_connect(client, userdata, flags, rc):
    try:
        client.subscribe("sensor/ultrasonic")
        logger.debug(f'Conectado no contexto, recebendo informações da distância')
    except Exception as e:
        logger.error(f'Erro ao se conectar ao contexto, verfique as configura ção do ESP {str(e)}')

# Função de contexto, para executar as ações
def on_message(client, userdata,msg):
    try:
        global taking_pictures
        data = json.loads(msg.payload.decode()) #decodifica o JSON
        distancia =  float(data["distance"]) # extrai o valor da distancia
        if distancia < 20:
            if not taking_pictures:
                taking_pictures = True
            if taking_pictures:
                    foto = 1
                    while foto <= 3:
                        timestamp = time.strftime("%Y%m%d-%H%M%S")
                        file_path = os.path.join(PHOTO_DIRECTORY_not_process, f'foto_{timestamp}_{foto}.jpg')
                        take_photo(file_path)
                        image_analyzer(file_path, foto)
                        foto+=1
        else:
            if taking_pictures:
                taking_pictures = False
    except Exception as e:
        logger.error(f'Erro na função de contexo, verifique à aplicação {str(e)}')
        
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("localhost", 1883, 60)
client.loop_forever()
