library(tidyverse)
library(mgcv)
library(geomtextpath)
#library(itsadug)

setwd("/home/roger/Documents/RA/oops_lab-speech_rate/prelim_analysis/")

`%ni%` <- Negate(`%in%`)

# apah <- read_csv(
#   "../doreco_data/doreco_apah1238_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Yali") %>%
#   arrange(speaker, discourse, phone_start)

# arap <- read_csv(
#   "../doreco_data/doreco_arap1274_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Arapaho") %>%
#   arrange(speaker, discourse, phone_start)

# bain <- read_csv(
#   "../doreco_data/doreco_bain1259_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Gubeeher") %>%
#   arrange(speaker, discourse, phone_start)

# beja <- read_csv(
#   "../doreco_data/doreco_beja1238_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Beja") %>%
#   arrange(speaker, discourse, phone_start)

# bora <- read_csv(
#   "../doreco_data/doreco_bora1263_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Bora") %>%
#   arrange(speaker, discourse, phone_start)

# dolg <- read_csv(
#   "../doreco_data/doreco_dolg1241_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Dolgan") %>%
#   arrange(speaker, discourse, phone_start)

# even <- read_csv(
#   "../doreco_data/doreco_even1259_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Evenki") %>%
#   arrange(speaker, discourse, phone_start)

# guri <- read_csv(
#   "../doreco_data/doreco_guri1247_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Gurindji") %>%
#   arrange(speaker, discourse, phone_start)

# jeju <- read_csv(
#   "../doreco_data/doreco_jeju1234_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Jejuan") %>%
#   arrange(speaker, discourse, phone_start)

# kama <- read_csv(
#   "../doreco_data/doreco_kama1351_durations.csv",
#   col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
# ) %>%
#   mutate(language="Kamas") %>%
#   arrange(speaker, discourse, phone_start)

# lowe <- read_csv("../doreco_data/doreco_lowe1385_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Lower_Sorbian") %>%
#   arrange(speaker, discourse, phone_start)

# movi <- read_csv("../doreco_data/doreco_movi1243_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Movima") %>%
#   arrange(speaker, discourse, phone_start)

# ngal <- read_csv("../doreco_data/doreco_ngal1292_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Dalabon") %>%
#   arrange(speaker, discourse, phone_start)

# nngg <- read_csv("../doreco_data/doreco_nngg1234_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Nuu") %>%
#   arrange(speaker, discourse, phone_start)

# orko <- read_csv("../doreco_data/doreco_orko1234_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Fanbyak") %>%
#   arrange(speaker, discourse, phone_start)

# resi <- read_csv("../doreco_data/doreco_resi1247_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Resigaro") %>%
#   arrange(speaker, discourse, phone_start)

# ruul <- read_csv("../doreco_data/doreco_ruul1235_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Ruuli") %>%
#   arrange(speaker, discourse, phone_start)

# sadu <- read_csv("../doreco_data/doreco_sadu1234_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Sadu") %>%
#   arrange(speaker, discourse, phone_start)

# sanz <- read_csv("../doreco_data/doreco_sanz1248_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Sanzhi_Dargwa") %>%
#   arrange(speaker, discourse, phone_start)

# sout <- read_csv("../doreco_data/doreco_sout3282_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="English") %>%
#   arrange(speaker, discourse, phone_start)

# svan <- read_csv("../doreco_data/doreco_svan1243_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Svan") %>%
#   arrange(speaker, discourse, phone_start)

# trin <- read_csv("../doreco_data/doreco_trin1278_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Mojeno_Trinitario") %>%
#   arrange(speaker, discourse, phone_start)

# urum <- read_csv("../doreco_data/doreco_urum1249_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Urum") %>%
#   arrange(speaker, discourse, phone_start)

# vera <- read_csv("../doreco_data/doreco_vera1241_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Veraa") %>%
#   arrange(speaker, discourse, phone_start)

# yong <- read_csv("../doreco_data/doreco_yong1270_durations.csv",
#                  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
#   mutate(language="Yongning_Na") %>%
#   arrange(speaker, discourse, phone_start)

# df.drc <- bind_rows(
#   apah,
#   arap,
#   bain,
#   beja,
#   bora,
#   dolg,
#   even,
#   guri,
#   jeju,
#   kama,
#   lowe,
#   movi,
#   ngal,
#   nngg,
#   orko,
#   resi,
#   ruul,
#   sadu,
#   sanz,
#   sout,
#   svan,
#   trin,
#   urum,
#   vera,
#   yong
# )

df.drc <- read_csv("../data/DoReCo.csv")
saveRDS(df.drc, "../data/DoReCo.rds")
df.mapping <- read_csv("../data/phone_mapping.csv")

df.raw <- df.drc %>%
  left_join(x = ., y = df.mapping, by = c("language" = "lang", "phone" = "phone", "phone_ipa" = "phone_ipa"))

df.raw.drc <- df.raw %>%
  filter(language %in% c(
    "Yali", "Gubeeher", "Beja", "Bora", "Evenki",
    "Movima", "Nuu", "Sanzhi_Dargwa", "Svan", "Mojeno_Trinitario"
  )) %>%
  select(
    speaker, uttr_id, num_words_uttr, num_sylls_uttr, uttr_start, uttr_end, uttr_dur,
    word, num_phones_word, num_sylls_word, word_start, word_end, word_dur,
    phone_ipa, previous_phone, following_phone, segtype,
    phone_start, phone_end, phone_dur, language, c_type
  ) %>%
  rename(
    num_syllables_uttr = "num_sylls_uttr",
    num_syllables_word = "num_sylls_word",
    phone = "phone_ipa", previous = "previous_phone",
    following = "following_phone", segment_type = "segtype"
  )

twm <- read_csv("../data/taiwanese_mandarin_durations.csv") %>%
  arrange(speaker, file, phone_start) %>%
  filter(speaker != "mn_tw_66") %>%
  select(-sex, -age) %>%
  mutate(language="Taiwan Mandarin",
         folder="taiwanese_mandarin")

