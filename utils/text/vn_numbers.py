import re

class NumToVnStr:
    def __init__(self, doc_so_rong=True):
        self.chu_so= ('không', 'một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín', 'mười')
        self.muoi = 'mươi'
        self.tram = 'trăm'
        self.nghin = 'nghìn'
        self.trieu = 'triệu'
        self.ty = 'tỷ'
        self.mot = 'mốt'
        self.tu = 'tư'
        self.lam = 'lăm'
        self.linh = 'linh'
        self.doc_so_rong = doc_so_rong


    def to_vn_str(self, s):
        return self._arbitrary(s.lstrip('0'))


    def _int(self, c):
        return ord(c) - ord('0') if c else 0


    def _LT1e2(self, s):
        if len(s) <= 1: return self.chu_so[self._int(s)]
        if s[0] == '1':
            ret = self.chu_so[10]
        else:
            ret = self.chu_so[self._int(s[0])]
            if self.muoi: ret += ' ' + self.muoi
            elif s[1] == '0': ret += ' mươi'
        if s[1] != '0':
            ret += ' '
            if   s[1] == '1' and s[0] != '1': ret += self.mot
            elif s[1] == '4' and s[0] != '1': ret += self.tu
            elif s[1] == '5': ret += self.lam
            else: ret += self.chu_so[self._int(s[1])]
        return ret


    def _LT1e3(self, s):
        if len(s) <= 2: return self._LT1e2(s)
        if s == '000': return ''
        ret = self.chu_so[self._int(s[0])] + ' ' + self.tram
        if s[1] != '0':
            ret += ' ' + self._LT1e2(s[1:])
        elif s[2] != '0':
            ret += ' ' + self.linh + ' ' + self.chu_so[self._int(s[2])]
        return ret


    def _LT1e9(self, s):
        if len(s) <= 3: return self._LT1e3(s)
        if s == '000000' or s == '000000000': return ''
        mid = len(s) % 3 if len(s) % 3 else 3
        left, right = self._LT1e3(s[:mid]), self._LT1e9(s[mid:])
        hang = self.nghin if len(s) <= 6 else self.trieu
        if not left:
            if not self.doc_so_rong: return right
            else: return self.chu_so[0] + ' ' + hang + ' ' + right
        if not right: return left + ' ' + hang
        return left + ' ' + hang + ' ' + right
        

    def _arbitrary(self, s):
        if len(s) <= 9: return self._LT1e9(s)
        mid = len(s) % 9 if len(s) % 9 else 9
        left, right = self._LT1e9(s[:mid]), self._arbitrary(s[mid:])
        hang = ' '.join([self.ty] * ((len(s) - mid) // 9))
        if not left:
            if not self.doc_so_rong: return right
            elif right: return self.chu_so[0] + ' ' + hang + ', ' + right
            else: return right
        if not right: return left + ' ' + hang
        return left + ' ' + hang + ', ' + right


default_converter = NumToVnStr()

def _vn_convert_numbers(s):
    a = []    
    for i in s.split():
        if i.isdigit():
            i = default_converter.to_vn_str(i)
        a.append(i)
    a = ' '.join(a)
    return a

def vn_convert_numbers(s):
    _s = s
    
#     thousands = re.findall(r'\d+.\d+', _s)
#     for th in thousands:
#         _s = _s.replace('.', '')
    
#     decimals = 
    
    numbers = re.findall(r'\d+', _s)
    for n in numbers:
        _s = _s.replace(n, default_converter.to_vn_str(n), 1)
    return _s
    


if __name__ == '__main__':
    test_cases_1 = (
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
        "10", "11", "12", "20", "21", "22", "24", "90", "91", "97",
        "300", "999", "121", "215", "5121", "39500",
        "1025217", "51105500", "51000000", "999999999",
        "5120625952200", "12000000000000000000", "18446744073709551615",
        "18000000000709551615", "11000000000",
        "1000015", "1002015", "1000000024",
        "03215", "", "0000", "00001", "00100",
        "1844674407370955161518000000000000000000709551615",
        "0321", "000345", "15", "40430203", "3209", "3500", "3901", "21",
        "3005", "3055", "9031", "9330",
        "9000005", "9001005",
    )
    test_cases_2 = (
        ("32000000", "ba mươi hai triệu"),
        ("32516000", "ba mươi hai triệu năm trăm mười sáu nghìn"),
        ("32516497", "ba mươi hai triệu năm trăm mười sáu nghìn bốn trăm chín mươi bảy"),
        ("834291712", "tám trăm ba mươi tư triệu hai trăm chín mươi mốt nghìn bảy trăm mười hai"),
        ("308250705", "ba trăm linh tám triệu hai trăm năm mươi nghìn bảy trăm linh năm"),
        ("500209037", "năm trăm triệu hai trăm linh chín nghìn không trăm ba mươi bảy"),
        ("7312836", "bảy triệu ba trăm mười hai nghìn tám trăm ba mươi sáu"),
        ("57602511", "năm mươi bảy triệu sáu trăm linh hai nghìn năm trăm mười một"),
        ("351600307", "ba trăm năm mươi mốt triệu sáu trăm nghìn ba trăm linh bảy"),
        ("900370200", "chín trăm triệu ba trăm bảy mươi nghìn hai trăm"),
        ("400070192", "bốn trăm triệu không trăm bảy mươi nghìn một trăm chín mươi hai"),
        ("10250214", "mười triệu hai trăm năm mươi nghìn hai trăm mười bốn"),
        ("253564888", "hai trăm năm mươi ba triệu năm trăm sáu mươi tư nghìn tám trăm tám mươi tám"),
        ("400036105", "bốn trăm triệu không trăm ba mươi sáu nghìn một trăm linh năm"),
        ("700000231", "bảy trăm triệu không nghìn hai trăm ba mươi mốt"),
    )

    custom_converter = NumToVnStr(đọc_số_rỗng=True, linh='lẻ', tư='bốn', nghìn='ngàn', mươi=False, tỷ='tỉ', lăm='nhăm')
    for i in test_cases_1:
        print('{} = {}'.format(i, custom_converter.to_vn_str(i)))
    default_converter = NumToVnStr()
    for test_case in test_cases_2:
        i, o = test_case
        assert default_converter.to_vn_str(i) == o
        print('\n{}\n{}\n{}'.format(i, default_converter.to_vn_str(i), o))