hard coded in kanji i know ```seen_kanji_set_tobira``` if a kanji appears outside of that set, it and the sentence it is in is added to a - eventually csv file

the result csv will contain ```kanji, jp,sentence, timestamp, episode``` columns

```util.read_all_srt_files``` and ```util.extract_episode_number``` will have to be modified to work with your srt / other files. im not using this code right now otherwise I'd probbably force some sort of naming convention on files and do some checks on srt formatting. but for now im not using this aside from the 1 show i "scraped"

subtitles had the form of "Slam Dunk.S08E05.JA.srt" as titles. i wont upload them to github...
