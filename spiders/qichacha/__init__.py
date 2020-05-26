from .qichacha import Qichacha, qcc_cookie_check

# import os 
# with open(os.path.join(os.path.dirname(__file__), 'resource/code.txt'), 'r') as f:
#     codes = f.readlines()
#     fout = open(os.path.join(os.path.dirname(__file__), 'resource/task.txt'), 'a')
#     for code in codes:
#         code = code.replace('\n', '')
#         for _ in range(6 - len(code)):
#             code = '0' + code
#         fout.write("{} 1\n".format(code))