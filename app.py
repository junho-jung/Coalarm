from flask import Flask,jsonify,render_template, request
from exchange import exchange
from getdata import corona, vaccine, kr_name, notice, noticeall
from mainstatistic import board_data
import json
import datetime


app = Flask(__name__)
@app.route('/',methods=["GET"])
def index():
    return render_template('index.html')

@app.route('/data',methods=['GET'])
def data():
    with open('./static/Test_json/api_data.json','r') as f:
            lvl_data = json.load(f)
    return jsonify({'caution':lvl_data})

@app.route('/boarddata',methods=['GET'])
def board():
    boarddata = board_data()
    return jsonify({'boarddata':boarddata})

@app.route('/country/<ISO_code>', methods=['GET'])
def country(ISO_code):
    # corona_data = Corona_data.query.filter(Coron_data.iso_code = ISO_code).first()
    # vaccine_data = Vaccine_data.query.filter(Vaccine_data.iso_code = ISO_code).first()
    # country_data = {'corona':corona_data,'vaccine':vaccine_data}
    exchange_rate = exchange(ISO_code)
    coronadata = corona(ISO_code)
    vaccinedata = vaccine(ISO_code)
    country_kr = kr_name(ISO_code)
    noticedata = notice(ISO_code)
    allnotice = noticeall(ISO_code)
    dataset = {
        'name':country_kr,'exchange':exchange_rate,'corona':coronadata,
        'vaccine':vaccinedata,'notice':noticedata,'allnotice':allnotice
        }
    return render_template('detail.html',data = dataset)


# 해당 나라 댓글 개수 알려주기
@app.route('/country/<ISO_code>/comment_update', methods=['GET'])
def get_comment_count(ISO_code):
    # comment table select query
    with open('./static/Test_json/comment.json','r') as f:  # db 업데이트
        comment = json.load(f)
    return jsonify({"count" : len(comment)})

# json 파일(db) 읽기
@app.route('/country/<ISO_code>/comment', methods=['GET'])
def comment_data(ISO_code):
    with open('./static/Test_json/comment.json', 'r') as f:
        commentDatas = json.load(f)
        result = []
        for commentData in commentDatas:
            if commentData['iso_code'] == ISO_code:
                result.append(commentData)
    return jsonify(result)

# post input : 닉네임, 내용, 비밀번호, 부모 인덱스
@app.route('/country/<ISO_code>', methods=['POST'])
def add_comment(ISO_code):
    # comment table insert query
    data = request.get_json()
    print(data)
    with open('./static/Test_json/comment.json','r') as f:  # db 대용 json 파일
        comment = json.load(f)
    data["write_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    data["index"] = len(comment)
    if data["parent"] == -1:
        data["parent"] = data["index"]
    comment.insert(0, data)

    with open('./static/Test_json/comment.json','w') as f:  # db 대용 json 파일
        json.dump(comment, f)

    # print(comment[-1])
    return jsonify({"result":"success"})

# update input : 인덱스, 비밀번호, 내용
@app.route('/country/<ISO_code>', methods=['PATCH'])
def update_comment(ISO_code):
    # comment table update query
    return

# delete input : 인덱스, 비밀번호
@app.route('/country/<ISO_code>', methods=['DELETE'])
def delete_comment(ISO_code):
    # comment table delete query
    return
    

if __name__ =="__main__":
    app.run(debug=True)
