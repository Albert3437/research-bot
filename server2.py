from flask import Flask
from first_part import run
from modules.config import TOKEN_LIST

app = Flask(__name__)

number = 2

@app.route("/receive", methods=["POST"])
def receive():
    # Вот тут должен быть вызов функции для просчета метрик
    run(TOKEN_LIST[number-1])
    return "OK" 

  
if __name__ == "__main__":
    app.run(debug=True, port=5000+number)