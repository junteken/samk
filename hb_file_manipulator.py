# braket_server_list = {'다12':('입춘대길', '탄금주적'), 
#                '다11':('원문사극', '진북론천'),
#                '라5' :('언과기실', '백리지재'),
#                'H1' : ('우공이산', '천지개벽'),               
#                }

braket_server_list = {'입춘대길':'다12', 
               '원문사극' : '다11',
               '언과기실' :'라5',
               '우공이산' :'H1',
               }




def getserverlist(filename):
        filepath = './rsrc/' + filename
        sv_list = []
        with open(filepath, "r", encoding="utf-8") as file:
            sv_list = [line.strip() for line in file]

        return sv_list



# original_list = getserverlist('hb')
# merge_str = None
# new_sv_list = []


# with open('./rsrc/hb_new', "w", encoding="utf-8") as file:            
#     for sv in original_list:
#         if sv == '입춘대길':
#             merge_str = braket_server_list['입춘대길']
#         elif sv == '원문사극':
#             merge_str = braket_server_list['원문사극']
#         elif sv == '언과기실':
#             merge_str = braket_server_list['언과기실']
#         elif sv == '우공이산':
#             merge_str = braket_server_list['우공이산']

#         new_sv = '[' + sv + ']' + merge_str
#         file.write(new_sv+'\n')

#         if sv == '천지개벽':
#             break

with open('./rsrc/S001', "w", encoding="utf-8") as file:            
    three_digit_numbers = [f"{i:03}" for i in range(1, 146)]

    for sv in three_digit_numbers:
        file.write('[S '+ sv +']\n')




      
