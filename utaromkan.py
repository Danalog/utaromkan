#!/usr/bin/env python
# encoding: utf-8

"""romkan.py - a Python rewrite of the Perl Romaji<->Kana conversion module.

Romkan Copyright (C) 2000 Satoru Takabayashi <satoru-t@is.aist-nara.ac.jp>

romkan.py Copyright (C) 2006 Eric Nichols <eric-n@is.naist.jp>
    All rights reserved.
    This is free software with ABSOLUTELY NO WARRANTY.

You can redistribute it and/or modify it under the terms of 
the GNU General Public License version 2.

Modified by Jason Moiron to work with utf-8 instead of euc-jp

Modified by Tart to be specific to UTAU
"""

__author__ = "Tart"
__author_email__ = "conemusicproductions@gmail.com"
__version__ = "0.1"
__revision__ = "1"

import re


def get_utatab():
    """get_utatab() -> string

    Reads kana<->romaji conversion table into string.

    Table is taken from KAKASI <http://kakasi.namazu.org/> and has been
    modified.

    """
    return """
あ	a	い	i	う	u	え	e	お	o 
ヴぁ　va　ヴぃ　vi　ヴ　vu　ヴぇ　ve　ヴぉ vo 

か　ka　き　ki　く　ku　け　ke　け　ko　こ
きゃ　kya　きゅ　kyu　きぇ　kye　きょ kyo
が　ga　ぎ　gi　ぐ　gu　げ　ge　ご　go
ぎゃ　gya　ぎゅ　gyu　ぎぇ　gye　ぎょ　gyo

さ　sa　すぃ　si　す　su　せ　se　そ so
すぁ　swa　すぅ　swu　すぇ　swe　すぉ　swo
ざ　za　ずぃ　zi　ず　zu　ぜ　ze　ぞ　zo

しゃ　sha　し　shi　しゅ　shu　しぇ　she　しょ　sho
じゃ　ja　じ　ji　じゅ　ju　じぇ　je　じょ　jo

た　ta　てぃ　ti　てぅ　tu　て　te　と　to
てゃ tya　てゅ　tyu　てぇ　tye　てょ　tyo
だ　da　でぃ　di　でぅ　du　で　de　ど　do
でゃ　dya　でゅ　dyu　でぇ　dye　でょ　dyo

つぁ　tsa　つぃ　tsi　つ　tsu　つぇ　tse　つぉ　tso
づぁ　dza　づぃ　dzi　づぅ　dzu　づぇ　dze　づぉ dzo

ちゃ　cha　ち　chi　ちゅ　chu　ちぇ　che　ちょ　cho
ぢゃ　dja　ぢ　dji　ぢゅ　dju　ぢぇ　dje　ぢょ　djo

な　na　に　ni　ぬ　nu　ね　ne　の
にゃ　nya　にゅ　nyu　にぇ　nye　にょ　nyo
ま　ma　み　mi　む　mu　め　me　も　mo
みゃ　mya　みゅ　myu　みぇ　mye　みょ　myo

は　ha　ひ　hi　ほぅ　hu　へ　he　ほ　ho
ひゃ　hya　ひゅ　hyu　ひぇ　hye　ひょ
ば　ba　び　bi　ぶ　bu　べ　be　ぼ　bo
びゃ　bya　びゅ　byu　びぇ　bye　びょ　byo
ぱ　pa　ぴ　pi　ぷ　pu　ぺ　pe　ぽ　po
ぴゃ　pya　ぴゅ　pyu　ぴぇ　pye　ぴょ　pyo

ふぁ　fa　ふぃ　fi　ふ　fu　ふぇ　fe　ふぉ　fo

や　ya　いぃ　yi　ゆ　yu　いぇ　ye　よ　yo

ら　ra　り　ri　る　ru　れ　re　ろ　ro
りゃ　rya　りゅ　ryu　りぇ　rye　りょ　ryo

わ	wa	ゐ	wi	うぅ　wu　ゑ	we	を	wo
うぇ　we　うぉ　wo　うぃ　wi

_　_
__　__

ぐぁ　gwa　ぐぃ　gwi　ぐぅ　gwu　ぐぇ　gwe　ぐぉ　gwo
"""


