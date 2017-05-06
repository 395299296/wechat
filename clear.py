import os
import os.path
from PIL import Image

def remove_path(path, sub=None, remain=True):
    '''
    删除所有文件
    '''
    sub = sub if sub else path;
    if not os.path.exists(sub): return;
    
    if os.path.isdir(sub):
        files = os.listdir(sub);
        for item in files:
            curr = os.path.join(sub, item);
            if item.find('.svn') != -1:
                if remain: continue;
                os.chmod(curr, '777');
            if os.path.isdir(sub):
                remove_path(path, curr);
            else:
                os.remove(curr);
        if path == sub and remain: return;
        
        files = os.listdir(sub);
        if 0 < len(files):
            time.sleep(0.1);
        os.rmdir(sub);
    else:
        os.remove(sub);

input_dir = 'girls/'
remove_dirs = []
remove_files = []
remove_imgs = []
for parent,dirnames,filenames in os.walk(input_dir):
    if len(dirnames) != 0:
        print(parent, len(dirnames), len(filenames))
        for x in dirnames:
            file = '%s/%s/个人简介.txt' % (parent, x)
            if not os.path.exists(file):
                remove_dirs.append(x)
            else:
                with open(file, 'r', encoding='utf-8') as f:
                    data = f.read()
                    keywords = ['q', 'Q', 'qq', 'QQ', '微信', '电话', '手机', '联系方式']
                    for y in keywords:
                        if y in data:
                            break
                    else:
                        remove_dirs.append(x)
        for x in filenames:
            basename = os.path.splitext(x)[0]
            if not os.path.exists(input_dir + basename):
                remove_files.append(x)
    else:
        for x in filenames:
            file = '%s/%s' % (parent, x)
            extname = os.path.splitext(x)[1]
            if extname == '.jpg':
                try:
                    img = Image.open(file)
                    if img.size[0] < 100 or img.size[1] < 100:
                        remove_imgs.append(file)
                except Exception as e:
                    print(e)

print('remove', len(remove_dirs), len(remove_files), len(remove_imgs))

for x in remove_dirs:
    rmdir = input_dir + x
    remove_path(rmdir,  rmdir, False)
    file = '%s%s.jpg' % (input_dir, x)
    if os.path.exists(file): 
        os.remove(file)

for x in remove_files:
    basename = os.path.splitext(x)[0]
    rmdir = input_dir + basename
    remove_path(rmdir,  rmdir, False)
    os.remove(input_dir + x)

for x in remove_imgs:
    os.remove(x)
