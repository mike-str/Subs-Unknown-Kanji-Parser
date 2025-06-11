import re
from pathlib import Path
from fugashi import Tagger
from typing import List, Tuple

hiragana_full = r'[ぁ-ゟ]'
katakana_full = r'[゠-ヿ]'
kanji = r'[㐀-䶵一-鿋豈-頻]'
radicals = r'[⺀-⿕]'
katakana_half_width = r'[｟-ﾟ]'
alphanum_full = r'[！-～]'
symbols_punct = r'[、-〿]'
misc_symbols = r'[ㇰ-ㇿ㈠-㉃㊀-㋾㌀-㍿]'
ascii_char = r'[ -~]'

def extract_unicode_block(unicode_block, s):
    # https://stackoverflow.com/questions/33338713/filtering-out-all-non-kanji-characters-in-a-text-with-python-3
    return re.findall(unicode_block, s)

def extract_kanji_block(s):
    return re.findall(r'[㐀-䶵一-鿋豈-頻]', s)

def extract_episode_number(file_path):
    match = re.search(r'S(\d+)E(\d+)', file_path.stem, re.IGNORECASE)
    if match:
        season = int(match.group(1))
        episode = int(match.group(2))
        return season * 100 + episode  # ensures proper order: S01E09 < S02E01
    return -1


def read_all_srt_files(directory):
    # TODO this will break with different file naming conventions. Files this works on are:
    # Naruto (168).srt

    file_names = []

    srt_texts = []
    dir_path = Path(directory)
    files = list(dir_path.glob("*.srt"))
    
    # Sort by episode number extracted from parentheses
    files.sort(key=extract_episode_number)

    for srt_file in files:
        file_names.append(srt_file.name)
        with srt_file.open(encoding='utf-8') as f:
            srt_texts.append(f.read())

    return file_names, srt_texts


def extract_words_from_srt(srt_path: Path) -> List[Tuple[str, str]]:
    """
    Extract unique words from a .srt file along with their sentence and timestamp.

    Returns:
        A list of tuples (lemma, sentence, timestamp)
    """
    tagger = Tagger()
    seen = set()
    results = []

    srt_path = Path(srt_path) 

    with srt_path.open(encoding="utf-8") as f:
        lines = f.read().splitlines()

    i = 0
    while i < len(lines):
        if not lines[i].strip().isdigit():
            i += 1
            continue

        i += 1  # timestamp line
        timestamp = lines[i].strip() if i < len(lines) else ""
        i += 1

        subtitle_lines = []
        while i < len(lines) and lines[i].strip():
            subtitle_lines.append(lines[i].strip())
            i += 1

        sentence = " ".join(subtitle_lines)
        sentence = re.sub(r'^（[^（）\n]*?(（.*?）)?[^（）\n]*?）', '', sentence).strip()

        for tok in tagger(sentence):
            lemma = (tok.feature.orthBase
                     if hasattr(tok.feature, "orthBase")
                     else tok.feature.orth)

            if lemma == "*" or lemma in seen:
                continue

            seen.add(lemma)
            results.append((lemma, sentence, timestamp))

        while i < len(lines) and not lines[i].strip():
            i += 1

    return results