k <- read_csv("../data/korean_durations.csv") %>%
  arrange(speaker, file, phone_start) %>%
  select(-sex, -age) %>%
  mutate(language="Seoul Korean",
         folder="korean")

p <- read_csv("../data/kapampangan_durations.csv") %>%
  arrange(speaker, file, phone_start) %>%
  select(-sex, -age) %>%
  mutate(language="Kapampangan",
         folder="kapampangan")

v <- read_csv("../data/vietnamese_durations.csv") %>%
  arrange(speaker, file, phone_start) %>%
  #select(-sex, -age) %>%
  mutate(language="Vietnamese",
         speaker=as.character(speaker),
         folder="vietnamese")

s <- read_csv("../data/swahili_durations.csv") %>%
  arrange(speaker, file, phone_start) %>%
  #select(-sex, -age) %>%
  mutate(language="Swahili",
         speaker=as.character(speaker),
         folder="swahili")

tu <- read_csv("../data/turkish_durations.csv") %>%
  arrange(speaker, file, phone_start) %>%
  #select(-sex, -age) %>%
  mutate(language="Turkish",
         speaker=as.character(speaker),
         folder="turkish")

a <- read_csv("../data/amharic_durations.csv") %>%
  arrange(speaker, file, phone_start) %>%
  #select(-sex, -age) %>%
  mutate(language="Amharic",
         speaker=as.character(speaker),
         folder="amharic")

g <- read_csv("../data/georgian_durations.csv") %>%
  arrange(speaker, file, phone_start) %>%
  #select(-sex, -age) %>%
  mutate(language="Georgian",
         speaker=as.character(speaker),
         folder="georgian")

b <- readRDS("../data/buckeye_durations.rds") %>%
  arrange(speaker, file, phone_start) %>%
  mutate(language="American English",
         segment_type=case_when(
           phone %in% c("{E_TRANS}", "{B_TRANS}", "id", "no", "hhn", "an") ~ "non-speech",
           phone %in% c("a", "e", "ih l", "ah r", "i", "ah l", "ah ix", "uw ix", "ah n") ~ "vowel",
           TRUE ~ segment_type
         )
  )

d <- bind_rows(twm, k, p, b, v, s, tu, a, g) %>%
  select(
    speaker, uttr_id, num_words_uttr, num_syllables_uttr, uttr_start, uttr_end, uttr_dur,
    word, num_phones_word, num_syllables_word, word_start, word_end, word_dur,
    phone, previous, following, segment_type,
    phone_start, phone_end, phone_dur, language
  )

