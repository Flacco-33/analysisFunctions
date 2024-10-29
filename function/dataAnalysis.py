import os
import json
import requests
from dotenv import load_dotenv
from function.analyzePromt import analyze_data

load_dotenv()
# Define la URL de la API
url = f"{os.getenv('URL_API')}/dataMatch"

prompt ="Generates a JSON string representing information about a student, a teacher, and an analysis of their experience in a course. The JSON must include the following fields: idStudent, idTeacher, aspect, idCourse, sentiment, comment, and predominant_emotion. The predominant emotion must be determined based on the provided emotions. The output must be a single line with no newline characters. Example of input data: idStudent: '13TL1234', idTeacher: '30TE8902', aspect: 4, idCourse: 'BasesFilosoficas', comment: 'Well, the use of technology was good, since the teacher did let us upload the tasks through the digital platform. So, no problem. The only thing I would put the firefighter on was the means of communication, since he did not let us contact him by any other means other than being present in the classroom.', sentiment: 'neutral', emotions: happy: 0.2, sad: 0, anger: 0, surprise: 0, neutral: 0.6, disgust: 0, fear: 0, contempt: 0.2 Example of expected output: {'idStudent':'13TL1234','idTeacher':'30TE8902','aspect':4,'idCourse':'BasesFilosoficas','sentiment':'neutral','comment':'Well, the use of technology was good, since the teacher did let us upload the assignments through the digital platform. So, no problem. The only thing I would put him down for was the means of communication, since he didn't let us contact him by any other means than being present in the classroom.','predominant_emotion':'neutral'}"

def analysis_data_match():
    
    response = requests.get(url)
    urlSaveData = f"{os.getenv('URL_API')}/storeDocument"

    if response.status_code == 200:
        
        data = response.json()
        
        for match in data["dataMatch"]:
            analyzeData= analyze_data(match, prompt)
            print(analyzeData)
            # data = json.loads(analyzeData)
           
            # response = requests.post(urlSaveData, json=data)
            
        return {"status": "data celean"}
    else:
        print("Error:", response.status_code, response.text)
        return {"error": "Ocurrió un error al llamar a la API."}