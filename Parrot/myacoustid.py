import acoustid
import chromaprint
import glob
import pickle

popcnt_table_8bit = [
    0,1,1,2,1,2,2,3,1,2,2,3,2,3,3,4,1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,
    1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
    1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
    2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
    1,2,2,3,2,3,3,4,2,3,3,4,3,4,4,5,2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,
    2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
    2,3,3,4,3,4,4,5,3,4,4,5,4,5,5,6,3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,
    3,4,4,5,4,5,5,6,4,5,5,6,5,6,6,7,4,5,5,6,5,6,6,7,5,6,6,7,6,7,7,8,
]

def build_fp():
    all_fp = []
    count = 0
    for file_name in glob.glob('*.mp3'):
        tmp_fp = []
        tmp_fp.append(file_name[:-4])
        tmp = acoustid.fingerprint_file(file_name)
        decode_fp = chromaprint.decode_fingerprint(tmp[1])[0]
        tmp_fp.append(decode_fp)
        all_fp.append(tmp_fp)
        count = count + 1
        print("fp for music", file_name[:-4], "generated", "Total:", count)
    f = open('all_fp.dat', 'wb')
    pickle.dump(all_fp, f)
    f.close()

def popcnt(x):
    """
    Count the number of set bits in the given 32-bit integer.
    """
    return (popcnt_table_8bit[(x >>  0) & 0xFF] +
            popcnt_table_8bit[(x >>  8) & 0xFF] +
            popcnt_table_8bit[(x >> 16) & 0xFF] +
            popcnt_table_8bit[(x >> 24) & 0xFF])

def compare_fp(fp1, fp2):
    error = 0
    for x, y in zip(fp1, fp2):
        error += popcnt(x ^ y)
    #print("Compare value is:", 1.0 - error / 32.0 / min(len(fp1), len(fp2)))
    #print (1.0 - error / 32.0 / min(len(fp1), len(fp2)))
    return 1.0 - error / 32.0 / min(len(fp1), len(fp2))

def search_fp(file_name):
    return_score = []
    f = open('all_fp.dat', 'rb')
    all_fp = pickle.load(f)
    f.close()
    input_mp3 = acoustid.fingerprint_file(file_name)
    input_fp = chromaprint.decode_fingerprint(input_mp3[1])[0]
    for i in all_fp:
        #print("compare test mp3 and", i[0])
        tmp = []
        tmp.append(i[0])
        tmp.append(compare_fp(input_fp, i[1]))
        return_score.append(tmp)
    return_score.sort(key=lambda x:x[1], reverse=True)
    #print(return_score[:20])
    return return_score[:5]

# test = acoustid.fingerprint_file('../test.mp3')
# test2 = acoustid.fingerprint_file('../1.mp3')
# # print(test[1])
# # print("After decode")
# # print(chromaprint.decode_fingerprint(test[1])[0])
# fp1 = chromaprint.decode_fingerprint(test[1])[0]
# fp2 = chromaprint.decode_fingerprint(test2[1])[0]
# compare_fp(fp1, fp2)
# error = 0
# for x, y in zip(fp1, fp2):
#     error += popcnt(x ^ y)
# #print("Compare value")
# #print (1.0 - error / 32.0 / min(len(fp1), len(fp2)))
# print("Compare value is:", 1.0 - error / 32.0 / min(len(fp1), len(fp2)))
#build_fp()
#search_fp('326785.mp3')
