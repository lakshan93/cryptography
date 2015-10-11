import sys
english_dic = {}

def read_dict():
    with open("english.dic") as f:
        for line in f:
            (key, val) = line.split(',')
            english_dic[key] = int(val)

def rotate_sentence(sent, rot):
    rotatedWord = ""
    for c in sent:
        ascii = ord(c)
        if ascii >= 97 and ascii < 123:
            rotatedWord += str(unichr((ascii - 97 + rot)%26 + 97))
        else:
            rotatedWord += c
    return rotatedWord
            
def checkValidWords(rotated_sentence):
    valid_words_count = 0
    for word in rotated_sentence:
        if word in english_dic:
            valid_words_count += 1
            english_dic[word] += 1
    return valid_words_count

def decrypt(sentence, key = -1):
    if key != -1:
        print 'Decrypting the message with key...'
        return [key, rotate_sentence(sentence, -key)]
    else:
        print 'Decrypting the message without key (brute force)...'
        read_dict()
        max_match = 0
        max_match_sent = ''
        words_in_sent = len(sentence.split())
        correct_rot = -1
        for rot in range(1,26):
            rotated_sentence = rotate_sentence(sentence, -rot)        
            valid_words_count = checkValidWords(rotated_sentence.split())
            if max_match < valid_words_count:
                max_match = valid_words_count
                max_match_sent = rotated_sentence
                correct_rot = rot
            if max_match == words_in_sent:
                print 'Max words matched: ', max_match
                return [rot, rotated_sentence]
        print 'Max words matched: ', max_match
        return [correct_rot, max_match_sent]

def encrypt(sentence, key):
    print 'Decrypting the message with key...'
    return [key, rotate_sentence(sentence, key)] 

def help():
    print 'Usage:'
    print '\tpython caesor.py crypt sentence key'
    print '\t\tchoice : 1 - encrypt, 2 - decrypt'
    print '\t\tsentence : sentence to encrypt/decrypt'
    print '\t\tkey (number) : key to encrypt/decrypt. If key is not given for decrypt it will try to crack it'

def validate_input(argv):
    argv_len = len(argv)
    print argv_len
    if argv_len < 2 or argv_len > 3:
        print 'Invalid number of parameters.'
        help()
        sys.exit(0)
    
def main(argv):
    validate_input(argv)
    words_in_sent = len(argv[1].split())
    print 'Given sentence: ', argv[1]
    print 'Words in Sentence: ', words_in_sent
    print 'Sentence length: ', len(argv[1]), '\n'
    choice = int(argv[0])
    final_res = []
    if choice == 1:
        if len(argv) != 3:
            print 'Key required for encryption'
            help()
            sys.exit(0)
        elif not argv[2].isdigit():
            print 'Key should be a number'
            help()
            sys.exit(0)
        final_res = encrypt(argv[1].lower(),int(argv[2])%26)
    elif choice == 2:
        if len(argv) == 3:
            if not argv[2].isdigit():
                print 'Key should be a number'
                help()
                sys.exit(0)
            final_res = decrypt(argv[1].lower(), int(argv[2])%26)
        else:
            final_res = decrypt(argv[1].lower())
    else:
        print 'Choice should be 1 or 2'
        help()
        sys.exit(0)
    if final_res == []:
        print "Someting went wrong... result is empty"
    else:
        print 'key: ', final_res[0]
        print 'Final ', 'encrypted' if choice == 1 else 'decrypted',' sentence: ',  final_res[1]

if __name__ == '__main__':
    main(sys.argv[1:])
