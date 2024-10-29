import os
import json
import requests
from dotenv import load_dotenv
import pandas as pd
import time
from function.analyzePromt import analyze_data

load_dotenv()

url = f"{os.getenv('URL_API')}/teacher_comments"

prompt = """You are an analyst and you will help me interpret a csv, I will pass you the content separated with commas and you will generate a SWOT analysis of the teacher based on the comments of his students, 
the file contains information about the teacher, the course, the aspect, the predominant emotion in each sentence and the feeling if it is positive or negative, the aspects are from 1 to 4 and each aspect refers to specific points that are being evaluated of the teacher, 
The aspects refer to: 1.- mastery of the subject, planning, motivation, course management and general satisfaction. 2.- strategies, methods, techniques and learning environments 3.- evaluation, communication and course management. 4.- This focuses directly on the use of ICTs. 
I want the response to be in json format only and return the SWOT analysis, a comment summarizing the students' comments in general, the relationship between positive and negative by aspects to be able to make a stacked bar graph, 
a teacher rating based on numbers from 1 to 5 points based on the positive and negative where they can be better evaluated and where not to generate a radar graph, and the feelings that their students feel to generate a pie chart, 
this data is important to be able to generate graphs of their performance, the output json must contain the following: SWOT 'strengths, weaknesses, opportunities, threats', summaryComment, ratingsAspects, teacherEvaluations, sentiment. 
Restrictions: do not use markup language or line breaks, I want the response to be a json to store it in a string. The output json must follow this format: {"idTeacher": "idTeacher","idCourse": "idCourse","SWOT": {"strengths": ["Regular evaluation and alignment of exams with class content."], "weaknesses": ["Lack of dynamic teaching methods and poor planning."], "opportunities": ["Improvement in teaching strategies and methods."], "threats": ["Student dissatisfaction leading to negative perceptions of the course."]}, "summaryComment": "Students expressed disappointment in the teacher's methods and planning, although they appreciated the evaluation process.", "ratingsAspects": {"1": {"positive": 0, "negative": 4}, "2": {"positive": 0, "negative": 2}, "3": {"positive": 2, "negative": 0}, "4": {"positive": 0, "negative": 0}}, "teacherEvaluations": {"1": 1, "2": 1, "3": 5, "4": 3}, "emotions": {"sad": 2, "happy": 6 ...}}
the result must be in spanish"""

def analysis_teacher():
    response = requests.get(url)
    urlSaveData = f"{os.getenv('URL_API')}/saveEvaluation"

    if response.status_code == 200:
        
        data = response.json()

        for teacher in data:
            records = []
            idTeacher = teacher["idTeacher"]
            idCourse = teacher["idCourse"]
            for aspect in teacher["aspects"]:
                aspect_id = aspect["aspect"]
                for comment in aspect["positive_comments"]:
                    records.append({
                        "idTeacher": idTeacher,
                        "idCourse": idCourse,
                        "aspect": aspect_id,
                        "comment": comment["comment"],
                        "predominant_emotion": comment["predominant_emotion"],
                        "sentiment": "positive"
                    })
                for comment in aspect["negative_comments"]:
                    records.append({
                        "idTeacher": idTeacher,
                        "idCourse": idCourse,
                        "aspect": aspect_id,
                        "comment": comment["comment"],
                        "predominant_emotion": comment["predominant_emotion"],
                        "sentiment": "negative"
                    })

            df = pd.DataFrame(records)
            df_string = df.to_string()
           
            df_string = df.to_csv(index=False, sep=',')
           
            result=analyze_data(df_string, prompt)
            data = json.loads(result)
           
            response = requests.post(urlSaveData, json=data)
            
            time.sleep(15)
           
        return {"message": "The analysis of the teachers' comments has been completed."}
    else:
        print("Error:", response.status_code, response.text)
        return {"error": "Ocurrió un error al llamar a la API."}