library(tidyverse)
library(mgcv)
library(itsadug)

apah <- read_csv(
  "../doreco_data/doreco_apah1238_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Yali") %>%
  arrange(speaker, discourse, phone_start)

arap <- read_csv(
  "../doreco_data/doreco_arap1274_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Arapaho") %>%
  arrange(speaker, discourse, phone_start)

bain <- read_csv(
  "../doreco_data/doreco_bain1259_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Gubeeher") %>%
  arrange(speaker, discourse, phone_start)

beja <- read_csv(
  "../doreco_data/doreco_beja1238_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Beja") %>%
  arrange(speaker, discourse, phone_start)

bora <- read_csv(
  "../doreco_data/doreco_bora1263_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Bora") %>%
  arrange(speaker, discourse, phone_start)

dolg <- read_csv(
  "../doreco_data/doreco_dolg1241_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Dolgan") %>%
  arrange(speaker, discourse, phone_start)

even <- read_csv(
  "../doreco_data/doreco_even1259_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Evenki") %>%
  arrange(speaker, discourse, phone_start)

guri <- read_csv(
  "../doreco_data/doreco_guri1247_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Gurindji") %>%
  arrange(speaker, discourse, phone_start)

jeju <- read_csv(
  "../doreco_data/doreco_jeju1234_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Jejuan") %>%
  arrange(speaker, discourse, phone_start)

kama <- read_csv(
  "../doreco_data/doreco_kama1351_durations.csv",
  col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")
) %>%
  mutate(language="Kamas") %>%
  arrange(speaker, discourse, phone_start)

lowe <- read_csv("../doreco_data/doreco_lowe1385_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Lower_Sorbian") %>%
  arrange(speaker, discourse, phone_start)

movi <- read_csv("../doreco_data/doreco_movi1243_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Movima") %>%
  arrange(speaker, discourse, phone_start)

ngal <- read_csv("../doreco_data/doreco_ngal1292_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Dalabon") %>%
  arrange(speaker, discourse, phone_start)

nngg <- read_csv("../doreco_data/doreco_nngg1234_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Nuu") %>%
  arrange(speaker, discourse, phone_start)

orko <- read_csv("../doreco_data/doreco_orko1234_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Fanbyak") %>%
  arrange(speaker, discourse, phone_start)

resi <- read_csv("../doreco_data/doreco_resi1247_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Resigaro") %>%
  arrange(speaker, discourse, phone_start)

ruul <- read_csv("../doreco_data/doreco_ruul1235_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Ruuli") %>%
  arrange(speaker, discourse, phone_start)

sadu <- read_csv("../doreco_data/doreco_sadu1234_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Sadu") %>%
  arrange(speaker, discourse, phone_start)

sanz <- read_csv("../doreco_data/doreco_sanz1248_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Sanzhi_Dargwa") %>%
  arrange(speaker, discourse, phone_start)

sout <- read_csv("../doreco_data/doreco_sout3282_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="English") %>%
  arrange(speaker, discourse, phone_start)

svan <- read_csv("../doreco_data/doreco_svan1243_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Svan") %>%
  arrange(speaker, discourse, phone_start)

trin <- read_csv("../doreco_data/doreco_trin1278_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Mojeno_Trinitario") %>%
  arrange(speaker, discourse, phone_start)

urum <- read_csv("../doreco_data/doreco_urum1249_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Urum") %>%
  arrange(speaker, discourse, phone_start)

vera <- read_csv("../doreco_data/doreco_vera1241_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Veraa") %>%
  arrange(speaker, discourse, phone_start)

yong <- read_csv("../doreco_data/doreco_yong1270_durations.csv",
                 col_types = cols(.default = "?", speaker = "c", sex = "c", all_speakers = "c")) %>%
  mutate(language="Yongning_Na") %>%
  arrange(speaker, discourse, phone_start)

df.drc <- bind_rows(
  apah,
  arap,
  bain,
  beja,
  bora,
  dolg,
  even,
  guri,
  jeju,
  kama,
  lowe,
  movi,
  ngal,
  nngg,
  orko,
  resi,
  ruul,
  sadu,
  sanz,
  sout,
  svan,
  trin,
  urum,
  vera,
  yong
)

df.drc <- read_csv("../data/DoReCo.csv")
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
saveRDS(cv_mod_baseline, "cv_mod_baseline.rds")
cv_mod_baseline <- readRDS("cv_mod_baseline.rds")
summary(cv_mod_baseline)
