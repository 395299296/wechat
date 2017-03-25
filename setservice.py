from urllib import request, parse

def add():
	account_data = {
	     "kf_account" : "kefu@liaotian2020",
	     "nickname" : "你不懂不怪你",
	     "password" : "123456",
	}
	account_data_urlencode = parse.urlencode(account_data).encode('utf-8')

	requrl = "https://api.weixin.qq.com/customservice/kfaccount/add?access_token=91930762d6cc738b"

	req = request.Request(url = requrl,data =account_data_urlencode)
	print(req)

	res_data = request.urlopen(req)
	res = res_data.read()
	print(res)

if __name__ == '__main__':
	add()