d <- d %>%
  mutate(
    c_type = case_when(
      ## Taiwan Mandarin
      language == "Taiwan Mandarin" & 
        phone %in% c("p", "b", "t", "d", "k", "g") ~ "stop",
      language == "Taiwan Mandarin" & 
        phone %in% c("f", "sh", "s", "x", "h") ~ "fricative",
      language == "Taiwan Mandarin" & 
        phone %in% c("j", "q", "zh", "ch", "z", "c") ~ "affricate",
      language == "Taiwan Mandarin" & 
        phone %in% c("m", "n", "ng") ~ "nasal",
      language == "Taiwan Mandarin" & 
        phone %in% c("y", "w", "ue") ~ "approximant",
      language == "Taiwan Mandarin" & 
        phone %in% c("l", "r") ~ "liquid",
      language == "Taiwan Mandarin" & 
        phone %in% c("i", "ii", "v", "u") ~ "high monophthong",
      language == "Taiwan Mandarin" & 
        phone %in% c("a", "e", "o") ~ "non-high monophthong",
      language == "Taiwan Mandarin" & 
        phone %in% c("ai", "ao", "ei", "ou") ~ "diphthong",
      ## Korean
      language == "Seoul Korean" & 
        phone %in% c("B", "Ph", "BB", "p", "D", "Th", "DD", "t", "G", "Kh", "GG", "k") ~ "stop",
      language == "Seoul Korean" & 
        phone %in% c("S", "SS", "H") ~ "fricative",
      language == "Seoul Korean" & 
        phone %in% c("J", "CHh", "JJ") ~ "affricate",
      language == "Seoul Korean" & 
        phone %in% c("M", "N", "NG") ~ "nasal",
      language == "Seoul Korean" & 
        phone %in% c("L", "R") ~ "liquid",
      language == "Seoul Korean" & 
        phone %in% c("I","U") ~ "high monophthong",
      language == "Seoul Korean" & 
        phone %in% c("A", "E", "O") ~ "non-high monophthong",
      language == "Seoul Korean" & 
        phone %in% c("AE", "EO", "EU", "OE", "UE", "euI", "iA", "iE", "iEO", "iO", "iU", "oA", "uEO") ~ "diphthong",
      ## Kapampangan
      language == "Kapampangan" & 
        phone %in% c("b", "p", "d", "t", "ɡ", "k", "ʔ", "q", "c") ~ "stop",
      language == "Kapampangan" & 
        phone %in% c("s", "ʃ", "f", "h", "v", "x") ~ "fricative",
      language == "Kapampangan" & 
        phone %in% c("tʃ", "dʒ") ~ "affricate",
      language == "Kapampangan" & 
        phone %in% c("m", "n", "ŋ") ~ "nasal",
      language == "Kapampangan" & 
        phone %in% c("j", "w") ~ "approximant",
      language == "Kapampangan" & 
        phone %in% c("l", "r") ~ "liquid",
      language == "Kapampangan" & 
        phone %in% c("i", "ɪ", "u", "ʊ") ~ "high monophthong",
      language == "Kapampangan" & 
        phone %in% c("e", "o", "a") ~ "non-high monophthong",
      ## American English
      language == "American English" &
        phone %in% c("p", "b", "t", "d", "k", "g", "dx", "q", "tq") ~ "stop",
      language == "American English" &
        phone %in% c("m", "n", "ng", "nx") ~ "nasal",
      language == "American English" &
        phone %in% c("f", "v", "th", "dh", "s", "z", "sh", "zh", "hh", "h", "x") ~ "fricative",
      language == "American English" &
        phone %in% c("ch", "jh", "j") ~ "affricate",
      language == "American English" &
        phone %in% c("r", "l") ~ "liquid",
      language == "American English" &
        phone %in% c("w", "y") ~ "approximant",
      language == "American English" &
        phone %in% c("em", "en", "el", "eng") ~ "syllabic C",
      language == "American English" & 
        phone %in% c("i", "ih", "ih l", "ihn", "iy", "uw", "uw ix", "ihn", "uh", "uhn", "iyn", "uwn") ~ "high monophthong",
      language == "American English" & 
        phone %in% c(
          "a", "aa", "aan", "ae", "aen", "ah", "ah ix", "ah l", "ah n", "ah r", "ahn", "an", "ao", "aon",
          "e", "eh", "ehn", "er", "ern"
        ) ~ "non-high monophthong",
      language == "American English" & 
        phone %in% c("ay", "ayn", "aw", "awn", "oy", "oyn", "ow", "own", "ey", "eyn") ~ "diphthong",
      ## Vietnamese
      language == "Vietnamese" &
        phone %in% c("p", "t", "c", "k", "tʰ", "ɓ", "ɗ", "ʔ") ~ "stop",
      language == "Vietnamese" &
        phone %in% c("m", "n", "ɲ", "ŋ") ~ "nasal",
      language == "Vietnamese" &
        phone %in% c("f", "v", "s", "z", "x", "ɣ", "h") ~ "fricative",
      language == "Vietnamese" &
        phone %in% c("tɕ") ~ "affricate",
      language == "Vietnamese" &
        phone %in% c("l") ~ "liquid",
      language == "Vietnamese" &
        phone %in% c("w", "j") ~ "approximant",
      language == "Vietnamese" & 
        phone %in% (unique(filter(v, segment_type == "vowel")$phone) %>% str_subset("^.ə")) ~ "diphthong",
      language == "Vietnamese" & 
        phone %in% (unique(filter(v, segment_type == "vowel")$phone) %>% str_subset("^[iɨu][^ə]")) ~ "high monophthong",
      language == "Vietnamese" & 
        phone %in% (unique(filter(v, segment_type == "vowel")$phone) %>% str_subset("^[^iɨu][^ə]")) ~ "non-high monophthong",
      ## Swahili
      language == "Swahili" &
        phone %in% c('b', 'd', 'k', 'p', 't', 'ɓ', 'ɗ', 'ɠ', 'ɡ', 'ʄ') ~ "stop",
      language == "Swahili" &
        phone %in% c('m', 'n', 'ŋ', 'ɱ', 'ɲ') ~ "nasal",
      language == "Swahili" &
        phone %in% c('f', 'h', 's', 'v', 'z', 'ð', 'ɣ', 'ʃ', 'θ') ~ "fricative",
      language == "Swahili" &
        phone %in% c('dʒ', 'tʃ') ~ "affricate",
      language == "Swahili" &
        phone %in% c("l", "ɾ") ~ "liquid",
      language == "Swahili" &
        phone %in% c("w", "j") ~ "approximant",
      language == "Swahili" & 
        phone %in% c("i","u","iː","uː") ~ "high monophthong",
      language == "Swahili" & 
        phone %in% c("ɑ","ɑː", "ɔ", "ɔː", "ɛ", "ɛː") ~ "non-high monophthong",
      ## Turkish
      language == "Turkish" &
        phone %in% c('b', 'bː', 'c', 'cː', 'd̪', 'd̪ː','k', 'kː', 'p','t̪', 't̪ː', 'ɟ', 'ɡ') ~ "stop",
      language == "Turkish" &
        phone %in% c('m', 'mː', 'n̪', 'n̪ː','ŋ') ~ "nasal",
      language == "Turkish" &
        phone %in% c('f', 'h', 'hː', 's̪', 's̪ː','v', 'z̪','ç','ʃ','ʒ') ~ "fricative",
      language == "Turkish" &
        phone %in% c('dʒ', 'tʃ') ~ "affricate",
      language == "Turkish" &
        phone %in% c('ɾ','ɫ', 'ɫː', 'ʎ', 'ʎː') ~ "liquid",
      language == "Turkish" &
        phone %in% c("j") ~ "approximant",
      language == "Turkish" & 
        phone %in% c("i","ɯ","u","y","iː","ɯː","uː","yː","ɨ","ʏ", "ɪ", "ʊ") ~ "high monophthong",
      language == "Turkish" & 
        phone %in% c("a", "aː", "e", "eː", "o", "oː", "ø", "øː", "ɛ") ~ "non-high monophthong",
      ## Georgian
      language == "Georgian" &
        phone %in% c('b', 'd', 'kʰ', 'kʼ', 'pʰ', 'pʼ', 'qʼ', 'tʰ', 'tʼ', 'ɡ') ~ "stop",
      language == "Georgian" &
        phone %in% c('m', 'n') ~ "nasal",
      language == "Georgian" &
        phone %in% c('h', 's', 'v', 'x', 'z', 'ɣ', 'ʃ', 'ʒ') ~ "fricative",
      language == "Georgian" &
        phone %in% c('dz', 'dʒ', 'ts', 'tsʼ', 'tʃ', 'tʃʼ') ~ "affricate",
      language == "Georgian" &
        phone %in% c('ɾ', 'l') ~ "liquid",
      language == "Georgian" &
        phone %in% c("i", 'u') ~ "high monophthong",
      language == "Georgian" &
        phone %in% c("ɑ", "ɔ", "ɛ") ~ "non-high monophthong",
      ## Amharic
      language == "Amharic" &
        phone %in% c('p', 'pʷ', 'pʼ', 'pʷʼ', 'b', 'pʷ', 't', 'tʷ', 'tʼ', 'tʷʼ', 'd', 'dʷ', 'k', 'kʷ', 'kʼ', 'kʷʼ', 'ɡ', 'ɡʷ', 'ʔ') ~ "stop",
      language == "Amharic" &
        phone %in% c('m', 'mʷ', 'n', 'nʷ', 'ɲ', 'ɲʷ') ~ "nasal",
      language == "Amharic" &
        phone %in% c('v', 'vʷ', 'f', 'fʷ', 's', 'sʷ', 'sʼ', 'sʷʼ', 'z', 'zʷ', 'ʃ', 'ʃʷ', 'ʒ', 'ʒʷ', 'h', 'hʷ') ~ "fricative",
      language == "Amharic" &
        phone %in% c('t͡ʃ', 't͡ʃʷ', 't͡ʃʼ', 't͡ʃʷʼ', 'd͡ʒ', 'd͡ʒʷ') ~ "affricate",
      language == "Amharic" &
        phone %in% c('r', 'rʷ', 'l', 'lʷ') ~ "liquid",
      language == "Amharic" &
        phone %in% c('w', 'j') ~ "approximant",
      language == "Amharic" &
        phone %in% c('i', 'u', "ɨ") ~ "high monophthong",
      language == "Amharic" &
        phone %in% c("a", "e", "o", "ə") ~ "non-high monophthong"
      #segment_type == "vowel" &  ~ "vowel"
    ),
    c_type = ifelse(is.na(c_type), NA, c_type),
    c_type = ifelse(segment_type == "vowel" & c_type %ni% c("high monophthong", "diphthong"),  "non-high monophthong", c_type)
  )
  
