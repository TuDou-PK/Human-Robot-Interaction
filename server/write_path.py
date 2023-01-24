import os

def write_path(file_name, path):
    with open('/home/robot/playground/html/sample1/actions/' + file_name, 'w') as f:
        f.write('IMAGE\n')
        f.write('<*,*,*,*>:  img/a_map.png\n')
        f.write('----\n')
        f.write('TEXT\n')
        f.write('<*,*,*,*>: ' + path + '\n')
        f.write('----\n')
        f.write('TTS\n')
        f.write('<*,*,*,*>: ' + path + '\n')
        f.write('----\n')