def init_rkdict(table):
    """init_rkdict(string) -> dict

    Converts string containing KAKASI romaji<->kana conversion table into
    Python dictionary indexed on kana.

    """
    rkdict = {}
    mappings = table.split()
    while (mappings):
        romaji = mappings.pop()
        kana = mappings.pop()
        rkdict[kana] = romaji
    return rkdict


# Make dictionary of kana->kunrei mappings
kunrei = init_rkdict(get_kunreitab())
# Make dictionary of kana->hepburn mappings
hepburn = init_rkdict(get_hepburntab())


def init_all():
    """init_all() -> (dict, dict, dict)

    Creates romaji->kana , kana->hepburn, and kunrei->hepburn mappings as
    Python dictionaries.

    """
    # romaji->kana
    romaji_kana = {}
    # kana->romaji
    kana_romaji = {}
    # kunrei->hepburn
    romaji_romaji = {}
    hitems = hepburn.iteritems()
    for kan, hrom in hitems:
        romaji_kana[hrom] = kan
        # kanroms[kan] = hrom
    # same as hepburn dict
    kana_romaji = hepburn
    kitems = kunrei.iteritems()
    for kan, krom in kitems:
        romaji_kana[krom] = kan
        romaji_romaji[krom] = hepburn[kan]
    return (romaji_kana, kana_romaji, romaji_romaji,)


(romkans, kanroms, romroms,) = init_all()


def init_pattern(elements):
    """init_pattern(list) -> string

    Creates pattern from list sorted by length in descending order.

    """
    items = sorted(elements, key=lambda a: len(a), reverse=True)
    pattern = '|'.join(items)
    return pattern


# pattern for matching romaji
rompat = init_pattern(romkans.keys())
# pattern for matching kana
kanpat = init_pattern(kanroms.keys())
# pattern for matching kunrei
kunpat = init_pattern(kunrei.values())
# pattern for matching hepburn
heppat = init_pattern(hepburn.values())

# consonant regex
consonants = "ckgszjtdhfpbmyrwxn"
conpat = "[%s]" % (consonants,)
conre = re.compile(r"^%s$" % (conpat,))


def isconsonant(char):
    """isconsonant(string) -> bool

    Returns true if string is a consonant.
    """
    if len(char) == 1 and char in "ckgszjtdhfpbmyrwxn":
        return True
    return False


# vowel regex
vowels = "aeiou"
vowpat = "[%s]" % (vowels,)
vowre = re.compile(r"^%s$" % (vowpat,))


def isvowel(char):
    """isvowel(string) -> bool

    Returns true if string is a vowel.
    """
    if len(char) == 1 and char in 'aeiou':
        return True
    return False


def consonant2moras(consonant):
    """consonant2moras(string) -> list

    Create list of mora starting with consonant.

    >>> list(sorted(consonant2moras('z')))
    ['za', 'ze', 'zi', 'zo', 'zu', 'zya', 'zyo', 'zyu', 'zza', 'zze', \
'zzi', 'zzo', 'zzu', 'zzya', 'zzyo', 'zzyu']

    """
    results = []
    for roma in romkans.keys():
        if re.match(consonant, roma):
            results.append(roma)
    return results


n_re = re.compile(r"n'(?=[^aiueoyn]|$)")


def normalize_double_n(word):
    """normalize_double_n(string) -> string

    Normalizes romaji string by removing excess occurances of n or
    converting them to n'.

    >>> normalize_double_n('tanni')
    "tan'i"
    >>> normalize_double_n('kannji')
    'kanji'
    >>> normalize_double_n('hannnou')
    "han'nou"
    >>> normalize_double_n('hannnya')
    "han'nya"

    """  # '
    word = word.replace("nn", "n'")
    word = n_re.sub("n", word)
    return word