df <- bind_rows(d, df.raw.drc)
d_seg <- df %>%
  filter(segment_type %in% c("consonant", "vowel", "syllabic"),
         phone_dur > 0,
         c_type != "syllabic C") %>%
  group_by(
    language,
    speaker,
    uttr_id
  ) %>%
  mutate(
    # duration of segmental material only
    uttr_dur = sum(phone_dur),
    num_syllables_uttr = sum(segment_type == "vowel" | segment_type == "syllabic" | c_type == "syllabic C"),
    num_segments_uttr = n(),
    segment_dur_uttr = uttr_dur / num_segments_uttr,
    syllable_dur_uttr = uttr_dur / num_syllables_uttr,
    segment_type = recode(segment_type, syllabic = "vowel")
  ) %>%
  ungroup()

d_seg <- d_seg %>%
  filter(num_syllables_uttr > 5) %>%
  filter(segment_dur_uttr < 0.25) %>%  # we only keep utterances where avg seg dur > 0.04 and < 0.25
  filter(segment_dur_uttr > 0.04) %>%
  group_by(language) %>%
  filter(
    log(segment_dur_uttr) > 
      mean(log(segment_dur_uttr)) - 
      3*sd(log(segment_dur_uttr)),
    log(segment_dur_uttr) < 
      mean(log(segment_dur_uttr)) +
      3*sd(log(segment_dur_uttr))
  ) %>%
  ungroup() %>%
  filter(phone_dur > 0.03,  #raw phone duration
         phone_dur < 0.4)

d_seg <- d_seg %>%
  group_by(language, speaker, uttr_id) %>%
  mutate(
    uttr_dur = sum(phone_dur),
    num_segments_uttr = n(),
    segment_dur_uttr = uttr_dur / num_segments_uttr
  ) %>%
  ungroup() %>%
  filter(num_segments_uttr >= 10)

d_uttr <- d_seg %>%
  filter(segment_type %in% c("consonant", "vowel", "syllabic"), phone_dur > 0) %>%
  group_by(language, speaker, uttr_id) %>%
  summarise(
    # duration of segmental material only
    uttr_dur = sum(phone_dur),
    num_syllables_uttr = sum(segment_type == "vowel" | segment_type == "syllabic" | c_type == "syllabic C"),
    num_segments_uttr = n(),
    segment_dur_uttr = uttr_dur / num_segments_uttr,
    syllable_dur_uttr = uttr_dur / num_syllables_uttr,
    vowel_dur_uttr = mean(phone_dur[segment_type %in% c("vowel", "syllabic")]),
    cons_dur_uttr = mean(phone_dur[segment_type == "consonant"]),
    nh_v_dur = mean(phone_dur[c_type == "non-high monophthong"]),
    h_v_dur = mean(phone_dur[c_type == "high monophthong"]),
    di_v_dur = mean(phone_dur[c_type == "diphthong"]),,
    stop_dur = mean(phone_dur[c_type == "stop"]),
    fricative_dur = mean(phone_dur[c_type == "fricative"]),
    affricate_dur = mean(phone_dur[c_type == "affricate"]),
    nasal_dur = mean(phone_dur[c_type == "nasal"]),
    approximant_dur = mean(phone_dur[c_type == "approximant"]),
    liquid_dur = mean(phone_dur[c_type == "liquid"]),
    click_dur = mean(phone_dur[c_type == "click"]),
    syllabic_c_dur = mean(phone_dur[c_type == "syllabic C"]),
    perc_v = 100 * sum(phone_dur[segment_type == "vowel"]) / uttr_dur
  ) %>%
  ungroup()

d_seg$segment_type_o <- as.ordered(d_seg$segment_type)
contrasts(d_seg$segment_type_o) <- "contr.treatment"

d_seg$speaker_f <- as.factor(d_seg$speaker)
d_seg$speakerSegtype <- interaction(d_seg$speaker, d_seg$segment_type)

d_seg$language_f <- as.factor(d_seg$language)
d_seg$languageSegtype <- interaction(d_seg$language, d_seg$segment_type)

d_seg$log_segment_dur_uttr <- log(d_seg$segment_dur_uttr)
d_seg$log_dur <- log(d_seg$phone_dur)

d_seg$c_type_f <- as.factor(d_seg$c_type)

