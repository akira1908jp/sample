
#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import wsgiref.handlers
from google.appengine.ext import webapp

#テンプレートを使用するため、下記二つのimportを追加
import os
from google.appengine.ext.webapp import template

#データベースを使用するため、importを追加
from google.appengine.ext import db

#データベース登録用のクラス
class Post(db.Model):
    #郵便番号
    zip_code = db.StringProperty(required=True)
    #住所
    address = db.StringProperty(required=True)

class MainHandler(webapp.RequestHandler):

    def get(self):
        zip_code = self.request.get("zip_code")
        template_values = {}

        if zip_code:
            query = Post.all()
            query.filter('zip_code =', zip_code)

            address = "対象のデータが見つかりません"
            for result in query:
                address = result.address

            #連想配列にテンプレートに渡す値を設定
            #テンプレートからは、連想配列のキーでアクセスする。
            template_values = {'zip_code' : zip_code, 'address' : address}

        #使用するテンプレートを指定
        path = os.path.join(os.path.dirname(__file__), 'template/index.html')
        #レンダリングを実行し、結果をレスポンスとしてブラウザに返却
        self.response.out.write(template.render(path, template_values))

    def post(self):
        #入力された郵便番号、住所を取得
        rquest_zip_code = self.request.get("zip_code")
        rquest_address = self.request.get("address")

        #データの登録実行
        post = Post(zip_code=rquest_zip_code, address=rquest_address)
        post.put()

        #最初の画面にリダイレクト
        self.redirect("/")


#def main():
application = webapp.WSGIApplication([('/', MainHandler)],  debug=True)
#    wsgiref.handlers.CGIHandler().run(application)


#if __name__ == '__main__':
#    main()
