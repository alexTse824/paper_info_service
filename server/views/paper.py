import setting
from flask import Blueprint, request, jsonify, abort
from utils.crawler import GooglePaperInfoCrawler, BaiduPaperInfoCrawler


paper = Blueprint('paper', __name__)

@paper.route('/', methods=['POST'])
def get_paper_info():
    keyword = request.form['keyword']
    if not keyword:
        abort(404)
    
    engine = request.form['engine']
    if engine == 'baidu':
        crawler = BaiduPaperInfoCrawler(keyword)
        return jsonify(crawler.get_paper_cit())
    elif engine == 'google':
        crawler = GooglePaperInfoCrawler(keyword)
        return jsonify(crawler.get_paper_cit())
    else:
        abort(404)