# model 1: no control for quality
cv_mod_baseline <- bam(phone_dur ~
                         segment_type_o +
                         s(segment_dur_uttr, bs = "cr") +
                         s(segment_dur_uttr, by = segment_type_o, bs = "cr") +
                         #s(segment_dur_uttr, c_type_f, bs = "fs", m = 1, xt = list("cr")) +
                         s(segment_dur_uttr, speakerSegtype, bs = "fs", m = 1, xt = list("cr")) +
                         s(segment_dur_uttr, languageSegtype, bs = "fs", m = 1, xt = list("cr")),
                       data = d_seg,
                       #weights=d_seg$weight / mean(d_seg$weight),
                       discrete = TRUE,
                       nthreads = 8
)
saveRDS(cv_mod_baseline, "../model/cv_mod_baseline.rds")
baseline <- readRDS("../model/cv_mod_baseline.rds")
summary(cv_mod_baseline)

cv_mod_type <- bam(phone_dur ~
  segment_type_o +
  s(segment_dur_uttr, bs = "cr") +
  s(segment_dur_uttr, by = segment_type_o, bs = "cr") +
  s(segment_dur_uttr, c_type_f, bs = "fs", m = 1, xt = list("cr")) +
  s(segment_dur_uttr, speakerSegtype, bs = "fs", m = 1, xt = list("cr")) +
  s(segment_dur_uttr, languageSegtype, bs = "fs", m = 1, xt = list("cr")),
  data = d_seg,
  discrete = TRUE,
  nthreads = 8
)
saveRDS(cv_mod_type, "../model/cv_mod_type.rds")
type <- readRDS("../model/cv_mod_type.rds")
summary(cv_mod_type)


d_uttr_plot <- d_seg %>%
  group_by(language, speaker, uttr_id) %>%
  summarise(
    # duration of segmental material only
    uttr_dur = sum(phone_dur),
    num_syllables_uttr = sum(segment_type == "vowel" | segment_type == "syllabic" | c_type == "syllabic C"),
    num_segments_uttr = n(),
    segment_dur_uttr = uttr_dur / num_segments_uttr,
    syllable_dur_uttr = uttr_dur / num_syllables_uttr,
    vowel_dur_uttr = mean(phone_dur[segment_type %in% c("vowel", "syllabic")]),
    cons_dur_uttr = mean(phone_dur[segment_type == "consonant"]),
  ) %>%
  ungroup() %>%
  pivot_longer(c(vowel_dur_uttr, cons_dur_uttr),
               names_to="measure",
               values_to="value")


newdat_cv <- expand.grid(
  segment_dur_uttr = seq(
    min(d_seg$segment_dur_uttr),
    max(d_seg$segment_dur_uttr),
    length.out = 100
  ),
  c_type_f = d_seg$c_type_f[1],
  speakerSegtype = d_seg$speakerSegtype[1],
  languageSegtype = d_seg$languageSegtype[1],
  segment_type_o = unique(d_seg$segment_type_o)
)

newdat_cv$segment_type_o <- as.ordered(newdat_cv$segment_type_o)
contrasts(newdat_cv$segment_type_o) <- "contr.treatment"

preds_full <- predict(cv_mod_type, newdat_cv,
  exclude = c(
    "s(segment_dur_uttr,c_type_f)",
    "s(segment_dur_uttr,speakerSegtype)",
    "s(segment_dur_uttr,languageSegtype)"
  ),
  se.fit = TRUE
)

newdat_cv$dur <- preds_full$fit
newdat_cv$ul <- preds_full$fit + preds_full$se.fit * 1.96
newdat_cv$ll <- preds_full$fit - preds_full$se.fit * 1.96

p <- newdat_cv %>%
  ggplot(aes(x = segment_dur_uttr, y = dur, color = segment_type_o)) +
    geom_ribbon(aes(ymin = ll, ymax = ul, group = segment_type_o), color = NA, fill = "grey", alpha = 0.25) +
    geom_textline(aes(label = segment_type_o), size = 10, linewidth = 2.5, hjust = 0.75) +
    scale_x_log10(breaks = c(0.05, 0.07, 0.1, 0.14), labels = c(".05", ".07", ".10", ".14")) +
    scale_y_log10(breaks = c(0.03, 0.04, 0.05, 0.07, 0.1, 0.14), labels = c(".03", ".04", ".05", ".07", ".10", ".14")) +
    scale_color_manual(values=c("#56B4E9", "#e69f00"), guide="none") +
    xlab("Average segment dur. in s (inverse speech rate)") +
    ylab("Average duration in s") +
    theme(
      panel.grid.major = element_blank(),
      panel.grid.minor = element_blank(),
      plot.background = element_rect(fill = "transparent", color = NA),
      panel.background = element_rect(fill = "transparent", color = NA),
      legend.position = "none"
    )
p
ggsave(filename = "./graphs/pop_lang_talk.png", plot = p, width = 9.42, height = 9)

# origin
# model predictions
newdat_cv <- expand.grid(
  segment_dur_uttr = seq(
    min(d_seg$segment_dur_uttr),
    max(d_seg$segment_dur_uttr),
    length.out = 100
  ),
  c_type_f = d_seg$c_type_f[1],
  speakerSegtype = d_seg$speakerSegtype[1],
  #language_f=unique(d_uttr_cv$language_f),
  languageSegtype = unique(d_seg$languageSegtype)
)

newdat_cv$segment_type_o <- str_extract(newdat_cv$languageSegtype, "[^.]*$")
newdat_cv$segment_type_o <- as.ordered(newdat_cv$segment_type_o)
contrasts(newdat_cv$segment_type_o) <- "contr.treatment"

newdat_cv$language <- str_extract(newdat_cv$languageSegtype, "^[^.]*")
newdat_cv$language_f <- as.factor(newdat_cv$language)
newdat_cv$speaker_f <- as.factor(str_extract(newdat_cv$speakerSegtype, "^[^.]*"))
#newdat_cv$speaker_f <- d_uttr_cv$speaker_f[1]

preds_baseline <- predict(cv_mod_baseline, newdat_cv,
  # the following is used when predicting without speakers
  exclude=c("s(segment_dur_uttr,speakerSegtype)",
            "s(segment_dur_uttr,speaker_f)",
            "s(segment_dur_uttr,speaker_f):segment_type_ovowel_dur_uttr",
            "s(segment_dur_uttr,c_type_f)"),
  se.fit = TRUE
)

