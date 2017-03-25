import time

def from_unixtime(timestamp=time.time(), _format="%Y-%m-%d %H:%M:%S"):
	'''
	将时间戳转换为日期
	'''
	timearray = time.localtime(timestamp)
	datetime = time.strftime(_format, timearray)
	return datetime

def join(sep, args):
	'''
	连接字符串
	'''
	args_list = [];
	for item in args:
		if isinstance(item, str):
			args_list.append("%s"%item);
		elif isinstance(item, unicode):
			args_list.append("%s"%item.encode('utf-8'));
		else:
			args_list.append("%s"%str(item));
			
	return sep.join(args_list);

def log(*args, **kw):
	'''
	在控制台跟本地输出日志
	'''
	strs = join(', ', args)
	timestamp = time.time()
	timearray = str(timestamp).split('.')
	head = '[%s+%s]'%(from_unixtime(int(timestamp)), str('000' + timearray[1])[-3:])
	log_info = '%s %s'%(head, strs)
	print(log_info)
	log_info += '\n'
	with open("log.log", 'a+', encoding='utf-8') as fp:
		fp.write(log_info)
