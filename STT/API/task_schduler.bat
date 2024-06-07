@echo on
call conda activate waqar_speech
uvicorn app:app --host 0.0.0.0 --port 1000 --reload