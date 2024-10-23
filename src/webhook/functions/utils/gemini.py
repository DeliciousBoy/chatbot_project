import pandas as pd 
import numpy as np
from FlagEmbedding import BGEM3FlagModel
import google.generativeai as genai
import pickle
import json
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from googleapiclient.discovery import build
from google.oauth2 import service_account
import io
from googleapiclient.http import MediaIoBaseDownload
from datetime import datetime
import schedule

load_dotenv()
sys.path.append(r"C:\Users\ASUS\OneDrive\เอกสาร\GitHub\chatbot_project")
from src.config import RAW_DATA_DIR,PROCESSED_DATA_DIR

BGEmodel = BGEM3FlagModel('BAAI/bge-m3',use_fp16=True)
SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = PROCESSED_DATA_DIR /'SERVICE_ACCOUNT_FILE.json'
PARENT_FOLDER_ID = os.getenv("PARENT_FOLDER_ID")

genai.configure(api_key=os.getenv("API_KEY"))
generation_config = {
        "temperature": 0.3,
        "top_p": 0.50,
        "top_k": 32,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

version = 'models/gemini-1.5-flash' # @param ["models/gemini-1.5-flash", "models/gemini-1.5-pro", "models/gemini-1.0-pro"]
genaimodel = genai.GenerativeModel(version,generation_config=generation_config)
Sales_Expert = genaimodel.start_chat(history=[])

def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds
def find_file(service, file_name):
    query = f"name='{file_name}' and '{PARENT_FOLDER_ID}' in parents and trashed=false"
    results = service.files().list(q=query, spaces='drive', fields="files(id, name)").execute()
    files = results.get('files', [])
    return files[0] if files else None

def download_file(destination_path):
    creds = authenticate()
    service = build('drive', 'v3', credentials=creds)
    # Extract the file name from the destination path
    file_name = os.path.basename(destination_path)
    
    existing_file = find_file(service, file_name)
    if not existing_file:
        # print(f"File '{file_name}' not found in the specified folder.")
        return

    file_id = existing_file['id']
    # Download the file from Google Drive
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(destination_path, 'wb')  # Open the destination file for writing

    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
        # print(f"Download progress: {int(status.progress() * 100)}%")

    print(f"File downloaded to {destination_path}")
    
def load_data():
    download_file(PROCESSED_DATA_DIR / "product_data.csv")
    download_file(PROCESSED_DATA_DIR / "product_data_embeddings.pkl")
    
def task_every_1th():
    # ตรวจสอบว่าปัจจุบันเป็นวันที่ 29 หรือไม่
    today = datetime.now().day
    if today == 1:
        # print("It's the 29th! Running the scheduled task.")
        # เรียกใช้ฟังก์ชันของคุณที่นี่
        load_data()
    else:
        # print("Today is not the 29th. Task skipped.")
        return

def create_prompt(user_input):
    raw_product_article = pd.read_csv(PROCESSED_DATA_DIR / "product_data.csv", header=None)
    product_article = raw_product_article.values.tolist()

    embeddings_1 = BGEmodel.encode(user_input, 
                            batch_size=8, 
                            max_length=1200,
                            )['dense_vecs']
    with open(PROCESSED_DATA_DIR / "product_data_embeddings.pkl", 'rb') as f:
        embeddings_2_loaded = pickle.load(f)
    similarity = embeddings_1 @ embeddings_2_loaded.T

# หาค่ามากที่สุดและ index ของมัน
    max_value_index = np.argmax(similarity)
    max_value = similarity[max_value_index]
    # print(max_value_index)
# หาค่าที่น้อยกว่าหรือเท่ากับ 10% ของค่ามากสุด และเก็บ index ของมัน
    threshold = max_value * 0.85
    indices_below_threshold = np.where(similarity >= threshold)[0]
    # print(indices_below_threshold)
    sorted_indices = indices_below_threshold[np.argsort(-similarity[indices_below_threshold])]
    # print(sorted_indices)
    relative_doc = [product_article[i] for i in sorted_indices[:150]]
            
    prompt = f"""คุณคือ ผู้ที่ชำนาญด้านการเป็นผู้ช่วยในการขายและเป็นผู้เชี่ยวชาญเกี่ยวกับสินค้า คุณสามารถให้ข้อมูลและให้คําปรึกษาเกี่ยวกับผลิตภัณฑ์ต่างๆ
    
คำถาม : {user_input}
ข้อมูลที่เกี่ยวข้อง : {relative_doc}

โปรดให้คำตอบโดย:
- เน้นคำตอบที่ตรงประเด็น
- แนะนำสินค้าให้เหมาะสมกับความต้องการของลูกค้า
- หากเป็นไปได้ ให้เปรียบเทียบกับสินค้าประเภทเดียวกันเพื่อช่วยให้ลูกค้าตัดสินใจได้ง่ายขึ้น
- ตอบด้วยภาษาที่เป็นมิตรและชัดเจน
"""
    return prompt

def sale_ex(prompt):
# prompt = "เอสซีจี รุ่นคลาสสิคไทย มีสีอะไรบ้าง แล้วแต่ละอันราคาเท่าไร"
    Sales_Expert.send_message(prompt)
# model.count_tokens(prompt)
    respon = Sales_Expert.last.text
    return respon

if __name__ == "__main__":
    task_every_1th()
    # อ่าน input จาก Node.js ผ่านทาง argument ที่ส่งมา
    # schedule.every().day.at("13:51").do(task_every_29th)
    # schedule.run_pending()
    input_data = sys.argv[1] 
    # input_data = 'ขอราคาของกระเบื้อง'
    # เรียกใช้งานฟังก์ชัน
    prompt = create_prompt(input_data)
    result = sale_ex(prompt)
    # print(result)
    # ส่งผลลัพธ์กลับไปในรูปแบบ JSON
    print(json.dumps({"result": result}))
    
    
