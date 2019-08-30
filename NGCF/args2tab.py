outfile = open('tb_args_performance.csv', 'w')

def str2intlist(s):
    s = s.strip('[').strip(']').split(',')
    l = [int(i) for i in s]
    return l

unprint_args = ['pretrain', 'epoch', 'weights_path', 'regs', 'alg_type', 'gpu_id',  'adj_type',
                'embed_size', 'Ks', 'data_path',  'test_flag', 'report_loop', 'mess_dropout',
                'verbose', 'dataset', 'model_type', 'report', 'lr', 'save_flag', 'proj_path',
                'keep_prob', 'save_print_flag']

with open('args_performance.txt', 'r') as infile:
    odd_flag = 0
    header_flag = 1
    field_name_dic = {}
    field_name_list_keys = []
    list_ks = []
    print_args = []
    
    for l in infile.readlines():
        l = l.strip('\n')
        odd_flag = 1 - odd_flag
        
        if odd_flag:
            # Namespace(Ks='[10]', adj_type='norm', ...)
            l = l.strip('Namespace').strip('(').strip(')').replace("'","")
            for field in l.split(', '):
                field = field.split('=')
                if field.__len__() > 1:
                    field_name_dic[field[0]] = field[1]
                else:
                    field_name_dic[field[0]] = ''
                
            if header_flag:
                list_ks = str2intlist(field_name_dic['Ks'])
                headline = 'idx,t_train'  # headline = 'idx,t_train,Recall,Precision,HR,NDCG'
                for fn in ['Recall','Precision','HR','NDCG']:
                    for k in list_ks:
                        headline += ',' + fn + '@' + str(k)
                field_name_list_keys = field_name_dic.keys()
                
                print_args = list(set(field_name_list_keys) - set(unprint_args))
#                 for fn in field_name_list_keys:
                for fn in print_args:
                    headline += ',' + fn
                headline = headline.replace(',','\t')
                print(headline, file=outfile)
                header_flag = 0
        else:
            # idx,t_train,Recall,Precision,HR,NDCG
#             outline = l.replace(',','\t')
#             list_ks = field_name_dic['Ks']
            l = l.split('\t')
            outline = l[0] + '\t' + l[1]
            for li in l[2:]:
                li = li.strip('[').strip(']').replace("'",'').replace(', ','\t')
                outline += '\t' + li
#             for k in field_name_list_keys:
            for k in print_args:
                outline += '\t' + field_name_dic[k]
            print(outline, file=outfile)

outfile.close()