preds_full <- predict(cv_mod_type, newdat_cv,
  # the following is used when predicting without speakers
  exclude=c("s(segment_dur_uttr,speakerSegtype)",
            "s(segment_dur_uttr,speaker_f)",
            "s(segment_dur_uttr,speaker_f):segment_type_ovowel_dur_uttr",
            "s(segment_dur_uttr,c_type_f)"),
  se.fit = TRUE
)

# baseline

newdat_cv_baseline <- newdat_cv

newdat_cv_baseline$dur <- preds_baseline$fit
newdat_cv_baseline$ul <- preds_baseline$fit + preds_baseline$se.fit * 1.96
newdat_cv_baseline$ll <- preds_baseline$fit - preds_baseline$se.fit * 1.96

newdat_cv_baseline$model <- "baseline"

# full

newdat_cv_full <- newdat_cv

newdat_cv_full$dur <- preds_full$fit
newdat_cv_full$ul <- preds_full$fit + preds_full$se.fit * 1.96
newdat_cv_full$ll <- preds_full$fit - preds_full$se.fit * 1.96

newdat_cv_full$model <- "type"

newdat_all <- bind_rows(
  newdat_cv_baseline,
  newdat_cv_full
)

d_uttr_plot %>%
  ggplot(data = ., aes(x = segment_dur_uttr, y = value, col = measure)) +
  facet_wrap(. ~ language) +
  geom_point(alpha = 0.1, pch=16) +
  #geom_ribbon(data = filter(newdat_cv_all,
  #                          model == "dur",
  #                          segment_type_o == "vowel_dur_uttr"),
  #            aes(ymin = ll, ymax = ul), col = NA, fill = "grey",
  #            alpha = 0.5) +
  #geom_ribbon(data = filter(newdat_cv,
  #                          measure_type == "dur",
  #                          segment_type_o == "cons_dur_uttr"),
   #           aes(ymin = ll, ymax = ul), col = NA, fill = "grey",
   #           alpha = 0.5) +
  geom_line(data = filter(newdat_all,
                          segment_type_o == "vowel"),
            aes(lty=model, y=dur),
            col = "darkorange1", lwd = 1) +
  geom_line(data = filter(newdat_all,
                          segment_type_o == "consonant"),
            aes(lty=model, y=dur),
            col = "purple4", lwd = 1) +
  scale_x_log10(breaks = c(0.05, 0.07, 0.1, 0.14)) +
  scale_y_log10(breaks = c(0.05, 0.07, 0.1, 0.14),
                limits = c(0.03, 0.19)) +
  #scale_x_continuous(limits=c(0.035,0.145), 
  #                   breaks=seq(0.04,0.14,0.02),
  #                   labels=c(".04",".06",".08",".10",".12",".14")) +
  scale_colour_manual(values = c("purple", "orange"), guide = "none") +
  #scale_y_continuous(breaks=seq(0.04,0.20,0.02)) +
    # labels for axes
  xlab("Average segment duration in s (inverse speech rate)") +
  labs(y = "Average C vs. V duration in s") +
  #ylab("Average V vs. C duration in s") +
  # remove clutter
  theme_minimal()


eff_sizes <- list()

# model predictions
newdat_deriv <- expand.grid(
  speakerSegtype = d_seg$speakerSegtype[1],
  languageSegtype = unique(d_seg$languageSegtype),
  c_type_f = d_seg$c_type_f[1]
)

newdat_deriv$segment_type_o <- str_extract(newdat_deriv$languageSegtype,
                                        "[^.]*$")
newdat_deriv$segment_type_o <- as.ordered(newdat_deriv$segment_type_o)
contrasts(newdat_deriv$segment_type_o) <- "contr.treatment"

newdat_deriv$language <- str_extract(newdat_deriv$languageSegtype,
                                        "^[^.]*")
newdat_deriv$language_f <- as.factor(newdat_deriv$language)
newdat_deriv$speaker_f <- newdat_cv$speaker_f[1]

language_med_durs <- d_seg %>%
  group_by(language) %>%
  summarise(segment_dur_uttr = median(segment_dur_uttr)) %>%
  ungroup()

newdat_deriv <- left_join(
  newdat_deriv,
  language_med_durs,
  by = "language"
)

eps <- 0.001

newdat_deriv_1 <- newdat_deriv %>%
  mutate(segment_dur_uttr = exp(log(segment_dur_uttr) - (eps/2)))
newdat_deriv_2 <- newdat_deriv %>%
  mutate(segment_dur_uttr = exp(log(segment_dur_uttr) + (eps/2)))

mods <- c("baseline", "type")
for (m in mods) {
X0 <- predict(get(m), 
              newdat_deriv_1,
              exclude=c(
                "s(segment_dur_uttr,speakerSegtype)",
                "s(segment_dur_uttr,speaker_f)",
                "s(segment_dur_uttr,speaker_f):segment_type_ovowel_dur_uttr",
                "s(segment_dur_uttr,c_type_f)"
              )
) %>% log()
X1 <- predict(get(m), 
              newdat_deriv_2,
              exclude=c(
                "s(segment_dur_uttr,speakerSegtype)",
                "s(segment_dur_uttr,speaker_f)",
                "s(segment_dur_uttr,speaker_f):segment_type_ovowel_dur_uttr",
                "s(segment_dur_uttr,c_type_f)"
              )
) %>% log()

# finite difference approximation of first derivative
# the design matrix
first_deriv <- (X1 - X0) / eps
#first_deriv <- Xp %*% coef(get(m))

newdat_deriv$derivative <- first_deriv
newdat_deriv$model <- m

eff_sizes[[m]] <- newdat_deriv %>%
  dplyr::select(language, segment_type_o, segment_dur_uttr, model, derivative) %>%
  group_by(language, segment_dur_uttr, model) %>%
  summarise(eff_size = derivative[segment_type_o == "vowel"] - derivative[segment_type_o == "consonant"]) %>%
  ungroup() %>%
  arrange(desc(eff_size))
}

