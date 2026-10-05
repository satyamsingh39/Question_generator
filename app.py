from fastapi import FastAPI, Form, Request, File, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import os
import aiofiles
import csv
from src.helper import llm_pipeline


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request}
    )


@app.post("/upload")
async def chat(request: Request, pdf_file: bytes = File(), filename: str = Form(...)):
    base_folder = 'static/docs/'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    pdf_filename = os.path.join(base_folder, filename)

    async with aiofiles.open(pdf_filename, 'wb') as f:
        await f.write(pdf_file)

    return {"msg": "success", "pdf_filename": pdf_filename}



def get_csv(file_path, question_type="Short Answer", difficulty="Medium"):
    answer_generation_chain, ques_list = llm_pipeline(
        file_path=file_path,
        question_type=question_type,
        difficulty=difficulty
    )
    base_folder = 'static/output/'
    if not os.path.isdir(base_folder):
        os.mkdir(base_folder)
    output_file = base_folder+"QA.csv"

    # Limit to first 10 questions for faster processing
    # Remove this limit if you want all questions
    ques_list = ques_list[:10]
    qa_list = []

    # Using utf-8-sig adds BOM so Excel opens CSV without garbled Unicode/characters
    with open(output_file, "w", newline="", encoding="utf-8-sig") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question", "Answer"])  # Writing the header row

        for idx, question in enumerate(ques_list, 1):
            try:
                print(f"Processing question {idx}/{len(ques_list)}: {question}")
            except UnicodeEncodeError:
                print(f"Processing question {idx}/{len(ques_list)}: {question.encode('ascii', errors='replace').decode()}")
            answer = answer_generation_chain.run(question)
            try:
                print(f"Answer: {answer}")
            except UnicodeEncodeError:
                print(f"Answer: {answer.encode('ascii', errors='replace').decode()}")
            print("--------------------------------------------------\n\n")

            # Save answer to CSV file
            csv_writer.writerow([question, answer])
            qa_list.append({
                "number": idx,
                "question": question,
                "answer": answer
            })
    return output_file, qa_list



@app.post("/analyze")
async def chat(
    request: Request,
    pdf_filename: str = Form(...),
    question_type: str = Form("Short Answer"),
    difficulty: str = Form("Medium")
):
    try:
        output_file, qa_list = get_csv(
            file_path=pdf_filename,
            question_type=question_type,
            difficulty=difficulty
        )
        return {"output_file": output_file, "qa_list": qa_list}
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"Error in analyze: {error_msg}")
        print(traceback.format_exc())
        return {"error": error_msg, "details": traceback.format_exc()}


if __name__ == "__main__":
    uvicorn.run("app:app", host='0.0.0.0', port=8080, reload=True)