# Romaji -> Romaji
hk_re = re.compile(r"(%s*?)(%s)" % (heppat, kunpat,))


def romrom(word):
    """romrom(string) -> string

    Normalizes romaji string into hepburn.

    >>> romrom('kanzi')
    'kanji'
    >>> romrom('hurigana')
    'furigana'
    >>> romrom('utukusii')
    'utsukushii'
    >>> romrom('tiezo')
    'chiezo'

    """
    # word = normalize_double_n(word)
    word = hk_re.sub(lambda m: m.groups()[0] + romroms[m.groups()[1]], word)
    return word


# EUC-JP kana codes
CHAR = "(?:[\x00-\x7f]|(?:\x8f[\xa1-\xfe]|[\x8e\xa1-\xfe])[\xa1-\xfe])"
# UTF-8 kana codes (i kept ascii because i'm not sure why it's there)
CHAR = "(?:[\x00-\x7f]|(?:\xe3\x82[\x81-\xbf])|(?:\xe3\x83[\x80-\xbc]))"

# Romaji -> Kana
cr_re = re.compile(r"(%s*?)(%s)" % (CHAR, rompat,))


def romkan(word):
    """romkan(string) -> string

    Converts romaji sequence into hiragana. Can handle both Hepburn and
    Kunrei formats.

    """
    # word = normalize_double_n(word)
    word = cr_re.sub(lambda m: m.groups()[0] + romkans[m.groups()[1]], word)
    return word


# Kana -> Romaji
ck_re = re.compile(r"(%s*?)(%s)" % (CHAR, kanpat,))


def kanrom(word):
    """kanrom(string) -> string

    Converts hiragana string into Hepburn romaji string.

    """
    # word = normalize_double_n(word)
    word = ck_re.sub(lambda m: m.groups()[0] + kanroms[m.groups()[1]], word)
    word = n_re.sub("n", word)
    # small katakana letters don't get the 'x' taken out when they are
    # 'improperly' used to lengthen vowel sounds (ex. カ-ビィ -> ka-bii)
    word = word.replace('x', '')
    return word


def unistr(word):
    try:
        uw = word.decode('utf-8')
    except UnicodeEncodeError:
        uw = unicode(word)
    return uw


# Hiragana -> Katakana
def hirakata(word):
    """hirakata(string) -> string

    Converts hiragana string into katakana.

    """
    s = u''
    uniword = unistr(word)
    for char in uniword:
        if ord(char) > 0x3040 and ord(char) < 0x3097:
            s += unichr(ord(char) + 0x60)
        else:
            s += char
    return s.encode('utf-8')


# Katakana -> Hiragana
def katahira(word):
    """katahira(string) -> string

    Converts katakana string into hiragana.

    """
    s = u''
    uniword = unistr(word)
    for char in uniword:
        if ord(char) > 0x30A0 and ord(char) < 0x30F7:
            s += unichr(ord(char) - 0x60)
        else:
            s += char
    return s.encode('utf-8')


def defullw(word):
    """defullw(string) -> string

    Converts Fullwidth unicode characters to ascii equivalents.
    """
    s = u''
    uniword = unistr(word)
    for char in uniword:
        if ord(char) >= 0xFF00 and ord(char) <= 0xff5f:
            s += unichr(ord(char) - 0xfee0)
        else:
            s += char
    return s.encode('utf-8')


def dekana(word):
    s = u''
    kana_substr = u''
    uniword = unistr(word)
    i = 0
    while i < len(uniword):
        char = uniword[i]
        if ord(uniword[i]) > 0x3040 and ord(uniword[i]) < 0x30F7:
            while i < len(uniword) and ord(uniword[i]) > 0x3040 and ord(uniword[i]) < 0x30F7:
                kana_substr += uniword[i]
                i += 1
            kana_substr = katahira(kana_substr)
            s += kanrom(kana_substr)
            kana_substr = u''
        else:
            s += char
            i += 1
    return s.encode('utf-8')