eff_sizes_df <- bind_rows(eff_sizes)

for (m in mods) {
  
  eff_sizes_m <- eff_sizes[[m]]
  eff_sizes_m$language <- factor(eff_sizes_m$language, levels=eff_sizes_m$language)
  eff_sizes_m$segment_dur_uttr <- 0.05
  eff_sizes_m$value <- 0.13
  
  newdat_m <- filter(newdat_all, model==m)
  newdat_m$language <- factor(newdat_m$language, levels=eff_sizes_m$language)
  
  plot_dat <- d_uttr_plot
  plot_dat$language <- factor(plot_dat$language, levels=eff_sizes_m$language)
  
  plot_dat %>%
    ggplot(data = ., aes(x = segment_dur_uttr, y = value, col = measure)) +
    facet_wrap(. ~ language) +
    geom_point(alpha = 0.1, pch=16) +
    #geom_ribbon(data = filter(newdat_cv_all,
    #                          model == "dur",
    #                          segment_type_o == "vowel_dur_uttr"),
    #            aes(ymin = ll, ymax = ul), col = NA, fill = "grey",
    #            alpha = 0.5) +
    #geom_ribbon(data = filter(newdat_cv,
    #                          measure_type == "dur",
    #                          segment_type_o == "cons_dur_uttr"),
    #            aes(ymin = ll, ymax = ul), col = NA, fill = "grey",
    #            alpha = 0.5) +
    geom_line(data = filter(newdat_m,
                            segment_type_o == "vowel"),
              aes(lty=model, y=dur),
              col = "darkorange1", lwd = 1) +
    geom_line(data = filter(newdat_m,
                            segment_type_o == "consonant"),
              aes(lty=model, y=dur),
              col = "purple4", lwd = 1) +
    geom_text(data=eff_sizes_m, 
              aes(label=paste0("Δβ = ", round(eff_size,2))),
              col="black", size=5) +
    scale_x_log10(breaks = c(0.05, 0.07, 0.1, 0.14)) +
    scale_y_log10(breaks = c(0.05, 0.07, 0.1, 0.14),
                  limits = c(0.03, 0.19)) +
    scale_colour_manual(values = c("purple", "orange"), guide = "none") +
    xlab("Average segment duration in s (inverse speech rate)") +
    labs(y = "Average C vs. V duration in s") +
    theme_minimal() +
    theme(panel.grid = element_blank(),
        axis.line = element_line(size=0.8),
        axis.ticks = element_line(size=0.8),
        axis.text = element_text(size=16, colour="black"),
        axis.title = element_text(size=18, face="bold"),
        strip.background.y = element_blank(), 
        strip.placement = "outside",
        strip.text=element_text(size=18, face="bold"))
  ggsave(paste0("graphs/", m, ".png"), width=9, height=9, dpi=300)
}


# -------------------------------------------------------------------------
# Shared settings
# -------------------------------------------------------------------------

mods_cv <- c(baseline = "cv_mod_baseline", type = "cv_mod_type")

exclude_terms <- c(
  "s(segment_dur_uttr,speakerSegtype)",
  "s(segment_dur_uttr,speaker_f)",
  "s(segment_dur_uttr,c_type_f)"
)

eps <- 0.001

# -------------------------------------------------------------------------
# Prediction grid
# -------------------------------------------------------------------------

newdat_cv_deriv_curve <- expand.grid(
  segment_dur_uttr = seq(
    min(d_seg$segment_dur_uttr),
    max(d_seg$segment_dur_uttr),
    length.out = 100
  ),
  c_type_f = d_seg$c_type_f[1],
  speakerSegtype = d_seg$speakerSegtype[1],
  languageSegtype = unique(d_seg$languageSegtype)
) %>%
  mutate(
    segment_type = str_extract(languageSegtype, "[^.]*$"),
    segment_type_o = as.ordered(segment_type),
    language = str_extract(languageSegtype, "^[^.]*"),
    language_f = as.factor(language),
    speaker_f = as.factor(str_extract(speakerSegtype, "^[^.]*"))
  )

contrasts(newdat_cv_deriv_curve$segment_type_o) <- "contr.treatment"

# -------------------------------------------------------------------------
# Density estimates by language
# -------------------------------------------------------------------------

segment_dist_stats <- d_seg %>%
  select(language, segment_dur_uttr) %>%
  group_by(language) %>%
  nest() %>%
  mutate(
    segment_dur_uttr_med = map_dbl(data, ~ median(.x$segment_dur_uttr)),
    dens_data = map(
      data,
      ~ broom::tidy(
        density(
          .x$segment_dur_uttr,
          n = 100,
          from = min(d_seg$segment_dur_uttr),
          to = max(d_seg$segment_dur_uttr)
        )
      )
    )
  ) %>%
  unnest(dens_data) %>%
  mutate(
    segment_dur_uttr = x,
    density = y / max(y)
  ) %>%
  ungroup() %>%
  select(language, segment_dur_uttr_med, segment_dur_uttr, density)

# -------------------------------------------------------------------------
# Join density information onto prediction grid
# -------------------------------------------------------------------------

newdat_cv_deriv_curve <- newdat_cv_deriv_curve %>%
  mutate(segment_dur_uttr = round(segment_dur_uttr, 15)) %>%
  left_join(
    segment_dist_stats %>%
      mutate(segment_dur_uttr = round(segment_dur_uttr, 15)),
    by = c("language", "segment_dur_uttr")
  )

# -------------------------------------------------------------------------
# Finite difference datasets
# -------------------------------------------------------------------------

newdat_cv_deriv_curve_1 <- newdat_cv_deriv_curve %>%
  mutate(segment_dur_uttr = exp(log(segment_dur_uttr) - eps / 2))

newdat_cv_deriv_curve_2 <- newdat_cv_deriv_curve %>%
  mutate(segment_dur_uttr = exp(log(segment_dur_uttr) + eps / 2))

# -------------------------------------------------------------------------
# Helper function
# -------------------------------------------------------------------------

predict_derivative_curve <- function(model, model_name) {
  
  x1 <- predict(
    model,
    newdata = newdat_cv_deriv_curve_1,
    exclude = exclude_terms
  ) %>% log()
  
  x2 <- predict(
    model,
    newdata = newdat_cv_deriv_curve_2,
    exclude = exclude_terms
  ) %>% log()
  
  x0 <- predict(
    model,
    newdata = newdat_cv_deriv_curve,
    exclude = exclude_terms
  )
  
  deriv_curve <- newdat_cv_deriv_curve %>%
    mutate(
      derivative = (x2 - x1) / eps,
      phone_dur = x0,
      model = model_name
    )
  
  deriv_curve %>%
    select(
      language,
      segment_type_o,
      segment_dur_uttr_med,
      segment_dur_uttr,
      density,
      phone_dur,
      model,
      derivative
    ) %>%
    group_by(
      language,
      segment_dur_uttr_med,
      segment_dur_uttr,
      density,
      model
    ) %>%
    summarise(
      derivative_c = derivative[segment_type_o == "consonant"],
      derivative_v = derivative[segment_type_o == "vowel"],
      delta_deriv = derivative_v - derivative_c,
      phone_dur_v = phone_dur[segment_type_o == "vowel"],
      phone_dur_c = phone_dur[segment_type_o == "consonant"],
      .groups = "drop"
    ) %>%
    group_by(language) %>%
    mutate(
      derivative_v_w = derivative_v * density,
      derivative_c_w = derivative_c * density,
      delta_deriv_w = delta_deriv * density,
      phone_dur_v_w = phone_dur_v * density,
      phone_dur_c_w = phone_dur_c * density
    ) %>%
    ungroup()
}

# -------------------------------------------------------------------------
# Compute effect curves
# -------------------------------------------------------------------------

eff_curves_cv <- imap(
  mods_cv,
  ~ predict_derivative_curve(
    model = get(.x),
    model_name = .y
  )
)

# -------------------------------------------------------------------------
# Compute density-weighted effect sizes
# -------------------------------------------------------------------------

eff_sizes_dw_cv <- imap(
  eff_curves_cv,
  ~ .x %>%
    group_by(
      language,
      segment_dur_uttr_med,
      model
    ) %>%
    summarise(
      density_area = sum(density),
      derivative_v_w_area = sum(derivative_v_w),
      derivative_c_w_area = sum(derivative_c_w),
      delta_deriv_w_area = sum(delta_deriv_w),
      phone_dur_v_w_area = sum(phone_dur_v_w),
      phone_dur_c_w_area = sum(phone_dur_c_w),
      eff_size_dw = delta_deriv_w_area / density_area,
      derivative_v_dw = derivative_v_w_area / density_area,
      derivative_c_dw = derivative_c_w_area / density_area,
      phone_dur_v_dw = phone_dur_v_w_area / density_area,
      phone_dur_c_dw = phone_dur_c_w_area / density_area,
      .groups = "drop"
    ) %>%
    left_join(
      eff_sizes[[.y]],
      by = "language"
    ) %>%
    arrange(desc(eff_size_dw))
)

# -------------------------------------------------------------------------
# Export combined outputs
# -------------------------------------------------------------------------

eff_curves_cv_df <- bind_rows(eff_curves_cv)

write_csv(
  eff_curves_cv_df,
  "eff_curves_cv_df.csv"
)

eff_sizes_dw_cv_df <- bind_rows(eff_sizes_dw_cv)

write_csv(
  eff_sizes_dw_cv_df,
  "eff_sizes_dw_cv_df.csv"
)

for (m in mods) {
  
  eff_sizes_m <- eff_sizes_dw_cv[[m]]
  eff_sizes_m$language <- factor(eff_sizes_m$language, levels = eff_sizes_m$language)
  eff_sizes_m$segment_dur_uttr <- 0.05
  eff_sizes_m$value <- 0.13
  
  newdat_m <- filter(newdat_all, model == m)
  newdat_m$language <- factor(newdat_m$language, levels=eff_sizes_m$language)
  
  plot_dat <- d_uttr_plot
  plot_dat$language <- factor(plot_dat$language, levels=eff_sizes_m$language)
  
  plot_dat %>%
    ggplot(data = ., aes(x = segment_dur_uttr, y = value, col = measure)) +
    facet_wrap(. ~ language) +
    geom_point(alpha = 0.1, pch=16) +
    geom_line(data = filter(newdat_m,
                            segment_type_o == "vowel"),
              aes(lty=model, y=dur),
              col = "darkorange1", lwd = 1) +
    geom_line(data = filter(newdat_m,
                            segment_type_o == "consonant"),
              aes(lty=model, y=dur),
              col = "purple4", lwd = 1) +
    geom_text(data=eff_sizes_m, 
              aes(label=paste0("Δβ = ", round(eff_size,2))),
              col="black", size=5) +
    scale_x_log10(breaks = c(0.05, 0.07, 0.1, 0.14)) +
    scale_y_log10(breaks = c(0.05, 0.07, 0.1, 0.14),
                  limits = c(0.03, 0.19)) +
    scale_colour_manual(values = c("purple", "orange"), guide = "none") +
    xlab("Average segment duration in s (inverse speech rate)") +
    labs(y = "Average C vs. V duration in s") +
    theme_minimal() +
    theme(panel.grid = element_blank(),
          axis.line = element_line(size=0.8),
          axis.ticks = element_line(size=0.8),
          axis.text = element_text(size=16, colour="black"),
          axis.title = element_text(size=18, face="bold"),
          strip.background.y = element_blank(), 
          strip.placement = "outside",
          strip.text=element_text(size=18, face="bold"))
  ggsave(paste0("graphs/", m, "_dw.png"), width=9, height=9, dpi=300)
}
