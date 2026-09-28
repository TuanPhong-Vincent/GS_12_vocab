/**
 * GLOBAL SUCCESS 12 - 50-DAY SPACED REPETITION VOCABULARY CHALLENGE DATA
 * Contains 5 Modules, 50 Days, covering all core vocabulary and grammar structures
 * from Global Success 12 (Units 1, 2, 3), 40 target grammar structures,
 * and 10 milestone review sessions based on Leitner Spaced Repetition.
 */

const GS12_50_DAYS_DATA = [
  {
    "day": 1,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "UNIT 01: LIFE STORIES WE ADMIRE",
    "subtopic": "Giai đoạn cuộc đời & Trưởng thành",
    "reviewInfo": "Ngày đầu tiên, chưa có bài cũ.",
    "isReview": false,
    "grammar": {
      "structure": "While + S + was/were + V-ing, S + V-ed",
      "note": "Diễn tả hành động đang diễn ra trong quá khứ thì một hành động khác xen vào (Global Success 12 Unit 1)",
      "example": "While he was spending his childhood in a peaceful village, he developed a deep passion for science."
    },
    "vocab": [
      {
        "id": "d1_1",
        "word": "childhood",
        "phonetics": "/ˈtʃaɪldhʊd/",
        "pos": "n",
        "meaning": "thời thơ ấu, tuổi thơ",
        "collocation": "spend one's childhood (trải qua thời thơ ấu)",
        "example": "While he was spending his childhood in a peaceful village, he developed a deep passion for science."
      },
      {
        "id": "d1_2",
        "word": "youth",
        "phonetics": "/juːθ/",
        "pos": "n",
        "meaning": "tuổi trẻ, thời thanh xuân",
        "collocation": "in one's youth (thời thanh xuân)",
        "example": "During her youth, she was working tirelessly as a volunteer teacher when the war broke out."
      },
      {
        "id": "d1_3",
        "word": "attend school",
        "phonetics": "/əˈtend skuːl/",
        "pos": "v.phr",
        "meaning": "đi học, theo học ở trường",
        "collocation": "attend school regularly (đi học đều đặn)",
        "example": "He attended school in his hometown while his older brothers were serving in the military."
      },
      {
        "id": "d1_4",
        "word": "attend college",
        "phonetics": "/əˈtend ˈkɒlɪdʒ/",
        "pos": "v.phr",
        "meaning": "theo học cao đẳng, học đại học",
        "collocation": "attend college full-time (theo học đại học chính quy)",
        "example": "She was attending college in the capital when she received a prestigious scholarship to study abroad."
      },
      {
        "id": "d1_5",
        "word": "drop out",
        "phonetics": "/drɒp aʊt/",
        "pos": "phr.v",
        "meaning": "bỏ học, nghỉ học giữa chừng",
        "collocation": "drop out of college (bỏ học đại học giữa chừng)",
        "example": "He dropped out of university because he was already running an innovative computer business."
      },
      {
        "id": "d1_6",
        "word": "marriage",
        "phonetics": "/ˈmærɪdʒ/",
        "pos": "n",
        "meaning": "cuộc hôn nhân, sự kết hôn",
        "collocation": "enter into marriage (bước vào cuộc sống hôn nhân)",
        "example": "Their marriage remained strong for decades while they were overcoming many difficult hardships together."
      }
    ]
  },
  {
    "day": 2,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "UNIT 01: LIFE STORIES WE ADMIRE",
    "subtopic": "Gia đình, Biến cố & Sự mất mát",
    "reviewInfo": "Ôn thẻ của Day 1 (Mốc +1).",
    "isReview": false,
    "grammar": {
      "structure": "S + was/were + V-ing + when + S + V-ed",
      "note": "Diễn tả hành động đang diễn ra thì bị một sự kiện bất ngờ khác cắt ngang",
      "example": "The scientist was working tirelessly on his research when he passed away."
    },
    "vocab": [
      {
        "id": "d2_1",
        "word": "have a long marriage",
        "phonetics": "/hæv ə lɒŋ ˈmærɪdʒ/",
        "pos": "v.phr",
        "meaning": "có một cuộc hôn nhân lâu dài",
        "collocation": "have a long marriage of over fifty years (có cuộc hôn nhân bền vững hơn 50 năm)",
        "example": "My grandparents had a long marriage of over fifty years and they were always supporting each other."
      },
      {
        "id": "d2_2",
        "word": "adopt",
        "phonetics": "/əˈdɒpt/",
        "pos": "v",
        "meaning": "nhận nuôi (con nuôi)",
        "collocation": "adopt a child (nhận nuôi một đứa trẻ)",
        "example": "A kind family adopted the orphan while the village was recovering from the flood."
      },
      {
        "id": "d2_3",
        "word": "biological parents",
        "phonetics": "/ˌbaɪəˈlɒdʒɪkl ˈpeərənts/",
        "pos": "n.phr",
        "meaning": "cha mẹ ruột",
        "collocation": "search for biological parents (tìm kiếm cha mẹ ruột)",
        "example": "While she was searching for her identity, she finally met her biological parents in 2015."
      },
      {
        "id": "d2_4",
        "word": "cancer",
        "phonetics": "/ˈkænsə/",
        "pos": "n",
        "meaning": "bệnh ung thư",
        "collocation": "battle against cancer (chiến đấu chống lại bệnh ung thư)",
        "example": "The scientist was still conducting groundbreaking research when he was diagnosed with cancer."
      },
      {
        "id": "d2_5",
        "word": "pass away",
        "phonetics": "/pɑːs əˈweɪ/",
        "pos": "phr.v",
        "meaning": "qua đời, mất (nói giảm nói tránh)",
        "collocation": "pass away peacefully (thanh thản qua đời)",
        "example": "The beloved artist passed away peacefully in 2020 while his family members were gathering beside him."
      },
      {
        "id": "d2_6",
        "word": "death",
        "phonetics": "/deθ/",
        "pos": "n",
        "meaning": "cái chết, sự qua đời",
        "collocation": "tragic death (sự ra đi thương tâm)",
        "example": "Shortly after the inventor's death, millions of admirers were sharing heartfelt tributes on the internet."
      }
    ]
  },
  {
    "day": 3,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "UNIT 01: LIFE STORIES WE ADMIRE",
    "subtopic": "Phẩm chất, Hoài bão & Trí tuệ",
    "reviewInfo": "Ôn thẻ của Day 2 (Mốc +1). Chuẩn bị mốc +3 cho Day 1.",
    "isReview": false,
    "grammar": {
      "structure": "S + used to / would + V(bare)",
      "note": "Diễn tả thói quen hoặc trạng thái trong quá khứ nay không còn nữa",
      "example": "In his youth, the visionary entrepreneur used to read books until midnight."
    },
    "vocab": [
      {
        "id": "d3_1",
        "word": "genius",
        "phonetics": "/ˈdʒiːniəs/",
        "pos": "n",
        "meaning": "thiên tài",
        "collocation": "mathematical genius (thiên tài toán học)",
        "example": "While the engineers were struggling with the complex design, the young genius proposed a simple solution."
      },
      {
        "id": "d3_2",
        "word": "visionary",
        "phonetics": "/ˈvɪʒnri/",
        "pos": "n",
        "meaning": "người nhìn xa trông rộng, nhà lãnh đạo có tầm nhìn",
        "collocation": "visionary leader (nhà lãnh đạo có tầm nhìn chiến lược)",
        "example": "The visionary was already planning electric transport when most people were still relying on fossil fuels."
      },
      {
        "id": "d3_3",
        "word": "determination",
        "phonetics": "/dɪˌtɜːmɪˈneɪʃn/",
        "pos": "n",
        "meaning": "sự quyết tâm, lòng kiên định",
        "collocation": "unwavering determination (lòng quyết tâm kiên định)",
        "example": "She showed incredible determination while she was training for the marathon through harsh winter storms."
      },
      {
        "id": "d3_4",
        "word": "ambitious",
        "phonetics": "/æmˈbɪʃəs/",
        "pos": "adj",
        "meaning": "có nhiều hoài bão, giàu tham vọng",
        "collocation": "ambitious goals (mục tiêu đầy hoài bão)",
        "example": "The ambitious student was studying day and night while his peers were playing video games."
      },
      {
        "id": "d3_5",
        "word": "well educated",
        "phonetics": "/ˌwel ˈedʒukeɪtɪd/",
        "pos": "adj",
        "meaning": "có học thức cao, được giáo dục tốt",
        "collocation": "well educated person (người có học thức uyên bác)",
        "example": "She was well educated and was speaking four foreign languages fluently when she joined the diplomatic service."
      }
    ]
  },
  {
    "day": 4,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "UNIT 01: LIFE STORIES WE ADMIRE",
    "subtopic": "Cống hiến, Ngưỡng mộ & Gắn kết",
    "reviewInfo": "Ôn thẻ Day 3 (Mốc +1) và Day 1 (Mốc +3). Lần đầu có 2 ngày cũ.",
    "isReview": false,
    "grammar": {
      "structure": "S + be admired for + V-ing / Noun",
      "note": "Mẫu câu ca ngợi phẩm chất, cống hiến hoặc hành động cao đẹp của một nhân vật",
      "example": "Dr. Dang Thuy Tram is admired for devoting her youth to the resistance war."
    },
    "vocab": [
      {
        "id": "d4_1",
        "word": "dedicated to",
        "phonetics": "/ˈdedɪkeɪtɪd tuː/",
        "pos": "adj.phr",
        "meaning": "tận tâm, cống hiến hết mình cho",
        "collocation": "dedicated to helping others (tận tâm giúp đỡ người khác)",
        "example": "He was completely dedicated to medical charity work while other doctors were pursuing lucrative careers."
      },
      {
        "id": "d4_2",
        "word": "devote to",
        "phonetics": "/dɪˈvəʊt tuː/",
        "pos": "v.phr",
        "meaning": "cống hiến, dành hết tâm huyết cho",
        "collocation": "devote one's life to (cống hiến cả cuộc đời cho)",
        "example": "The scientist devoted her life to research while she was living in a humble laboratory in Paris."
      },
      {
        "id": "d4_3",
        "word": "admire",
        "phonetics": "/ədˈmaɪə/",
        "pos": "v",
        "meaning": "ngưỡng mộ, khâm phục",
        "collocation": "admire someone deeply (vô cùng ngưỡng mộ ai đó)",
        "example": "We admired his bravery because he saved two children while the house was burning fiercely."
      },
      {
        "id": "d4_4",
        "word": "be admired for",
        "phonetics": "/bi ədˈmaɪəd fɔː/",
        "pos": "v.phr",
        "meaning": "được ngưỡng mộ/khâm phục vì điều gì",
        "collocation": "be admired for courage (được ngưỡng mộ vì lòng dũng cảm)",
        "example": "The female ruler was admired for her wisdom while she was leading the kingdom through a crisis."
      },
      {
        "id": "d4_5",
        "word": "bond over",
        "phonetics": "/bɒnd ˈəʊvə/",
        "pos": "phr.v",
        "meaning": "gắn kết, trở nên thân thiết nhờ sở thích chung",
        "collocation": "bond over shared interests (gắn kết nhờ chung sở thích)",
        "example": "They bonded over their love of classical music while they were attending a summer camp in 2018."
      }
    ]
  },
  {
    "day": 5,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "UNIT 01: LIFE STORIES WE ADMIRE",
    "subtopic": "Thành tựu, Đột phá & Công nghệ",
    "reviewInfo": "Ôn thẻ Day 4 (Mốc +1) và Day 2 (Mốc +3).",
    "isReview": false,
    "grammar": {
      "structure": "While + S1 + was/were + V1-ing, S2 + was/were + V2-ing",
      "note": "Diễn tả hai hành động kéo dài xảy ra song song đồng thời trong quá khứ",
      "example": "While Steve Jobs was developing cutting-edge technology, his team was creating digital animations."
    },
    "vocab": [
      {
        "id": "d5_1",
        "word": "achievement",
        "phonetics": "/əˈtʃiːvmənt/",
        "pos": "n",
        "meaning": "thành tựu, thành tích",
        "collocation": "remarkable achievement (thành tựu đáng nể)",
        "example": "She celebrated her greatest scientific achievement while colleagues from all over the world were congratulating her."
      },
      {
        "id": "d5_2",
        "word": "impressive achievement",
        "phonetics": "/ɪmˈpresɪv əˈtʃiːvmənt/",
        "pos": "n.phr",
        "meaning": "thành tựu ấn tượng",
        "collocation": "recognize impressive achievement (ghi nhận thành tựu ấn tượng)",
        "example": "Winning three gold medals was an impressive achievement when he was only seventeen years old."
      },
      {
        "id": "d5_3",
        "word": "national hero",
        "phonetics": "/ˌnæʃnəl ˈhɪərəʊ/",
        "pos": "n.phr",
        "meaning": "anh hùng dân tộc",
        "collocation": "venerate a national hero (tôn kính người anh hùng dân tộc)",
        "example": "The people declared him a national hero because he was defending the border when enemy troops attacked."
      },
      {
        "id": "d5_4",
        "word": "military genius",
        "phonetics": "/ˈmɪlətri ˈdʒiːniəs/",
        "pos": "n.phr",
        "meaning": "thiên tài quân sự",
        "collocation": "strategic military genius (thiên tài quân sự lỗi lạc)",
        "example": "The military genius changed his battle tactics while the enemy was preparing for a frontal assault."
      },
      {
        "id": "d5_5",
        "word": "cutting-edge technology",
        "phonetics": "/ˌkʌtɪŋ edʒ tekˈnɒlədʒi/",
        "pos": "n.phr",
        "meaning": "công nghệ tiên tiến nhất, công nghệ đỉnh cao",
        "collocation": "apply cutting-edge technology (ứng dụng công nghệ tối tân)",
        "example": "The startup was adopting cutting-edge technology when other competitors were still relying on outdated equipment."
      },
      {
        "id": "d5_6",
        "word": "blockbuster",
        "phonetics": "/ˈblɒkbʌstə/",
        "pos": "n",
        "meaning": "phim bom tấn (rất thành công và thu hút đông đảo người xem)",
        "collocation": "summer blockbuster (phim bom tấn mùa hè)",
        "example": "The studio released an animated blockbuster while cinemas across the country were seeing record audiences."
      }
    ]
  },
  {
    "day": 6,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "UNIT 01: LIFE STORIES WE ADMIRE",
    "subtopic": "Lịch sử, Vương triều & Kháng chiến",
    "reviewInfo": "Ôn thẻ Day 5 (Mốc +1) và Day 3 (Mốc +3).",
    "isReview": false,
    "grammar": {
      "structure": "S + V1-ed, V2-ed, and V3-ed",
      "note": "Chuỗi hành động kế tiếp nhau trong quá khứ kể lại tiểu sử nhân vật",
      "example": "The king established his kingdom, defeated the invaders, and built an independent nation."
    },
    "vocab": [
      {
        "id": "d6_1",
        "word": "tourist attraction",
        "phonetics": "/ˈtʊərɪst əˈtrækʃn/",
        "pos": "n.phr",
        "meaning": "điểm thu hút khách du lịch, địa điểm du lịch",
        "collocation": "major tourist attraction (điểm du lịch trọng điểm)",
        "example": "Thousands of visitors were exploring the famous tourist attraction when fireworks illuminated the night sky."
      },
      {
        "id": "d6_2",
        "word": "theme park",
        "phonetics": "/ˈθiːm pɑːk/",
        "pos": "n.phr",
        "meaning": "công viên giải trí theo chủ đề",
        "collocation": "visit a theme park (thăm quan công viên giải trí)",
        "example": "Families were enjoying rides in the theme park when the grand parade started in the afternoon."
      },
      {
        "id": "d6_3",
        "word": "rule",
        "phonetics": "/ruːl/",
        "pos": "v",
        "meaning": "cai trị, trị vì",
        "collocation": "rule the country wisely (trị vì đất nước sáng suốt)",
        "example": "The queen ruled the country wisely while rival factions were attempting to seize power."
      },
      {
        "id": "d6_4",
        "word": "kingdom",
        "phonetics": "/ˈkɪŋdəm/",
        "pos": "n",
        "meaning": "vương quốc",
        "collocation": "establish a kingdom (thành lập một vương quốc)",
        "example": "Peace and prosperity returned to the kingdom while the new laws were being enacted."
      },
      {
        "id": "d6_5",
        "word": "independent",
        "phonetics": "/ˌɪndɪˈpendənt/",
        "pos": "adj",
        "meaning": "độc lập, tự chủ",
        "collocation": "declare an independent nation (tuyên bố một quốc gia độc lập)",
        "example": "The nation became fully independent while its citizens were rebuilding towns devastated by the conflict."
      },
      {
        "id": "d6_6",
        "word": "defeat",
        "phonetics": "/dɪˈfiːt/",
        "pos": "v",
        "meaning": "đánh bại, đánh thắng",
        "collocation": "defeat the invaders (đánh bại quân xâm lược)",
        "example": "Our brave soldiers defeated the foreign invaders while heavy rain was falling on the battlefield."
      }
    ]
  },
  {
    "day": 7,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "UNIT 01: LIFE STORIES WE ADMIRE",
    "subtopic": "Kháng chiến cứu nước & Y học dã chiến",
    "reviewInfo": "Ôn thẻ Day 6 (Mốc +1) và Day 4 (Mốc +3).",
    "isReview": false,
    "grammar": {
      "structure": "Passive: S + was/were + V3/ed + by + O",
      "note": "Câu bị động thì quá khứ đơn, nhấn mạnh sự kiện và cống hiến lịch sử",
      "example": "The resistance war was fought bravely by heroic soldiers to protect national independence."
    },
    "vocab": [
      {
        "id": "d7_1",
        "word": "resistance war",
        "phonetics": "/rɪˈzɪstəns wɔː/",
        "pos": "n.phr",
        "meaning": "cuộc kháng chiến",
        "collocation": "join the resistance war (tham gia cuộc kháng chiến)",
        "example": "Many patriots volunteered to fight in the resistance war while danger was surrounding them everywhere."
      },
      {
        "id": "d7_2",
        "word": "surgeon",
        "phonetics": "/ˈsɜːdʒən/",
        "pos": "n",
        "meaning": "bác sĩ phẫu thuật",
        "collocation": "battlefield surgeon (bác sĩ phẫu thuật chiến trường)",
        "example": "The surgeon was performing an urgent operation when the power suddenly went out."
      },
      {
        "id": "d7_3",
        "word": "field hospital",
        "phonetics": "/ˈfiːld hɒspɪtl/",
        "pos": "n.phr",
        "meaning": "bệnh viện dã chiến",
        "collocation": "set up a field hospital (thiết lập bệnh viện dã chiến)",
        "example": "Nurses were treating wounded soldiers in the field hospital while fighter planes were flying overhead."
      },
      {
        "id": "d7_4",
        "word": "carry out attacks",
        "phonetics": "/ˌkæri aʊt əˈtæks/",
        "pos": "v.phr",
        "meaning": "thực hiện các cuộc tấn công, tiến hành đánh úp",
        "collocation": "carry out surprise attacks (tiến hành các cuộc tập kích bất ngờ)",
        "example": "The guerrilla fighters carried out surprise attacks while the colonial army was resting in the garrison."
      },
      {
        "id": "d7_5",
        "word": "biography",
        "phonetics": "/baɪˈɒɡrəfi/",
        "pos": "n",
        "meaning": "tiểu sử, truyện ký",
        "collocation": "read an inspiring biography (đọc cuốn tiểu sử truyền cảm hứng)",
        "example": "I was reading an inspiring biography of Uncle Ho when my friend phoned me last night."
      },
      {
        "id": "d7_6",
        "word": "account",
        "phonetics": "/əˈkaʊnt/",
        "pos": "n",
        "meaning": "lời kể, sự thuật lại sự việc đã xảy ra",
        "collocation": "firsthand account (lời kể của nhân chứng trực tiếp)",
        "example": "The journalist gave an emotional account of the battle while listeners were wiping away their tears."
      }
    ]
  },
  {
    "day": 8,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "UNIT 01: LIFE STORIES WE ADMIRE",
    "subtopic": "Nghệ thuật hoạt họa & Thành ngữ cảm xúc",
    "reviewInfo": "Ôn thẻ Day 7 (Mốc +1), Day 5 (Mốc +3) và Day 1 (Mốc +7). 3 bài cũ.",
    "isReview": false,
    "grammar": {
      "structure": "When + S + V-ed, S + was/felt + [Idiom expressing happiness]",
      "note": "Cấu trúc biểu đạt cảm xúc hân hoan tột cùng khi gặt hái thành công vang dội",
      "example": "When he won the prestigious animation award, he felt on top of the world."
    },
    "vocab": [
      {
        "id": "d8_1",
        "word": "animator",
        "phonetics": "/ˈænɪmeɪtə/",
        "pos": "n",
        "meaning": "họa sĩ hoạt hình, người làm phim hoạt hình",
        "collocation": "talented animator (họa sĩ hoạt hình tài năng)",
        "example": "The talented animator was sketching cartoon characters by hand before computers became widespread in the 1990s."
      },
      {
        "id": "d8_2",
        "word": "film producer",
        "phonetics": "/ˈfɪlm prəˌdjuːsə/",
        "pos": "n.phr",
        "meaning": "nhà sản xuất phim",
        "collocation": "prominent film producer (nhà sản xuất phim danh tiếng)",
        "example": "The film producer was negotiating with foreign distributors when the movie won first prize at the festival."
      },
      {
        "id": "d8_3",
        "word": "computer animation",
        "phonetics": "/kəmˈpjuːtər ˌænɪˈmeɪʃn/",
        "pos": "n.phr",
        "meaning": "hoạt hình vi tính, kỹ xảo hoạt họa máy tính",
        "collocation": "pioneer computer animation (tiên phong trong hoạt họa vi tính)",
        "example": "Technicians were experimenting with computer animation when they created the groundbreaking three-dimensional movie."
      },
      {
        "id": "d8_4",
        "word": "on top of the world",
        "phonetics": "/ɒn tɒp əv ðə wɜːld/",
        "pos": "idiom",
        "meaning": "vô cùng hạnh phúc, vui sướng ngất ngây",
        "collocation": "feel on top of the world (cảm thấy hạnh phúc tột cùng)",
        "example": "She was feeling on top of the world when the headmaster announced her first-place victory."
      },
      {
        "id": "d8_5",
        "word": "on cloud nine",
        "phonetics": "/ɒn klaʊd naɪn/",
        "pos": "idiom",
        "meaning": "lâng lâng sung sướng, ngập tràn hạnh phúc",
        "collocation": "be on cloud nine (đang ngập tràn niềm vui)",
        "example": "He was on cloud nine for days while congratulations were pouring in from his relatives and friends."
      },
      {
        "id": "d8_6",
        "word": "over the moon",
        "phonetics": "/ˈəʊvə ðə muːn/",
        "pos": "idiom",
        "meaning": "sướng rơn, vui mừng khôn xiết",
        "collocation": "be over the moon (vui mừng hết cỡ)",
        "example": "The young writer was over the moon when the publisher agreed to print her debut novel."
      }
    ]
  },
  {
    "day": 9,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "REVIEW SÂU: CỦNG CỐ UNIT 01",
    "subtopic": "Tổng hợp phản xạ từ vựng & Cấu trúc Unit 01 (Phần 1: Cuộc đời & Tính cách)",
    "reviewInfo": "Quét lại toàn bộ các thẻ từ vựng & cấu trúc của Unit 01 (Day 1, 2, 3, 4).",
    "isReview": true,
    "reviewType": "DEEP_REVIEW",
    "targetDays": [
      1,
      2,
      3,
      4
    ],
    "reviewNotes": [
      "Phân biệt cụm từ cuộc đời: attend school / college (theo học) vs drop out (bỏ học giữa chừng); pass away (qua đời - cách nói trang trọng, giảm nhẹ) vs death (cái chết).",
      "Củng cố tính từ miêu tả nhân vật: genius (thiên tài), visionary (có tầm nhìn xa), ambitious (giàu hoài bão), dedicated to (tận tụy với).",
      "Luyện tập thì Quá khứ tiếp diễn kết hợp Quá khứ đơn: phân biệt rõ hành động nền (past continuous) và hành động cắt ngang (past simple)."
    ],
    "integratedExample": "While the visionary leader was attending college, he decided to drop out and devote his youth to technological innovation."
  },
  {
    "day": 10,
    "module": "MODULE 1: DANH NHÂN & CÂU CHUYỆN CUỘC ĐỜI",
    "unit": "REVIEW LIÊN KẾT (INTERLEAVING): MODULE 1",
    "subtopic": "Tổng ôn đan cài toàn diện Unit 01: Lịch sử, Thành tựu & Thành ngữ",
    "reviewInfo": "Quét đan cài toàn bộ Unit 01 (Day 1 đến Day 8). Chuẩn bị bước sang Module 2.",
    "isReview": true,
    "reviewType": "INTERLEAVING_REVIEW",
    "targetDays": [
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8
    ],
    "reviewNotes": [
      "Ôn tập cụm danh từ lịch sử và thành tựu: military genius, national hero, resistance war, cutting-edge technology, tourist attraction.",
      "Bộ ba thành ngữ cảm xúc đỉnh cao: on top of the world = on cloud nine = over the moon (vô cùng hạnh phúc trước thành công vang dội).",
      "Liên kết ngữ pháp: Chuỗi hành động quá khứ đơn (sequencing) và câu bị động quá khứ đơn trong bài viết tiểu sử (biography)."
    ],
    "integratedExample": "When the national hero defeated the invaders and restored independence, the whole kingdom was on top of the world."
  },
  {
    "day": 11,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "UNIT 02: A MULTICULTURAL WORLD",
    "subtopic": "Đa dạng văn hóa & Toàn cầu hóa",
    "reviewInfo": "Bắt đầu Module 2! Ôn thẻ Day 8 (Mốc +3) và Day 4 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "Definite Article: The + N (unique / specific / defined in context)",
      "note": "Dùng mạo từ 'the' trước danh từ chỉ sự vật duy nhất hoặc đã được xác định cụ thể trong văn cảnh",
      "example": "The cultural diversity of our country attracts international visitors from all over the world."
    },
    "vocab": [
      {
        "id": "d11_1",
        "word": "cultural diversity",
        "phonetics": "/ˌkʌltʃərəl daɪˈvɜːsəti/",
        "pos": "n.phr",
        "meaning": "sự đa dạng văn hóa",
        "collocation": "celebrate cultural diversity (tôn vinh sự đa dạng văn hóa)",
        "example": "The United States is home to people from hundreds of ethnic backgrounds who contribute to the cultural diversity of the nation."
      },
      {
        "id": "d11_2",
        "word": "globalisation",
        "phonetics": "/ˌɡləʊbəlaɪˈzeɪʃn/",
        "pos": "n",
        "meaning": "sự toàn cầu hóa",
        "collocation": "the impact of globalisation (tác động của toàn cầu hóa)",
        "example": "Globalisation allows artists in the UK to exchange creative ideas seamlessly with musicians across the Atlantic."
      },
      {
        "id": "d11_3",
        "word": "identity",
        "phonetics": "/aɪˈdentəti/",
        "pos": "n",
        "meaning": "bản sắc, danh tính",
        "collocation": "preserve cultural identity (bảo tồn bản sắc văn hóa)",
        "example": "A community must protect its cultural heritage because the heritage reflects the unique identity of its ancestors."
      },
      {
        "id": "d11_4",
        "word": "culture shock",
        "phonetics": "/ˈkʌltʃə ʃɒk/",
        "pos": "n.phr",
        "meaning": "cú sốc văn hóa",
        "collocation": "experience culture shock (trải qua cú sốc văn hóa)",
        "example": "Many exchange students experience culture shock when they first arrive in the US to attend university."
      },
      {
        "id": "d11_5",
        "word": "multicultural",
        "phonetics": "/ˌmʌltiˈkʌltʃərəl/",
        "pos": "adj",
        "meaning": "đa văn hóa",
        "collocation": "multicultural society (xã hội đa văn hóa)",
        "example": "London has grown into a vibrant multicultural metropolis where citizens speak over three hundred languages from around the world."
      }
    ]
  },
  {
    "day": 12,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "UNIT 02: A MULTICULTURAL WORLD",
    "subtopic": "Giao lưu, Rào cản & Thích nghi văn hóa",
    "reviewInfo": "Ôn thẻ Day 11 (Mốc +1) và Day 5 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "Indefinite Article: A / An + Singular Countable Noun",
      "note": "Dùng mạo từ 'a/an' trước danh từ số ít đếm được khi nhắc tới lần đầu hoặc chưa xác định",
      "example": "Joining a culture exchange programme helps students overcome a language barrier effectively."
    },
    "vocab": [
      {
        "id": "d12_1",
        "word": "cross-cultural",
        "phonetics": "/ˌkrɒs ˈkʌltʃərəl/",
        "pos": "adj",
        "meaning": "giao lưu văn hóa, xuyên văn hóa",
        "collocation": "cross-cultural communication (giao tiếp liên văn hóa)",
        "example": "The orchestra held a cross-cultural concert where a musician played traditional bamboo flutes alongside the piano."
      },
      {
        "id": "d12_2",
        "word": "language barrier",
        "phonetics": "/ˈlæŋɡwɪdʒ ˌbæriə/",
        "pos": "n.phr",
        "meaning": "rào cản ngôn ngữ",
        "collocation": "overcome language barriers (vượt qua rào cản ngôn ngữ)",
        "example": "Young travelers can break the language barrier by using modern translation software available on the internet."
      },
      {
        "id": "d12_3",
        "word": "culture exchange",
        "phonetics": "/ˈkʌltʃər ɪksˌtʃeɪndʒ/",
        "pos": "n.phr",
        "meaning": "giao lưu văn hóa",
        "collocation": "culture exchange programme (chương trình giao lưu văn hóa)",
        "example": "She applied for a culture exchange programme that will allow her to study and volunteer in the UK next summer."
      },
      {
        "id": "d12_4",
        "word": "unfamiliar",
        "phonetics": "/ˌʌnfəˈmɪliə/",
        "pos": "adj",
        "meaning": "xa lạ, không quen thuộc",
        "collocation": "unfamiliar surroundings (môi trường xa lạ)",
        "example": "Living in an unfamiliar environment can be challenging, but it teaches young people valuable lessons about independence."
      },
      {
        "id": "d12_5",
        "word": "originate",
        "phonetics": "/əˈrɪdʒɪneɪt/",
        "pos": "v",
        "meaning": "bắt nguồn, khởi nguồn",
        "collocation": "originate from (bắt nguồn từ)",
        "example": "Certain folklore dances originated in villages nestled beneath the Alps centuries ago."
      }
    ]
  },
  {
    "day": 13,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "UNIT 02: A MULTICULTURAL WORLD",
    "subtopic": "Lễ hội & Phong tục truyền thống",
    "reviewInfo": "Ôn thẻ Day 12 (Mốc +1) và Day 6 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "Zero Article (∅): ∅ + Plural / Uncountable Nouns in general statements",
      "note": "Không dùng mạo từ (Zero article) trước danh từ số nhiều hoặc không đếm được nói chung",
      "example": "People often uphold traditions and follow local customs when they celebrate festivals."
    },
    "vocab": [
      {
        "id": "d13_1",
        "word": "festivities",
        "phonetics": "/feˈstɪvətiz/",
        "pos": "n.pl",
        "meaning": "các hoạt động lễ hội, không khí lễ hội",
        "collocation": "join in the festivities (hòa mình vào các hoạt động lễ hội)",
        "example": "The lively festivities reached their peak at midnight when people gathered in the central square to admire the full moon."
      },
      {
        "id": "d13_2",
        "word": "origin",
        "phonetics": "/ˈɒrɪdʒɪn/",
        "pos": "n",
        "meaning": "nguồn gốc, xuất xứ",
        "collocation": "historical origin (nguồn gốc lịch sử)",
        "example": "A researcher discovered an ancient manuscript that revealed the true origin of the temple."
      },
      {
        "id": "d13_3",
        "word": "custom",
        "phonetics": "/ˈkʌstəm/",
        "pos": "n",
        "meaning": "phong tục, tập quán",
        "collocation": "follow a local custom (tuân theo phong tục địa phương)",
        "example": "Lighting paper lanterns during the festival is an ancient custom passed down by village elders for generations."
      },
      {
        "id": "d13_4",
        "word": "tradition",
        "phonetics": "/trəˈdɪʃn/",
        "pos": "n",
        "meaning": "truyền thống",
        "collocation": "uphold a family tradition (duy trì truyền thống gia đình)",
        "example": "Weaving colorful mats is a cherished family tradition in several coastal provinces of the Philippines."
      },
      {
        "id": "d13_5",
        "word": "celebrate",
        "phonetics": "/ˈselɪbreɪt/",
        "pos": "v",
        "meaning": "kỷ niệm, ăn mừng, làm lễ kỷ niệm",
        "collocation": "celebrate a festival (ăn mừng một lễ hội)",
        "example": "Citizens throughout the nation celebrate the National Day by hanging red flags outside their homes."
      }
    ]
  },
  {
    "day": 14,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "UNIT 02: A MULTICULTURAL WORLD",
    "subtopic": "Lễ hội hóa trang & Không khí Halloween",
    "reviewInfo": "Ôn thẻ Day 13 (Mốc +1), Day 11 (Mốc +3) và Day 7 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "The + Plural / Special Countries / Specified Context",
      "note": "Dùng 'the' với tên quốc gia số nhiều (The United States, The Netherlands) hoặc danh từ nhắc lại lần 2",
      "example": "Halloween originated in Europe, but the festival is celebrated enthusiastically in the United States."
    },
    "vocab": [
      {
        "id": "d14_1",
        "word": "costume",
        "phonetics": "/ˈkɒstjuːm/",
        "pos": "n",
        "meaning": "trang phục, y phục lễ hội",
        "collocation": "wear traditional costume (mặc trang phục truyền thống)",
        "example": "The performer put on a traditional silk costume before playing the guitar in front of the audience."
      },
      {
        "id": "d14_2",
        "word": "carnival",
        "phonetics": "/ˈkɑːnɪvl/",
        "pos": "n",
        "meaning": "lễ hội hóa trang, ngày hội",
        "collocation": "annual street carnival (lễ hội đường phố thường niên)",
        "example": "Thousands of international tourists visit the carnival every spring to watch colorful parades along the Mediterranean coast."
      },
      {
        "id": "d14_3",
        "word": "trick or treat",
        "phonetics": "/ˌtrɪk ɔː ˈtriːt/",
        "pos": "phrase",
        "meaning": "trò chơi 'cho kẹo hay bị ghẹo' (vào dịp Halloween)",
        "collocation": "go trick or treating (đi chơi trò gõ cửa xin kẹo)",
        "example": "A child carried a plastic basket while playing trick or treat, and the basket was soon filled with chocolate candies."
      },
      {
        "id": "d14_4",
        "word": "pumpkin lantern",
        "phonetics": "/ˌpʌmpkɪn ˈlæntən/",
        "pos": "n.phr",
        "meaning": "đèn lồng quả bí ngô",
        "collocation": "carve a pumpkin lantern (khắc đèn lồng bí ngô)",
        "example": "They placed a carved pumpkin lantern by the gate, where it glowed brightly beneath the dark sky."
      },
      {
        "id": "d14_5",
        "word": "haunted house",
        "phonetics": "/ˌhɔːntɪd ˈhaʊs/",
        "pos": "n.phr",
        "meaning": "ngôi nhà ma ám",
        "collocation": "explore a haunted house (khám phá ngôi nhà ma)",
        "example": "The school club designed a spooky haunted house for Halloween, and the haunted house attracted hundreds of excited students."
      },
      {
        "id": "d14_6",
        "word": "cause for alarm",
        "phonetics": "/ˌkɔːz fər əˈlɑːm/",
        "pos": "idiom",
        "meaning": "lý do để báo động, điều đáng lo ngại",
        "collocation": "give cause for alarm (gây ra sự lo ngại)",
        "example": "Although foreign festivals are becoming popular among teenagers, cultural experts do not consider this trend a cause for alarm."
      }
    ]
  },
  {
    "day": 15,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "UNIT 02: A MULTICULTURAL WORLD",
    "subtopic": "Văn hóa ẩm thực & Tinh hoa ẩm thực",
    "reviewInfo": "Ôn thẻ Day 14 (Mốc +1), Day 12 (Mốc +3) và Day 8 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "The + Musical Instruments / Cultural Specialities: The + N",
      "note": "Dùng 'the' trước các nhạc cụ truyền thống hoặc biểu tượng văn hóa đặc trưng",
      "example": "At the cultural festival, musicians played the Dan Bau while visitors tasted the local cuisine."
    },
    "vocab": [
      {
        "id": "d15_1",
        "word": "cuisine",
        "phonetics": "/kwɪˈziːn/",
        "pos": "n",
        "meaning": "nền ẩm thực, phong cách nấu nướng",
        "collocation": "traditional Vietnamese cuisine (nền ẩm thực truyền thống Việt Nam)",
        "example": "Italian cuisine is immensely popular across the US because people love fresh pasta and handmade pizza."
      },
      {
        "id": "d15_2",
        "word": "speciality",
        "phonetics": "/ˌspeʃiˈæləti/",
        "pos": "n",
        "meaning": "đặc sản, món đặc trưng",
        "collocation": "local speciality (đặc sản địa phương)",
        "example": "Fish and chips is a world-renowned speciality that almost every tourist tries when visiting the UK."
      },
      {
        "id": "d15_3",
        "word": "ingredient",
        "phonetics": "/ɪnˈɡriːdiənt/",
        "pos": "n",
        "meaning": "nguyên liệu, thành phần",
        "collocation": "fresh organic ingredients (nguyên liệu hữu cơ tươi ngon)",
        "example": "The chef selected an exotic ingredient from the market, and the ingredient gave the soup an unforgettable flavor."
      },
      {
        "id": "d15_4",
        "word": "food stall",
        "phonetics": "/ˈfuːd stɔːl/",
        "pos": "n.phr",
        "meaning": "quầy bán đồ ăn, gian hàng ẩm thực",
        "collocation": "street food stall (quầy hàng rong đường phố)",
        "example": "We stopped at a lively food stall near the station, and the food stall served the most delicious dumplings in town."
      },
      {
        "id": "d15_5",
        "word": "tourist attraction",
        "phonetics": "/ˈtʊərɪst əˌtrækʃn/",
        "pos": "n.phr",
        "meaning": "điểm thu hút khách du lịch, điểm tham quan",
        "collocation": "major tourist attraction (điểm du lịch trọng điểm)",
        "example": "The historic windmill village is a top tourist attraction for visitors traveling around the Netherlands."
      }
    ]
  },
  {
    "day": 16,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "UNIT 02: A MULTICULTURAL WORLD",
    "subtopic": "Quà lưu niệm & Trò chơi dân gian",
    "reviewInfo": "Ôn thẻ Day 15 (Mốc +1) và Day 13 (Mốc +3). Day 1 và Day 2 đạt mốc +14.",
    "isReview": false,
    "grammar": {
      "structure": "Zero Article (∅) before Sports & Folk Games: play + ∅ + Game",
      "note": "Không dùng mạo từ trước tên các môn thể thao và trò chơi dân gian",
      "example": "Students love to play tug of war and participate in bamboo dancing during cultural festivals."
    },
    "vocab": [
      {
        "id": "d16_1",
        "word": "souvenir",
        "phonetics": "/ˌsuːvəˈnɪə/",
        "pos": "n",
        "meaning": "đồ lưu niệm",
        "collocation": "buy handcrafted souvenirs (mua quà lưu niệm thủ công)",
        "example": "She purchased a ceramic souvenir at the museum shop, but she accidentally dropped the souvenir on her way home."
      },
      {
        "id": "d16_2",
        "word": "traditional game",
        "phonetics": "/trəˈdɪʃənl ɡeɪm/",
        "pos": "n.phr",
        "meaning": "trò chơi dân gian, trò chơi truyền thống",
        "collocation": "participate in traditional games (tham gia trò chơi dân gian)",
        "example": "Children learned a traditional game in the schoolyard while an instructor played folk melodies on the flute."
      },
      {
        "id": "d16_3",
        "word": "tug of war",
        "phonetics": "/ˌtʌɡ əv ˈwɔː/",
        "pos": "n.phr",
        "meaning": "trò chơi kéo co",
        "collocation": "play tug of war (chơi trò kéo co)",
        "example": "The sports festival concluded with an exciting tug of war between the senior students and the teachers."
      },
      {
        "id": "d16_4",
        "word": "bamboo dancing",
        "phonetics": "/ˌbæmˈbuː ˌdɑːnsɪŋ/",
        "pos": "n.phr",
        "meaning": "điệu nhảy sạp, múa sạp",
        "collocation": "join in bamboo dancing (tham gia múa sạp)",
        "example": "Villagers perform bamboo dancing to welcome visitors who travel across the mountains to attend the spring fair."
      }
    ]
  },
  {
    "day": 17,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "UNIT 02: A MULTICULTURAL WORLD",
    "subtopic": "Xu hướng văn hóa & Giao thoa hiện đại",
    "reviewInfo": "Ôn thẻ Day 16 (Mốc +1) và Day 14 (Mốc +3). Day 3 đạt mốc +14.",
    "isReview": false,
    "grammar": {
      "structure": "S + blend(s) + A + with + B, captivat-ing + O",
      "note": "Mẫu câu miêu tả sự giao thoa văn hóa hiện đại tạo nên sức hút độc đáo",
      "example": "The performance skillfully blends folk music with modern beats, captivating audiences worldwide."
    },
    "vocab": [
      {
        "id": "d17_1",
        "word": "trend",
        "phonetics": "/trend/",
        "pos": "n",
        "meaning": "xu hướng, mốt",
        "collocation": "follow modern trends (theo đuổi xu hướng hiện đại)",
        "example": "Wearing thrifted clothing has become a fashionable trend among high school students in the United States."
      },
      {
        "id": "d17_2",
        "word": "popularity",
        "phonetics": "/ˌpɒpjuˈlærəti/",
        "pos": "n",
        "meaning": "sự phổ biến, sự ưa chuộng",
        "collocation": "gain immense popularity (trở nên vô cùng phổ biến)",
        "example": "The popularity of Asian pop music has expanded rapidly across nations on both sides of the Pacific."
      },
      {
        "id": "d17_3",
        "word": "blend",
        "phonetics": "/blend/",
        "pos": "v",
        "meaning": "pha trộn, kết hợp hài hòa",
        "collocation": "blend seamlessly with (hòa quyện nhịp nhàng với)",
        "example": "Talented musicians often blend modern electronic beats with classical melodies played on the violin."
      },
      {
        "id": "d17_4",
        "word": "captivate",
        "phonetics": "/ˈkæptɪveɪt/",
        "pos": "v",
        "meaning": "cuốn hút, làm say đắm",
        "collocation": "captivate audiences worldwide (làm say đắm khán giả toàn cầu)",
        "example": "The dancer delivered an extraordinary performance that captivated audiences all over the world."
      }
    ]
  },
  {
    "day": 18,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "UNIT 02: A MULTICULTURAL WORLD",
    "subtopic": "Sức ảnh hưởng & Trân trọng văn hóa",
    "reviewInfo": "Ôn thẻ Day 17 (Mốc +1), Day 15 (Mốc +3) và Day 11 (Mốc +7). Day 4 đạt mốc +14.",
    "isReview": false,
    "grammar": {
      "structure": "By + V-ing, S + can + appreciate + N",
      "note": "Cấu trúc nêu phương thức hành động để đạt được sự thấu hiểu và tôn trọng văn hóa",
      "example": "By joining extracurricular activities, students can appreciate cultural diversity and build empathy."
    },
    "vocab": [
      {
        "id": "d18_1",
        "word": "influence",
        "phonetics": "/ˈɪnfluəns/",
        "pos": "n",
        "meaning": "sự ảnh hưởng, sức ảnh hưởng",
        "collocation": "have a profound influence on (có ảnh hưởng sâu sắc tới)",
        "example": "British rock bands exerted a profound influence on pop music across Europe and the UK."
      },
      {
        "id": "d18_2",
        "word": "extracurricular activity",
        "phonetics": "/ˌekstrəkəˈrɪkjələ ækˌtɪvəti/",
        "pos": "n.phr",
        "meaning": "hoạt động ngoại khóa",
        "collocation": "organise extracurricular activities (tổ chức các hoạt động ngoại khóa)",
        "example": "Joining the youth orchestra as an extracurricular activity helped him master the piano."
      },
      {
        "id": "d18_3",
        "word": "appreciate",
        "phonetics": "/əˈpriːʃieɪt/",
        "pos": "v",
        "meaning": "trân trọng, đánh giá cao, thấu hiểu",
        "collocation": "appreciate cultural values (trân trọng các giá trị văn hóa)",
        "example": "Students learn to appreciate diverse cultural values after completing a volunteer project in the Philippines."
      }
    ]
  },
  {
    "day": 19,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "REVIEW SÂU: CỦNG CỐ UNIT 02",
    "subtopic": "Tổng hợp phản xạ từ vựng & Mạo từ Unit 02 (Ẩm thực, Phong tục & Lễ hội)",
    "reviewInfo": "Quét lại toàn bộ các thẻ từ vựng & cấu trúc mạo từ của Unit 02 (Day 11 đến 15).",
    "isReview": true,
    "reviewType": "DEEP_REVIEW",
    "targetDays": [
      11,
      12,
      13,
      14,
      15
    ],
    "reviewNotes": [
      "Ôn tập mạo từ toàn diện: Khi nào dùng 'the' (văn cảnh cụ thể, vật duy nhất, nhạc cụ, quốc gia số nhiều), khi nào dùng 'a/an' (nhắc lần đầu, đếm được), khi nào dùng mạo từ rỗng ∅ (nói chung chung, danh từ số nhiều, môn thể thao/trò chơi).",
      "Cụm từ hội nhập văn hóa: culture shock, cultural diversity, language barrier, culture exchange, cause for alarm.",
      "Từ vựng ẩm thực & phong tục: cuisine, speciality, ingredient, custom, tradition, festivities."
    ],
    "integratedExample": "By joining a culture exchange programme, students can overcome culture shock and appreciate the local cuisine."
  },
  {
    "day": 20,
    "module": "MODULE 2: THẾ GIỚI ĐA VĂN HÓA",
    "unit": "REVIEW LIÊN KẾT (INTERLEAVING): MODULE 2",
    "subtopic": "Tổng ôn đan cài đa văn hóa & Cuộc đời truyền cảm hứng (Unit 01 & Unit 02)",
    "reviewInfo": "Quét đan cài toàn bộ Unit 02 (Day 11 đến Day 18) kết hợp ôn lại Unit 01.",
    "isReview": true,
    "reviewType": "INTERLEAVING_REVIEW",
    "targetDays": [
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18
    ],
    "reviewNotes": [
      "Đan cài trò chơi dân gian & xu hướng văn hóa: bamboo dancing, tug of war, blend, captivate, extracurricular activity, appreciate.",
      "Liên kết Unit 1 & Unit 2: Một nhân vật truyền cảm hứng (Unit 1) cống hiến cho việc bảo tồn và lan tỏa bản sắc văn hóa đa quốc gia (Unit 2).",
      "Luyện tập chuyển đổi câu: Kết hợp thì quá khứ đơn / tiếp diễn với việc sử dụng mạo từ chính xác."
    ],
    "integratedExample": "While she was attending college, she organized an extracurricular festival that blended traditional customs with modern art."
  },
  {
    "day": 21,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Rác thải, Bãi chôn lấp & Sự phân hủy",
    "reviewInfo": "Bắt đầu Module 3! Ôn thẻ Day 18 (Mốc +3) và Day 14 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "It takes + [time] + for + O + to V(bare)",
      "note": "Mẫu câu diễn giải thời gian cần thiết để một chất thải phân hủy trong tự nhiên",
      "example": "It takes hundreds of years for plastic packaging to decompose in a landfill."
    },
    "vocab": [
      {
        "id": "d21_1",
        "word": "waste",
        "phonetics": "/weɪst/",
        "pos": "n",
        "meaning": "rác thải, sự lãng phí",
        "collocation": "reduce household waste (giảm lượng rác thải sinh hoạt)",
        "example": "Our school launched a campaign to cut down on cafeteria food waste, which helps reduce carbon emissions."
      },
      {
        "id": "d21_2",
        "word": "landfill",
        "phonetics": "/ˈlændfɪl/",
        "pos": "n",
        "meaning": "bãi chôn lấp rác",
        "collocation": "send rubbish to landfills (chuyển rác đến các bãi chôn lấp)",
        "example": "Tons of non-biodegradable rubbish are sent to the local landfill every week, which severely pollutes the surrounding soil and water."
      },
      {
        "id": "d21_3",
        "word": "decompose",
        "phonetics": "/ˌdiːkəmˈpəʊz/",
        "pos": "v",
        "meaning": "phân hủy (tự nhiên)",
        "collocation": "take years to decompose (mất nhiều năm để phân hủy)",
        "example": "Single-use plastics take hundreds of years to decompose in nature, which explains why we should stop using them."
      },
      {
        "id": "d21_4",
        "word": "packaging",
        "phonetics": "/ˈpækɪdʒɪŋ/",
        "pos": "n",
        "meaning": "bao bì đóng gói",
        "collocation": "excessive packaging (bao bì đóng gói quá mức)",
        "example": "Many supermarkets have switched to biodegradable packaging, which makes it much easier for customers to go green."
      },
      {
        "id": "d21_5",
        "word": "container",
        "phonetics": "/kənˈteɪnə/",
        "pos": "n",
        "meaning": "hộp đựng, đồ chứa",
        "collocation": "airtight container (hộp đậy kín khí)",
        "example": "Students bring their own reusable containers for lunch, which prevents a lot of plastic trash from ending up in bins."
      }
    ]
  },
  {
    "day": 22,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Bao bì nhựa & Thùng các-tông",
    "reviewInfo": "Ôn thẻ Day 21 (Mốc +1) và Day 15 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "Verbs with Prepositions: S + cut down on / switch to + N",
      "note": "Cụm động từ chỉ hành động cắt giảm chất thải và chuyển sang vật liệu tái chế",
      "example": "Students should cut down on single-use items and switch to recyclable containers."
    },
    "vocab": [
      {
        "id": "d22_1",
        "word": "cardboard box",
        "phonetics": "/ˈkɑːdbɔːd bɒks/",
        "pos": "n",
        "meaning": "thùng các-tông, hộp bìa cứng",
        "collocation": "flatten cardboard boxes (gập phẳng các thùng các-tông)",
        "example": "The shop provides free cardboard boxes for customers to pack groceries, which encourages people to avoid plastic bags."
      },
      {
        "id": "d22_2",
        "word": "single-use",
        "phonetics": "/ˌsɪŋɡl ˈjuːs/",
        "pos": "adj",
        "meaning": "dùng một lần",
        "collocation": "single-use plastic items (các món đồ nhựa dùng một lần)",
        "example": "The local cafeteria decided to ban single-use plastic cutlery, which directly protects marine wildlife from plastic pollution."
      },
      {
        "id": "d22_3",
        "word": "takeaway container",
        "phonetics": "/ˈteɪkəweɪ kənˈteɪnə/",
        "pos": "n",
        "meaning": "hộp đựng thức ăn mang đi",
        "collocation": "reusable takeaway container (hộp đựng đồ ăn mang đi tái sử dụng)",
        "example": "We always wash and reuse plastic takeaway containers at home, which saves money and cuts down on household waste."
      },
      {
        "id": "d22_4",
        "word": "recyclable",
        "phonetics": "/ˌriːˈsaɪkləbl/",
        "pos": "adj",
        "meaning": "có thể tái chế",
        "collocation": "recyclable materials (các vật liệu có thể tái chế)",
        "example": "We make sure that all recyclable materials are placed in the right bin, which makes waste processing much easier for sanitation workers."
      },
      {
        "id": "d22_5",
        "word": "recycle",
        "phonetics": "/ˌriːˈsaɪkl/",
        "pos": "v",
        "meaning": "tái chế",
        "collocation": "recycle plastic bottles (tái chế chai nhựa)",
        "example": "The municipality encourages residents to recycle paper, glass, and metals, which conserves valuable natural resources."
      }
    ]
  },
  {
    "day": 23,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Tái sử dụng & Quy trình làm sạch rác tái chế",
    "reviewInfo": "Ôn thẻ Day 22 (Mốc +1) và Day 16 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "Imperative: Make sure to / Remember to + V(bare) + before + V-ing",
      "note": "Mẫu câu nhắc nhở quy trình phân loại và xử lý rác tại nguồn",
      "example": "Remember to rinse out bottles and sort waste before putting them into the recycling bin."
    },
    "vocab": [
      {
        "id": "d23_1",
        "word": "reuse",
        "phonetics": "/ˌriːˈjuːz/",
        "pos": "v",
        "meaning": "tái sử dụng",
        "collocation": "reuse plastic containers (tái sử dụng hộp nhựa)",
        "example": "My sister loves to reuse old glass jars as pencil holders, which gives discarded items a brand-new purpose."
      },
      {
        "id": "d23_2",
        "word": "reduce",
        "phonetics": "/rɪˈdjuːs/",
        "pos": "v",
        "meaning": "cắt giảm, giảm thiểu",
        "collocation": "reduce carbon emissions (giảm lượng khí thải carbon)",
        "example": "Our family tries to reduce electricity consumption by turning off unused appliances, which lowers our monthly utility bills."
      },
      {
        "id": "d23_3",
        "word": "contaminated",
        "phonetics": "/kənˈtæmɪneɪtɪd/",
        "pos": "adj",
        "meaning": "bị nhiễm bẩn, bị ô nhiễm",
        "collocation": "contaminated waste (rác thải bị nhiễm bẩn)",
        "example": "Someone threw greasy pizza boxes into the paper bin and made the recyclables contaminated, which meant the entire batch had to be thrown into the landfill."
      },
      {
        "id": "d23_4",
        "word": "rinse out",
        "phonetics": "/rɪns aʊt/",
        "pos": "phr.v",
        "meaning": "súc sạch, rửa sạch",
        "collocation": "rinse out bottles thoroughly (súc sạch các chai lọ)",
        "example": "You should always rinse out milk cartons before putting them into recycling bins, which prevents bad smells and bacterial contamination."
      },
      {
        "id": "d23_5",
        "word": "sort waste",
        "phonetics": "/sɔːt weɪst/",
        "pos": "v",
        "meaning": "phân loại rác thải",
        "collocation": "sort waste into categories (phân loại rác theo danh mục)",
        "example": "All students in our school learn how to sort waste properly, which improves the overall recycling efficiency."
      }
    ]
  },
  {
    "day": 24,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Phân loại rác & Thùng thu gom",
    "reviewInfo": "Ôn thẻ Day 23 (Mốc +1), Day 21 (Mốc +3) và Day 17 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "Verbs with Prepositions: S + dispose of / throw away + N",
      "note": "Sử dụng động từ đi với giới từ đúng chuẩn trong chủ đề quản lý chất thải",
      "example": "Do not throw away recyclable items; dispose of them in the designated recycling bin."
    },
    "vocab": [
      {
        "id": "d24_1",
        "word": "separate garbage",
        "phonetics": "/ˈsepəreɪt ˈɡɑːbɪdʒ/",
        "pos": "v",
        "meaning": "phân tách rác",
        "collocation": "separate garbage into bins (phân tách rác vào các thùng riêng)",
        "example": "Every household is required to separate garbage into organic and inorganic bins, which makes waste collection much more effective."
      },
      {
        "id": "d24_2",
        "word": "rubbish bin",
        "phonetics": "/ˈrʌbɪʃ bɪn/",
        "pos": "n",
        "meaning": "thùng rác (thường)",
        "collocation": "throw into the rubbish bin (vứt vào thùng rác thường)",
        "example": "The park authorities placed a new rubbish bin near every bench, which stopped visitors from throwing trash on the grass."
      },
      {
        "id": "d24_3",
        "word": "recycling bin",
        "phonetics": "/ˌriːˈsaɪklɪŋ bɪn/",
        "pos": "n",
        "meaning": "thùng rác tái chế",
        "collocation": "empty the recycling bin (dọn sạch thùng rác tái chế)",
        "example": "Our school placed a bright blue recycling bin on every floor, which encourages students to dispose of plastic bottles responsibly."
      }
    ]
  },
  {
    "day": 25,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Phân hữu cơ & Rác thải gia đình",
    "reviewInfo": "Ôn thẻ Day 24 (Mốc +1), Day 22 (Mốc +3) và Day 18 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "By + V-ing + O, S + can + turn + A + into + B",
      "note": "Mẫu câu phương pháp tái tạo tài nguyên và ủ phân xanh hữu cơ",
      "example": "By building a compost pile, families can turn household waste into rich fertilizer."
    },
    "vocab": [
      {
        "id": "d25_1",
        "word": "compost",
        "phonetics": "/ˈkɒmpɒst/",
        "pos": "n",
        "meaning": "phân trộn, phân hữu cơ",
        "collocation": "organic compost (phân hữu cơ vi sinh)",
        "example": "Gardeners mix homemade compost into the flowerbeds, which enriches the soil naturally without needing harsh chemicals."
      },
      {
        "id": "d25_2",
        "word": "compost pile",
        "phonetics": "/ˈkɒmpɒst paɪl/",
        "pos": "n",
        "meaning": "đống ủ phân hữu cơ",
        "collocation": "build a compost pile (làm một đống ủ phân hữu cơ)",
        "example": "The science club built a compost pile in the backyard, which turns food scraps and dry leaves into rich organic fertilizer."
      },
      {
        "id": "d25_3",
        "word": "household waste",
        "phonetics": "/ˈhaʊshəʊld weɪst/",
        "pos": "n",
        "meaning": "rác thải sinh hoạt gia đình",
        "collocation": "manage household waste (quản lý rác thải sinh hoạt)",
        "example": "Our family sorts organic scraps from general household waste, which makes home composting much cleaner and easier."
      },
      {
        "id": "d25_4",
        "word": "garden waste",
        "phonetics": "/ˈɡɑːdn weɪst/",
        "pos": "n",
        "meaning": "rác vườn (cành cây, lá khô, cỏ xén)",
        "collocation": "collect garden waste (thu gom rác vườn)",
        "example": "We collect lawn clippings and fallen leaves as garden waste, which provides essential brown layers for our compost bin."
      }
    ]
  },
  {
    "day": 26,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Vỏ quả, Thức ăn thừa & Phân bón",
    "reviewInfo": "Ôn thẻ Day 25 (Mốc +1) và Day 23 (Mốc +3). Day 11 và 12 đạt mốc +14.",
    "isReview": false,
    "grammar": {
      "structure": "Instead of + V-ing, S + should + V(bare)",
      "note": "Mẫu câu khuyên giải pháp xanh thay thế thói quen gây hại môi trường",
      "example": "Instead of using chemical fertiliser, gardeners should use compost made from fruit peels and leftovers."
    },
    "vocab": [
      {
        "id": "d26_1",
        "word": "fruit peel",
        "phonetics": "/fruːt piːl/",
        "pos": "n",
        "meaning": "vỏ trái cây, vỏ hoa quả",
        "collocation": "banana and orange fruit peels (vỏ chuối và vỏ cam)",
        "example": "My mother adds orange and apple fruit peels to the compost bin, which provides valuable moisture and nutrients for the compost."
      },
      {
        "id": "d26_2",
        "word": "leftovers",
        "phonetics": "/ˈleftəʊvəz/",
        "pos": "n",
        "meaning": "thức ăn thừa, phần ăn còn lại",
        "collocation": "store food leftovers (bảo quản thức ăn thừa)",
        "example": "We store dinner leftovers in airtight containers for the next day, which prevents delicious food from being thrown away."
      },
      {
        "id": "d26_3",
        "word": "layer",
        "phonetics": "/ˈleɪə/",
        "pos": "n",
        "meaning": "lớp, tầng (vật liệu)",
        "collocation": "alternate layers of green and brown waste (xếp xen kẽ các lớp rác)",
        "example": "You should spread a dry soil layer over wet food scraps, which stops the compost from smelling bad and attracting insects."
      },
      {
        "id": "d26_4",
        "word": "chemical fertiliser",
        "phonetics": "/ˈkemɪkl ˈfɜːtəlaɪzə/",
        "pos": "n",
        "meaning": "phân bón hóa học",
        "collocation": "replace chemical fertiliser (thay thế phân bón hóa học)",
        "example": "Local farmers have stopped relying on chemical fertilisers, which protects the groundwater from toxic agricultural runoff."
      }
    ]
  },
  {
    "day": 27,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Nhận thức môi trường & Lối sống Zero Waste",
    "reviewInfo": "Ôn thẻ Day 26 (Mốc +1) và Day 24 (Mốc +3). Day 13 đạt mốc +14.",
    "isReview": false,
    "grammar": {
      "structure": "Relative Clause referring to a whole sentence: [Clause], which + helps / promotes + N",
      "note": "Mệnh đề quan hệ không xác định với đại từ 'which' thay thế cho toàn bộ ý của mệnh đề đứng trước",
      "example": "Schools raise environmental awareness, which encourages students to pursue a zero waste lifestyle."
    },
    "vocab": [
      {
        "id": "d27_1",
        "word": "zero waste",
        "phonetics": "/ˌzɪərəʊ ˈweɪst/",
        "pos": "n",
        "meaning": "lối sống không rác thải",
        "collocation": "aim for a zero waste lifestyle (hướng tới lối sống không rác thải)",
        "example": "Our family aims for a zero waste lifestyle by composting and avoiding single-use items, which keeps our rubbish output close to zero."
      },
      {
        "id": "d27_2",
        "word": "natural resources",
        "phonetics": "/ˈnætʃrəl rɪˈsɔːsɪz/",
        "pos": "n",
        "meaning": "tài nguyên thiên nhiên",
        "collocation": "conserve natural resources (bảo tồn tài nguyên thiên nhiên)",
        "example": "Industries are finding innovative ways to conserve natural resources, which ensures sustainable development for future generations."
      },
      {
        "id": "d27_3",
        "word": "sustainable",
        "phonetics": "/səˈsteɪnəbl/",
        "pos": "adj",
        "meaning": "bền vững",
        "collocation": "sustainable development (phát triển bền vững)",
        "example": "The city is investing heavily in sustainable public transportation, which drastically cuts down on toxic exhaust fumes."
      },
      {
        "id": "d27_4",
        "word": "environmental awareness",
        "phonetics": "/ɪnˌvaɪrənˈmentl əˈweənəs/",
        "pos": "n",
        "meaning": "nhận thức về môi trường",
        "collocation": "raise environmental awareness (nâng cao nhận thức môi trường)",
        "example": "The youth organisation held workshops to raise environmental awareness, which motivated local residents to clean up the neighbourhood."
      }
    ]
  },
  {
    "day": 28,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Đồ dùng thay thế bền vững",
    "reviewInfo": "Ôn thẻ Day 27 (Mốc +1), Day 25 (Mốc +3) và Day 21 (Mốc +7). Day 14 đạt mốc +14.",
    "isReview": false,
    "grammar": {
      "structure": "[Clause 1], which + allows / enables + someone + to V(bare)",
      "note": "Mệnh đề quan hệ với 'which' chỉ kết quả tích cực của hành động đối với con người",
      "example": "She always brings a reusable bottle, which allows her to avoid single-use plastics completely."
    },
    "vocab": [
      {
        "id": "d28_1",
        "word": "reusable bottle",
        "phonetics": "/ˌriːˈjuːzəbl ˈbɒtl/",
        "pos": "n",
        "meaning": "bình nước dùng nhiều lần",
        "collocation": "carry a reusable bottle (mang theo bình nước tái sử dụng)",
        "example": "Mai carries a reusable bottle filled with drinking water every day, which prevents her from buying plastic bottles from vending machines."
      },
      {
        "id": "d28_2",
        "word": "reusable cup",
        "phonetics": "/ˌriːˈjuːzəbl kʌp/",
        "pos": "n",
        "meaning": "cốc dùng nhiều lần",
        "collocation": "bring a reusable cup (mang theo cốc dùng nhiều lần)",
        "example": "The coffee shop offers discounts to anyone who brings a reusable cup, which discourages customers from taking disposable plastic cups."
      },
      {
        "id": "d28_3",
        "word": "glass jar",
        "phonetics": "/ɡlɑːs dʒɑː/",
        "pos": "n",
        "meaning": "lọ thủy tinh, hũ thủy tinh",
        "collocation": "store food in glass jars (bảo quản thực phẩm trong lọ thủy tinh)",
        "example": "We store dry beans and grains in airtight glass jars, which keeps food fresh without using plastic bags."
      },
      {
        "id": "d28_4",
        "word": "metal straw",
        "phonetics": "/ˈmetl strɔː/",
        "pos": "n",
        "meaning": "ống hút kim loại",
        "collocation": "use washable metal straws (dùng ống hút kim loại có thể rửa sạch)",
        "example": "Nam always carries a washable metal straw in his bag, which allows him to say no to disposable plastic straws."
      }
    ]
  },
  {
    "day": 29,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "REVIEW SÂU: CỦNG CỐ UNIT 03 (PHẦN 1)",
    "subtopic": "Tổng hợp phản xạ: Xử lý rác thải, Tái chế & Phân bón hữu cơ",
    "reviewInfo": "Quét lại toàn bộ các thẻ từ vựng & cấu trúc của Unit 03 Phần 1 (Day 21 đến Day 26).",
    "isReview": true,
    "reviewType": "DEEP_REVIEW",
    "targetDays": [
      21,
      22,
      23,
      24,
      25,
      26
    ],
    "reviewNotes": [
      "Cụm từ then chốt về rác thải: decompose (phân hủy), single-use (dùng một lần), contaminated (nhiễm bẩn), rinse out (súc sạch), sort waste (phân loại rác).",
      "Quy trình ủ phân xanh: compost pile, household waste, garden waste, fruit peel, leftovers, alternate layer, replace chemical fertiliser.",
      "Động từ đi với giới từ: cut down on (cắt giảm), dispose of (vứt bỏ, xử lý), depend on (phụ thuộc vào)."
    ],
    "integratedExample": "Before disposing of plastic containers, remember to rinse out leftovers, which keeps the recyclable materials clean."
  },
  {
    "day": 30,
    "module": "MODULE 3: LỐI SỐNG XANH - RÁC THẢI & TÁI CHẾ",
    "unit": "REVIEW LIÊN KẾT (INTERLEAVING): MODULE 3",
    "subtopic": "Tổng ôn đan cài Thói quen phân loại & Đồ dùng thay thế bền vững",
    "reviewInfo": "Quét đan cài toàn bộ Module 3 (Day 21 đến Day 28). Chuẩn bị bước sang Năng lượng & Bảo tồn.",
    "isReview": true,
    "reviewType": "INTERLEAVING_REVIEW",
    "targetDays": [
      21,
      22,
      23,
      24,
      25,
      26,
      27,
      28
    ],
    "reviewNotes": [
      "Mệnh đề quan hệ thay thế cả câu (Which-clause): [Mệnh đề chính], which + V (chia số ít)... Đây là cấu trúc ngữ pháp trọng điểm của Unit 3!",
      "Bộ từ vựng giải pháp thay thế: reusable bottle, reusable cup, glass jar, metal straw, zero waste, sustainable.",
      "Liên kết đa chủ đề: Lối sống xanh (Unit 3) và các hoạt động ngoại khóa đa văn hóa (Unit 2)."
    ],
    "integratedExample": "Students in our school bring reusable bottles and sort waste daily, which helps protect vital natural resources."
  },
  {
    "day": 31,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Thói quen xanh, Dấu chân Carbon & Tái nạp",
    "reviewInfo": "Bắt đầu Module 4! Ôn thẻ Day 28 (Mốc +3) và Day 24 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "[Action clause], which + results in / contributes to + Noun / V-ing",
      "note": "Dùng 'which contributes to / results in' để chỉ hệ quả trực tiếp đối với môi trường",
      "example": "Many citizens adopt green living, which results in a significant reduction in our carbon footprint."
    },
    "vocab": [
      {
        "id": "d31_1",
        "word": "green living",
        "phonetics": "/ɡriːn ˈlɪvɪŋ/",
        "pos": "n",
        "meaning": "lối sống xanh",
        "collocation": "adopt green living habits (áp dụng các thói quen sống xanh)",
        "example": "Many young people are embracing green living by cutting down on plastic, which contributes greatly to environmental protection."
      },
      {
        "id": "d31_2",
        "word": "eco-friendly",
        "phonetics": "/ˌiːkəʊ ˈfrendli/",
        "pos": "adj",
        "meaning": "thân thiện với môi trường",
        "collocation": "eco-friendly alternatives (các giải pháp thân thiện với môi trường)",
        "example": "The company switched to eco-friendly packaging materials, which attracted more environmentally conscious customers."
      },
      {
        "id": "d31_3",
        "word": "carbon footprint",
        "phonetics": "/ˈkɑːbən ˈfʊtprɪnt/",
        "pos": "n",
        "meaning": "dấu chân carbon (lượng khí thải carbon)",
        "collocation": "reduce personal carbon footprint (cắt giảm dấu chân carbon cá nhân)",
        "example": "We decided to walk or cycle to school to reduce our carbon footprint, which also helps improve our physical health."
      },
      {
        "id": "d31_4",
        "word": "refill",
        "phonetics": "/ˌriːˈfɪl/",
        "pos": "v",
        "meaning": "làm đầy lại, rót đầy lại",
        "collocation": "refill water bottles (làm đầy lại bình nước)",
        "example": "The school installed free water stations so that students can refill their flasks, which significantly reduces single-use plastic waste."
      }
    ]
  },
  {
    "day": 32,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Năng lượng xanh & Tiết kiệm điện",
    "reviewInfo": "Ôn thẻ Day 31 (Mốc +1) và Day 25 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "[Clause 1], which + is a waste of + [Resource]",
      "note": "Mệnh đề quan hệ chỉ nhận xét hoặc phê phán một hành động lãng phí tài nguyên",
      "example": "Leaving fans on in empty classrooms is common, which is a serious waste of electricity."
    },
    "vocab": [
      {
        "id": "d32_1",
        "word": "green energy",
        "phonetics": "/ɡriːn ˈenədʒi/",
        "pos": "n",
        "meaning": "năng lượng xanh",
        "collocation": "invest in green energy (đầu tư vào năng lượng sạch)",
        "example": "The government is heavily promoting green energy from wind and solar power, which helps reduce our dependency on fossil fuels."
      },
      {
        "id": "d32_2",
        "word": "turn off",
        "phonetics": "/tɜːn ɒf/",
        "pos": "phr.v",
        "meaning": "tắt (thiết bị điện)",
        "collocation": "turn off electrical appliances (tắt các thiết bị điện)",
        "example": "We always remember to turn off lights and computer screens before leaving the room, which saves a large amount of electricity."
      },
      {
        "id": "d32_3",
        "word": "waste of electricity",
        "phonetics": "/weɪst əv ɪˌlekˈtrɪsəti/",
        "pos": "n",
        "meaning": "sự lãng phí điện năng",
        "collocation": "prevent a waste of electricity (ngăn chặn sự lãng phí điện năng)",
        "example": "Keeping air conditioners on while all windows are open is a huge waste of electricity, which school regulations strictly forbid."
      }
    ]
  },
  {
    "day": 33,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Ô nhiễm không khí & Khí nhà kính",
    "reviewInfo": "Ôn thẻ Day 32 (Mốc +1) và Day 26 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "When + S + V, S + emit(s) + N, which + warms + the atmosphere",
      "note": "Miêu tả quá trình phát thải khí nhà kính và hệ quả gây hiệu ứng nhà kính",
      "example": "Organic waste rots in landfills, emitting methane, which accelerates global warming."
    },
    "vocab": [
      {
        "id": "d33_1",
        "word": "air pollution",
        "phonetics": "/eə pəˈluːʃn/",
        "pos": "n",
        "meaning": "ô nhiễm không khí",
        "collocation": "combat severe air pollution (chống lại ô nhiễm không khí trầm trọng)",
        "example": "Many commuters switched from motorbikes to electric buses to combat air pollution, which helps improve the city's air quality."
      },
      {
        "id": "d33_2",
        "word": "greenhouse gas",
        "phonetics": "/ˈɡriːnhaʊs ɡæs/",
        "pos": "n",
        "meaning": "khí nhà kính",
        "collocation": "emit greenhouse gases (thải ra các khí nhà kính)",
        "example": "Heavy industries release enormous volumes of greenhouse gases, which speeds up global climate change."
      },
      {
        "id": "d33_3",
        "word": "methane",
        "phonetics": "/ˈmiːθeɪn/",
        "pos": "n",
        "meaning": "khí mê-tan",
        "collocation": "release methane gas (giải phóng khí mê-tan)",
        "example": "Rotting organic food in landfills produces methane, which traps significantly more atmospheric heat than carbon dioxide."
      }
    ]
  },
  {
    "day": 34,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Khí thải CO2, Chất ô nhiễm & Cháy rừng",
    "reviewInfo": "Ôn thẻ Day 33 (Mốc +1), Day 31 (Mốc +3) và Day 27 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "Due to + N, [Clause], which + poses a grave threat to + O",
      "note": "Mẫu câu nguyên nhân - kết quả kết hợp mệnh đề quan hệ chỉ cả câu",
      "example": "Factories release pollutants into rivers, which poses a grave threat to aquatic ecosystems."
    },
    "vocab": [
      {
        "id": "d34_1",
        "word": "carbon dioxide",
        "phonetics": "/ˌkɑːbən daɪˈɒksaɪd/",
        "pos": "n",
        "meaning": "khí cacbonic, khí carbon dioxide (CO2)",
        "collocation": "absorb carbon dioxide (hấp thụ khí carbon dioxide)",
        "example": "Vast green forests absorb massive amounts of carbon dioxide, which plays a crucial role in regulating global temperatures."
      },
      {
        "id": "d34_2",
        "word": "pollutant",
        "phonetics": "/pəˈluːtənt/",
        "pos": "n",
        "meaning": "chất gây ô nhiễm",
        "collocation": "filter harmful pollutants (lọc các chất ô nhiễm độc hại)",
        "example": "The old factory discharged untreated chemical pollutants into the stream, which killed hundreds of river fish."
      },
      {
        "id": "d34_3",
        "word": "wildfire",
        "phonetics": "/ˈwaɪldfaɪə/",
        "pos": "n",
        "meaning": "đám cháy rừng, trận cháy dữ dội ngoài tự nhiên",
        "collocation": "trigger devastating wildfires (gây ra những trận cháy rừng tàn khốc)",
        "example": "Severe summer droughts triggered a catastrophic wildfire across the mountain, which destroyed thousands of hectares of natural woodland."
      }
    ]
  },
  {
    "day": 35,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Xả rác, Biến đổi khí hậu & Động vật hoang dã",
    "reviewInfo": "Ôn thẻ Day 34 (Mốc +1), Day 32 (Mốc +3) và Day 28 (Mốc +7).",
    "isReview": false,
    "grammar": {
      "structure": "If + S + V(present), S + will + V, which + makes + N + Adj",
      "note": "Câu điều kiện loại 1 kết hợp mệnh đề quan hệ chỉ cả sự việc",
      "example": "If people stop dropping litter, rivers will stay clean, which makes habitats safer for wildlife."
    },
    "vocab": [
      {
        "id": "d35_1",
        "word": "litter",
        "phonetics": "/ˈlɪtə/",
        "pos": "n",
        "meaning": "rác rưởi bừa bãi",
        "collocation": "drop litter in public areas (xả rác bừa bãi ở nơi công cộng)",
        "example": "Volunteers spent Sunday morning clearing plastic litter along the canal, which made the residential area much cleaner and safer."
      },
      {
        "id": "d35_2",
        "word": "climate change",
        "phonetics": "/ˈklaɪmət tʃeɪndʒ/",
        "pos": "n",
        "meaning": "biến đổi khí hậu",
        "collocation": "fight against climate change (chống lại biến đổi khí hậu)",
        "example": "Global scientists are working together to find solutions to climate change, which threatens sea levels and coastal communities worldwide."
      },
      {
        "id": "d35_3",
        "word": "harm wild animals",
        "phonetics": "/hɑːm waɪld ˈænɪmlz/",
        "pos": "v",
        "meaning": "gây hại cho động vật hoang dã",
        "collocation": "harm wild animals and their habitats (gây hại cho động vật hoang dã)",
        "example": "Carelessly throwing plastic rings and fishing lines into rivers can harm wild animals, which is why everyone must dispose of trash properly."
      }
    ]
  },
  {
    "day": 36,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Giao thông công cộng & Thiết bị tự động",
    "reviewInfo": "Ôn thẻ Day 35 (Mốc +1) và Day 33 (Mốc +3). Day 21 và 22 đạt mốc +14.",
    "isReview": false,
    "grammar": {
      "structure": "S + be fitted with / install + N, which + prevents / saves + N",
      "note": "Miêu tả ứng dụng công nghệ xanh để tiết kiệm tài nguyên",
      "example": "The school installed sensor taps and automatic lights, which saves water and electricity."
    },
    "vocab": [
      {
        "id": "d36_1",
        "word": "public transport",
        "phonetics": "/ˌpʌblɪk ˈtrænspɔːt/",
        "pos": "n",
        "meaning": "phương tiện giao thông công cộng",
        "collocation": "commute by public transport (đi lại bằng phương tiện công cộng)",
        "example": "More citizens choose to travel by public transport every day, which reduces road traffic congestion and exhaust emissions."
      },
      {
        "id": "d36_2",
        "word": "sensor tap",
        "phonetics": "/ˈsensə tæp/",
        "pos": "n",
        "meaning": "vòi nước cảm ứng",
        "collocation": "install sensor taps (lắp đặt vòi nước cảm ứng)",
        "example": "The school fitted each restroom with an automatic sensor tap, which prevents water from running continuously when students forget to turn it off."
      },
      {
        "id": "d36_3",
        "word": "automatic light",
        "phonetics": "/ˌɔːtəˈmætɪk laɪt/",
        "pos": "n",
        "meaning": "đèn tự động (cảm biến chuyển động)",
        "collocation": "motion-activated automatic light (đèn tự động cảm biến chuyển động)",
        "example": "Hallways were installed with automatic lights that turn off when no one is around, which saves a substantial amount of electrical energy."
      },
      {
        "id": "d36_4",
        "word": "plant pot",
        "phonetics": "/plɑːnt pɒt/",
        "pos": "n",
        "meaning": "chậu trồng cây",
        "collocation": "grow herbs in plant pots (trồng rau thơm trong chậu cây)",
        "example": "Students painted discarded tin cans and turned them into lovely plant pots, which brings greenery into every corner of the classroom."
      }
    ]
  },
  {
    "day": 37,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Máng ăn cho chim & Dọn dẹp cộng đồng",
    "reviewInfo": "Ôn thẻ Day 36 (Mốc +1) và Day 34 (Mốc +3). Day 23 đạt mốc +14.",
    "isReview": false,
    "grammar": {
      "structure": "Verbs with Prepositions: S + participate in / volunteer to + clean up + N",
      "note": "Động từ đi với giới từ trong hoạt động tình nguyện bảo vệ môi trường",
      "example": "Youth volunteers gathered to clean up the polluted beach, which revitalized the coastal scenery."
    },
    "vocab": [
      {
        "id": "d37_1",
        "word": "bird feeder",
        "phonetics": "/bɜːd ˈfiːdə/",
        "pos": "n",
        "meaning": "khay đựng thức ăn cho chim, máng ăn cho chim",
        "collocation": "hang a bird feeder (treo máng ăn cho chim)",
        "example": "Children hung a homemade bird feeder from a sturdy tree branch, which attracts diverse wild birds to the school garden."
      },
      {
        "id": "d37_2",
        "word": "clean up",
        "phonetics": "/kliːn ʌp/",
        "pos": "phr.v",
        "meaning": "dọn dẹp sạch sẽ, tổng vệ sinh",
        "collocation": "clean up the neighbourhood (dọn sạch khu phố)",
        "example": "Youth volunteers organised a weekend event to clean up the local canal, which greatly improved living conditions for nearby residents."
      }
    ]
  },
  {
    "day": 38,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "UNIT 03: GREEN LIVING",
    "subtopic": "Trách nhiệm môi trường & Tầm nhìn tương lai",
    "reviewInfo": "Ôn thẻ Day 37 (Mốc +1), Day 35 (Mốc +3) và Day 31 (Mốc +7). Day 24 đạt mốc +14.",
    "isReview": false,
    "grammar": {
      "structure": "Although + S + V, S + will + benefit + O + in the long run",
      "note": "Cấu trúc tương phản chỉ lợi ích bền vững lâu dài của lối sống xanh",
      "example": "Although green technologies cost more upfront, they save money and energy in the long run."
    },
    "vocab": [
      {
        "id": "d38_1",
        "word": "care about",
        "phonetics": "/keər əˈbaʊt/",
        "pos": "phr.v",
        "meaning": "quan tâm đến, để tâm đến",
        "collocation": "care about the environment (quan tâm đến môi trường)",
        "example": "Most teenagers in our town genuinely care about wildlife conservation, which inspires them to join local eco-friendly campaigns."
      },
      {
        "id": "d38_2",
        "word": "in the long run",
        "phonetics": "/ɪn ðə lɒŋ rʌn/",
        "pos": "idiom",
        "meaning": "về lâu về dài",
        "collocation": "benefit the planet in the long run (có lợi cho hành tinh về lâu dài)",
        "example": "Installing rooftop solar panels cuts electricity expenses significantly in the long run, which benefits both household budgets and the planet."
      }
    ]
  },
  {
    "day": 39,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "REVIEW SÂU: CỦNG CỐ UNIT 03 (PHẦN 2)",
    "subtopic": "Tổng hợp phản xạ: Năng lượng xanh, Ô nhiễm khí quyển & Công nghệ tiết kiệm",
    "reviewInfo": "Quét lại toàn bộ các thẻ từ vựng & cấu trúc của Unit 03 Phần 2 (Day 31 đến Day 38).",
    "isReview": true,
    "reviewType": "DEEP_REVIEW",
    "targetDays": [
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38
    ],
    "reviewNotes": [
      "Ôn tập khí thải & ô nhiễm: greenhouse gas, carbon dioxide, methane, pollutant, air pollution, wildfire, climate change.",
      "Giải pháp công nghệ xanh: public transport, sensor tap, automatic light, turn off, waste of electricity, refill.",
      "Thành ngữ & Cụm động từ: in the long run, care about, clean up, harm wild animals."
    ],
    "integratedExample": "We should install sensor taps and switch to public transport, which reduces air pollution in the long run."
  },
  {
    "day": 40,
    "module": "MODULE 4: LỐI SỐNG XANH - NĂNG LƯỢNG & BẢO TỒN",
    "unit": "REVIEW LIÊN KẾT (INTERLEAVING): MODULE 4",
    "subtopic": "Tổng ôn đan cài Hành động vì Môi trường & Lối sống bền vững",
    "reviewInfo": "Quét đan cài toàn bộ Unit 03 (Day 21 đến Day 38). Chuẩn bị bước vào Module 5 Tổng ôn.",
    "isReview": true,
    "reviewType": "INTERLEAVING_REVIEW",
    "targetDays": [
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38
    ],
    "reviewNotes": [
      "Luyện tập thuần thục cấu trúc: [Mệnh đề hoàn chỉnh], which + V (chia động từ ngôi thứ 3 số ít: which is / which helps / which saves / which reduces).",
      "Cụm động từ có giới từ Unit 3: care about, depend on, contribute to, result in, cut down on, dispose of.",
      "Liên kết đa ngữ cảnh: Một xã hội đa văn hóa (Unit 2) cùng đoàn kết hành động để giải quyết biến đổi khí hậu (Unit 3)."
    ],
    "integratedExample": "Citizens from diverse backgrounds care about environmental protection, which unites communities against climate change."
  },
  {
    "day": 41,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "CHUYÊN ĐỀ 1: PHRASAL VERBS & DẤU ẤN LỊCH SỬ (UNIT 1)",
    "subtopic": "Cụm động từ cố định & Hành động anh hùng",
    "reviewInfo": "Bắt đầu Module 5 Tổng ôn! Ôn thẻ Day 38 (Mốc +3) và Day 34 (Mốc +7). Day 1 đạt mốc +30.",
    "isReview": false,
    "grammar": {
      "structure": "Cleft Sentence for Emphasis: It was + [Element] + that + S + V",
      "note": "Câu chẻ nhấn mạnh nhân vật hoặc hoàn cảnh lịch sử (Cleft sentences with It)",
      "example": "It was by devoting her youth to the resistance war that Dr. Dang Thuy Tram inspired millions."
    },
    "vocab": [
      {
        "id": "d41_1",
        "word": "drop out",
        "phonetics": "/drɒp aʊt/",
        "pos": "phr.v",
        "meaning": "bỏ học, nghỉ học giữa chừng",
        "collocation": "drop out of college (bỏ học đại học giữa chừng)",
        "example": "He dropped out of university because he was already running an innovative computer business."
      },
      {
        "id": "d41_2",
        "word": "pass away",
        "phonetics": "/pɑːs əˈweɪ/",
        "pos": "phr.v",
        "meaning": "qua đời, mất (nói giảm nói tránh)",
        "collocation": "pass away peacefully (thanh thản qua đời)",
        "example": "The beloved artist passed away peacefully in 2020 while his family members were gathering beside him."
      },
      {
        "id": "d41_3",
        "word": "devote to",
        "phonetics": "/dɪˈvəʊt tuː/",
        "pos": "v.phr",
        "meaning": "cống hiến, dành hết tâm huyết cho",
        "collocation": "devote one's life to (cống hiến cả cuộc đời cho)",
        "example": "The scientist devoted her life to research while she was living in a humble laboratory in Paris."
      },
      {
        "id": "d41_4",
        "word": "dedicated to",
        "phonetics": "/ˈdedɪkeɪtɪd tuː/",
        "pos": "adj.phr",
        "meaning": "tận tâm, cống hiến hết mình cho",
        "collocation": "dedicated to helping others (tận tâm giúp đỡ người khác)",
        "example": "He was completely dedicated to medical charity work while other doctors were pursuing lucrative careers."
      },
      {
        "id": "d41_5",
        "word": "carry out attacks",
        "phonetics": "/ˌkæri aʊt əˈtæks/",
        "pos": "v.phr",
        "meaning": "thực hiện các cuộc tấn công, tiến hành đánh úp",
        "collocation": "carry out surprise attacks (tiến hành các cuộc tập kích bất ngờ)",
        "example": "The guerrilla fighters carried out surprise attacks while the colonial army was resting in the garrison."
      }
    ]
  },
  {
    "day": 42,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "CHUYÊN ĐỀ 2: PHẨM CHẤT DANH NHÂN & ĐỘT PHÁ (UNIT 1)",
    "subtopic": "Tầm nhìn chiến lược & Công nghệ đỉnh cao",
    "reviewInfo": "Ôn thẻ Day 41 (Mốc +1) và Day 35 (Mốc +7). Day 2 đạt mốc +30.",
    "isReview": false,
    "grammar": {
      "structure": "Inversion with Negative Adverbials: Not only + did/was + S + V, but + S + also + V",
      "note": "Đảo ngữ với 'Not only... but also...' để nhấn mạnh hai phẩm chất xuất chúng của nhân vật",
      "example": "Not only was he a visionary leader, but he was also admired for his genuine humility."
    },
    "vocab": [
      {
        "id": "d42_1",
        "word": "visionary",
        "phonetics": "/ˈvɪʒnri/",
        "pos": "n",
        "meaning": "người nhìn xa trông rộng, nhà lãnh đạo có tầm nhìn",
        "collocation": "visionary leader (nhà lãnh đạo có tầm nhìn chiến lược)",
        "example": "The visionary was already planning electric transport when most people were still relying on fossil fuels."
      },
      {
        "id": "d42_2",
        "word": "determination",
        "phonetics": "/dɪˌtɜːmɪˈneɪʃn/",
        "pos": "n",
        "meaning": "sự quyết tâm, lòng kiên định",
        "collocation": "unwavering determination (lòng quyết tâm kiên định)",
        "example": "She showed incredible determination while she was training for the marathon through harsh winter storms."
      },
      {
        "id": "d42_3",
        "word": "ambitious",
        "phonetics": "/æmˈbɪʃəs/",
        "pos": "adj",
        "meaning": "có nhiều hoài bão, giàu tham vọng",
        "collocation": "ambitious goals (mục tiêu đầy hoài bão)",
        "example": "The ambitious student was studying day and night while his peers were playing video games."
      },
      {
        "id": "d42_4",
        "word": "military genius",
        "phonetics": "/ˈmɪlətri ˈdʒiːniəs/",
        "pos": "n.phr",
        "meaning": "thiên tài quân sự",
        "collocation": "strategic military genius (thiên tài quân sự lỗi lạc)",
        "example": "The military genius changed his battle tactics while the enemy was preparing for a frontal assault."
      },
      {
        "id": "d42_5",
        "word": "cutting-edge technology",
        "phonetics": "/ˌkʌtɪŋ edʒ tekˈnɒlədʒi/",
        "pos": "n.phr",
        "meaning": "công nghệ tiên tiến nhất, công nghệ đỉnh cao",
        "collocation": "apply cutting-edge technology (ứng dụng công nghệ tối tân)",
        "example": "The startup was adopting cutting-edge technology when other competitors were still relying on outdated equipment."
      }
    ]
  },
  {
    "day": 43,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "CHUYÊN ĐỀ 3: THÀNH NGỮ & CẢM XÚC ĐỈNH CAO (UNITS 1 & 2)",
    "subtopic": "Thành ngữ chỉ niềm vui & Cú sốc văn hóa",
    "reviewInfo": "Ôn thẻ Day 42 (Mốc +1) và Day 36 (Mốc +7). Day 3 đạt mốc +30.",
    "isReview": false,
    "grammar": {
      "structure": "Participle Clause: Having + V3/ed + O, S + felt / was + [Idiom]",
      "note": "Rút gọn mệnh đề trạng ngữ bằng phân từ hoàn thành (Perfect Participle) chỉ hành động xảy ra trước",
      "example": "Having achieved an impressive score on the exam, the ambitious student was over the moon."
    },
    "vocab": [
      {
        "id": "d43_1",
        "word": "on top of the world",
        "phonetics": "/ɒn tɒp əv ðə wɜːld/",
        "pos": "idiom",
        "meaning": "vô cùng hạnh phúc, vui sướng ngất ngây",
        "collocation": "feel on top of the world (cảm thấy hạnh phúc tột cùng)",
        "example": "She was feeling on top of the world when the headmaster announced her first-place victory."
      },
      {
        "id": "d43_2",
        "word": "on cloud nine",
        "phonetics": "/ɒn klaʊd naɪn/",
        "pos": "idiom",
        "meaning": "lâng lâng sung sướng, ngập tràn hạnh phúc",
        "collocation": "be on cloud nine (đang ngập tràn niềm vui)",
        "example": "He was on cloud nine for days while congratulations were pouring in from his relatives and friends."
      },
      {
        "id": "d43_3",
        "word": "over the moon",
        "phonetics": "/ˈəʊvə ðə muːn/",
        "pos": "idiom",
        "meaning": "sướng rơn, vui mừng khôn xiết",
        "collocation": "be over the moon (vui mừng hết cỡ)",
        "example": "The young writer was over the moon when the publisher agreed to print her debut novel."
      },
      {
        "id": "d43_4",
        "word": "cause for alarm",
        "phonetics": "/ˌkɔːz fər əˈlɑːm/",
        "pos": "idiom",
        "meaning": "lý do để báo động, điều đáng lo ngại",
        "collocation": "give cause for alarm (gây ra sự lo ngại)",
        "example": "Although foreign festivals are becoming popular among teenagers, cultural experts do not consider this trend a cause for alarm."
      },
      {
        "id": "d43_5",
        "word": "culture shock",
        "phonetics": "/ˈkʌltʃə ʃɒk/",
        "pos": "n.phr",
        "meaning": "cú sốc văn hóa",
        "collocation": "experience culture shock (trải qua cú sốc văn hóa)",
        "example": "Many exchange students experience culture shock when they first arrive in the US to attend university."
      }
    ]
  },
  {
    "day": 44,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "CHUYÊN ĐỀ 4: BẢN SẮC & GIAO THOA TOÀN CẦU (UNIT 2)",
    "subtopic": "Hội nhập quốc tế & Xóa bỏ rào cản",
    "reviewInfo": "Ôn thẻ Day 43 (Mốc +1), Day 41 (Mốc +3) và Day 37 (Mốc +7). Day 4 đạt mốc +30.",
    "isReview": false,
    "grammar": {
      "structure": "Double Comparative: The more + S + V, the more + S + V",
      "note": "So sánh kép (The more... the more...) diễn đạt sự phát triển tương quan",
      "example": "The more people understand cultural diversity, the more effectively they break down language barriers."
    },
    "vocab": [
      {
        "id": "d44_1",
        "word": "cultural diversity",
        "phonetics": "/ˌkʌltʃərəl daɪˈvɜːsəti/",
        "pos": "n.phr",
        "meaning": "sự đa dạng văn hóa",
        "collocation": "celebrate cultural diversity (tôn vinh sự đa dạng văn hóa)",
        "example": "The United States is home to people from hundreds of ethnic backgrounds who contribute to the cultural diversity of the nation."
      },
      {
        "id": "d44_2",
        "word": "globalisation",
        "phonetics": "/ˌɡləʊbəlaɪˈzeɪʃn/",
        "pos": "n",
        "meaning": "sự toàn cầu hóa",
        "collocation": "the impact of globalisation (tác động của toàn cầu hóa)",
        "example": "Globalisation allows artists in the UK to exchange creative ideas seamlessly with musicians across the Atlantic."
      },
      {
        "id": "d44_3",
        "word": "multicultural",
        "phonetics": "/ˌmʌltiˈkʌltʃərəl/",
        "pos": "adj",
        "meaning": "đa văn hóa",
        "collocation": "multicultural society (xã hội đa văn hóa)",
        "example": "London has grown into a vibrant multicultural metropolis where citizens speak over three hundred languages from around the world."
      },
      {
        "id": "d44_4",
        "word": "cross-cultural",
        "phonetics": "/ˌkrɒs ˈkʌltʃərəl/",
        "pos": "adj",
        "meaning": "giao lưu văn hóa, xuyên văn hóa",
        "collocation": "cross-cultural communication (giao tiếp liên văn hóa)",
        "example": "The orchestra held a cross-cultural concert where a musician played traditional bamboo flutes alongside the piano."
      },
      {
        "id": "d44_5",
        "word": "language barrier",
        "phonetics": "/ˈlæŋɡwɪdʒ ˌbæriə/",
        "pos": "n.phr",
        "meaning": "rào cản ngôn ngữ",
        "collocation": "overcome language barriers (vượt qua rào cản ngôn ngữ)",
        "example": "Young travelers can break the language barrier by using modern translation software available on the internet."
      }
    ]
  },
  {
    "day": 45,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "CHUYÊN ĐỀ 5: TINH HOA ẨM THỰC & BẢO TỒN VĂN HÓA (UNIT 2)",
    "subtopic": "Ẩm thực truyền thống, Pha trộn hiện đại & Trân trọng di sản",
    "reviewInfo": "Ôn thẻ Day 44 (Mốc +1), Day 42 (Mốc +3) và Day 38 (Mốc +7). Day 5 đạt mốc +30.",
    "isReview": false,
    "grammar": {
      "structure": "No sooner had + S + V3/ed + than + S + V-ed",
      "note": "Đảo ngữ với 'No sooner... than...' (Vừa mới... thì đã...) trong diễn đạt nghệ thuật",
      "example": "No sooner had the folk music begun than the traditional dance captivated the entire audience."
    },
    "vocab": [
      {
        "id": "d45_1",
        "word": "cuisine",
        "phonetics": "/kwɪˈziːn/",
        "pos": "n",
        "meaning": "nền ẩm thực, phong cách nấu nướng",
        "collocation": "traditional Vietnamese cuisine (nền ẩm thực truyền thống Việt Nam)",
        "example": "Italian cuisine is immensely popular across the US because people love fresh pasta and handmade pizza."
      },
      {
        "id": "d45_2",
        "word": "speciality",
        "phonetics": "/ˌspeʃiˈæləti/",
        "pos": "n",
        "meaning": "đặc sản, món đặc trưng",
        "collocation": "local speciality (đặc sản địa phương)",
        "example": "Fish and chips is a world-renowned speciality that almost every tourist tries when visiting the UK."
      },
      {
        "id": "d45_3",
        "word": "blend",
        "phonetics": "/blend/",
        "pos": "v",
        "meaning": "pha trộn, kết hợp hài hòa",
        "collocation": "blend seamlessly with (hòa quyện nhịp nhàng với)",
        "example": "Talented musicians often blend modern electronic beats with classical melodies played on the violin."
      },
      {
        "id": "d45_4",
        "word": "captivate",
        "phonetics": "/ˈkæptɪveɪt/",
        "pos": "v",
        "meaning": "cuốn hút, làm say đắm",
        "collocation": "captivate audiences worldwide (làm say đắm khán giả toàn cầu)",
        "example": "The dancer delivered an extraordinary performance that captivated audiences all over the world."
      },
      {
        "id": "d45_5",
        "word": "appreciate",
        "phonetics": "/əˈpriːʃieɪt/",
        "pos": "v",
        "meaning": "trân trọng, đánh giá cao, thấu hiểu",
        "collocation": "appreciate cultural values (trân trọng các giá trị văn hóa)",
        "example": "Students learn to appreciate diverse cultural values after completing a volunteer project in the Philippines."
      }
    ]
  },
  {
    "day": 46,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "CHUYÊN ĐỀ 6: XỬ LÝ CHẤT THẢI & KINH TẾ TUẦN HOÀN (UNIT 3)",
    "subtopic": "Phân loại rác, Khử bẩn & Phân bón vi sinh",
    "reviewInfo": "Ôn thẻ Day 45 (Mốc +1) và Day 43 (Mốc +3). Day 6 đạt mốc +30.",
    "isReview": false,
    "grammar": {
      "structure": "Had it not been for + Noun, S + would/could (not) + have + V3/ed",
      "note": "Đảo ngữ câu điều kiện loại 3 chỉ giả định trái ngược với quá khứ",
      "example": "Had citizens not separated waste carefully, recyclable materials would have been contaminated."
    },
    "vocab": [
      {
        "id": "d46_1",
        "word": "decompose",
        "phonetics": "/ˌdiːkəmˈpəʊz/",
        "pos": "v",
        "meaning": "phân hủy (tự nhiên)",
        "collocation": "take years to decompose (mất nhiều năm để phân hủy)",
        "example": "Single-use plastics take hundreds of years to decompose in nature, which explains why we should stop using them."
      },
      {
        "id": "d46_2",
        "word": "single-use",
        "phonetics": "/ˌsɪŋɡl ˈjuːs/",
        "pos": "adj",
        "meaning": "dùng một lần",
        "collocation": "single-use plastic items (các món đồ nhựa dùng một lần)",
        "example": "The local cafeteria decided to ban single-use plastic cutlery, which directly protects marine wildlife from plastic pollution."
      },
      {
        "id": "d46_3",
        "word": "contaminated",
        "phonetics": "/kənˈtæmɪneɪtɪd/",
        "pos": "adj",
        "meaning": "bị nhiễm bẩn, bị ô nhiễm",
        "collocation": "contaminated waste (rác thải bị nhiễm bẩn)",
        "example": "Someone threw greasy pizza boxes into the paper bin and made the recyclables contaminated, which meant the entire batch had to be thrown into the landfill."
      },
      {
        "id": "d46_4",
        "word": "rinse out",
        "phonetics": "/rɪns aʊt/",
        "pos": "phr.v",
        "meaning": "súc sạch, rửa sạch",
        "collocation": "rinse out bottles thoroughly (súc sạch các chai lọ)",
        "example": "You should always rinse out milk cartons before putting them into recycling bins, which prevents bad smells and bacterial contamination."
      },
      {
        "id": "d46_5",
        "word": "compost pile",
        "phonetics": "/ˈkɒmpɒst paɪl/",
        "pos": "n",
        "meaning": "đống ủ phân hữu cơ",
        "collocation": "build a compost pile (làm một đống ủ phân hữu cơ)",
        "example": "The science club built a compost pile in the backyard, which turns food scraps and dry leaves into rich organic fertilizer."
      }
    ]
  },
  {
    "day": 47,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "CHUYÊN ĐỀ 7: NĂNG LƯỢNG TÁI TẠO & HÀNH TÍNH XANH (UNIT 3)",
    "subtopic": "Cắt giảm dấu chân Carbon & Lối sống bền vững",
    "reviewInfo": "Ôn thẻ Day 46 (Mốc +1) và Day 44 (Mốc +3). Day 7 đạt mốc +30.",
    "isReview": false,
    "grammar": {
      "structure": "Only by + V-ing, can + S + V(bare)",
      "note": "Đảo ngữ với 'Only by' để nhấn mạnh giải pháp duy nhất giải quyết khủng hoảng môi trường",
      "example": "Only by adopting green living, can we reduce our carbon footprint and build a sustainable future."
    },
    "vocab": [
      {
        "id": "d47_1",
        "word": "green living",
        "phonetics": "/ɡriːn ˈlɪvɪŋ/",
        "pos": "n",
        "meaning": "lối sống xanh",
        "collocation": "adopt green living habits (áp dụng các thói quen sống xanh)",
        "example": "Many young people are embracing green living by cutting down on plastic, which contributes greatly to environmental protection."
      },
      {
        "id": "d47_2",
        "word": "carbon footprint",
        "phonetics": "/ˈkɑːbən ˈfʊtprɪnt/",
        "pos": "n",
        "meaning": "dấu chân carbon (lượng khí thải carbon)",
        "collocation": "reduce personal carbon footprint (cắt giảm dấu chân carbon cá nhân)",
        "example": "We decided to walk or cycle to school to reduce our carbon footprint, which also helps improve our physical health."
      },
      {
        "id": "d47_3",
        "word": "zero waste",
        "phonetics": "/ˌzɪərəʊ ˈweɪst/",
        "pos": "n",
        "meaning": "lối sống không rác thải",
        "collocation": "aim for a zero waste lifestyle (hướng tới lối sống không rác thải)",
        "example": "Our family aims for a zero waste lifestyle by composting and avoiding single-use items, which keeps our rubbish output close to zero."
      },
      {
        "id": "d47_4",
        "word": "sustainable",
        "phonetics": "/səˈsteɪnəbl/",
        "pos": "adj",
        "meaning": "bền vững",
        "collocation": "sustainable development (phát triển bền vững)",
        "example": "The city is investing heavily in sustainable public transportation, which drastically cuts down on toxic exhaust fumes."
      },
      {
        "id": "d47_5",
        "word": "green energy",
        "phonetics": "/ɡriːn ˈenədʒi/",
        "pos": "n",
        "meaning": "năng lượng xanh",
        "collocation": "invest in green energy (đầu tư vào năng lượng sạch)",
        "example": "The government is heavily promoting green energy from wind and solar power, which helps reduce our dependency on fossil fuels."
      }
    ]
  },
  {
    "day": 48,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "CHUYÊN ĐỀ 8: BIẾN ĐỔI KHÍ HẬU & CHIẾN LƯỢC TƯƠNG LAI (UNIT 3)",
    "subtopic": "Kiềm chế khí nhà kính & Lợi ích bền vững lâu dài",
    "reviewInfo": "Ôn thẻ Day 47 (Mốc +1), Day 45 (Mốc +3) và Day 41 (Mốc +7). Day 8 đạt mốc +30.",
    "isReview": false,
    "grammar": {
      "structure": "[Clause 1], which + will + undoubtedly + benefit + O + in the long run",
      "note": "Mệnh đề quan hệ chỉ nhận định mang tầm chiến lược lâu dài",
      "example": "Governments invest in renewable energy, which will undoubtedly mitigate climate change in the long run."
    },
    "vocab": [
      {
        "id": "d48_1",
        "word": "greenhouse gas",
        "phonetics": "/ˈɡriːnhaʊs ɡæs/",
        "pos": "n",
        "meaning": "khí nhà kính",
        "collocation": "emit greenhouse gases (thải ra các khí nhà kính)",
        "example": "Heavy industries release enormous volumes of greenhouse gases, which speeds up global climate change."
      },
      {
        "id": "d48_2",
        "word": "pollutant",
        "phonetics": "/pəˈluːtənt/",
        "pos": "n",
        "meaning": "chất gây ô nhiễm",
        "collocation": "filter harmful pollutants (lọc các chất ô nhiễm độc hại)",
        "example": "The old factory discharged untreated chemical pollutants into the stream, which killed hundreds of river fish."
      },
      {
        "id": "d48_3",
        "word": "climate change",
        "phonetics": "/ˈklaɪmət tʃeɪndʒ/",
        "pos": "n",
        "meaning": "biến đổi khí hậu",
        "collocation": "fight against climate change (chống lại biến đổi khí hậu)",
        "example": "Global scientists are working together to find solutions to climate change, which threatens sea levels and coastal communities worldwide."
      },
      {
        "id": "d48_4",
        "word": "in the long run",
        "phonetics": "/ɪn ðə lɒŋ rʌn/",
        "pos": "idiom",
        "meaning": "về lâu về dài",
        "collocation": "benefit the planet in the long run (có lợi cho hành tinh về lâu dài)",
        "example": "Installing rooftop solar panels cuts electricity expenses significantly in the long run, which benefits both household budgets and the planet."
      },
      {
        "id": "d48_5",
        "word": "sensor tap",
        "phonetics": "/ˈsensə tæp/",
        "pos": "n",
        "meaning": "vòi nước cảm ứng",
        "collocation": "install sensor taps (lắp đặt vòi nước cảm ứng)",
        "example": "The school fitted each restroom with an automatic sensor tap, which prevents water from running continuously when students forget to turn it off."
      }
    ]
  },
  {
    "day": 49,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "REVIEW SÂU: TỔNG ÔN TRỌNG ĐIỂM UNITS 1 - 3",
    "subtopic": "Chinh phục cấu trúc ngữ pháp nâng cao & Bứt phá điểm thi THPT Quốc Gia",
    "reviewInfo": "Quét lại toàn bộ các cấu trúc đảo ngữ, câu chẻ, mệnh đề phân từ của Module 5.",
    "isReview": true,
    "reviewType": "DEEP_REVIEW",
    "targetDays": [
      41,
      42,
      43,
      44,
      45,
      46,
      47,
      48
    ],
    "reviewNotes": [
      "Cấu trúc đảo ngữ đỉnh cao trong đề thi THPT: Not only... but also..., Only by..., No sooner... than..., Inversion with Negative Adverbials.",
      "Câu chẻ nhấn mạnh (Cleft sentences: It is/was... that...) và Mệnh đề phân từ hoàn thành (Having + V3/ed).",
      "Tổng hợp các thành ngữ và cụm từ đắt giá của cả 3 Unit: on top of the world, on cloud nine, over the moon, cause for alarm, in the long run."
    ],
    "integratedExample": "Not only did the visionary leader inspire youth to embrace cultural diversity, but he also championed sustainable green living."
  },
  {
    "day": 50,
    "module": "MODULE 5: TỔNG ÔN ĐỈNH CAO GLOBAL SUCCESS 12",
    "unit": "FINAL REVIEW: THE GRAND SPRINT - BỨT PHÁ 50 NGÀY GLOBAL SUCCESS 12",
    "subtopic": "Tổng duyệt phản xạ toàn diện 50 Ngày - Tự tin làm chủ Tiếng Anh 12",
    "reviewInfo": "Đích đến vinh quang! Đã làm chủ toàn bộ từ vựng, ngữ pháp và cụm từ của Global Success 12.",
    "isReview": true,
    "reviewType": "GRAND_REVIEW",
    "targetDays": [
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      11,
      12,
      13,
      14,
      15,
      16,
      17,
      18,
      21,
      22,
      23,
      24,
      25,
      26,
      27,
      28,
      31,
      32,
      33,
      34,
      35,
      36,
      37,
      38,
      41,
      42,
      43,
      44,
      45,
      46,
      47,
      48
    ],
    "reviewNotes": [
      "Chúc mừng bạn đã chinh phục trọn vẹn Lộ trình 50 Ngày Thử Thách Spaced Repetition của Global Success 12!",
      "Bạn đã làm chủ 141 từ vựng cốt lõi & mở rộng, 40 cấu trúc ngữ pháp chuẩn sách giáo khoa và các dạng biến đổi nâng cao phục vụ kỳ thi Tốt Nghiệp THPT.",
      "Hãy tiếp tục luyện tập hàng ngày với 5 Hộp Leitner để duy trì khả năng phản xạ từ vựng và cấu trúc vĩnh viễn!"
    ],
    "integratedExample": "Throughout the 50-day challenge, learners mastered key vocabulary and grammar of Global Success 12, which paves the way for top exam scores."
  }
];

// Hỗ trợ tương thích trình duyệt và Node.js
const IELTS_50_DAYS_DATA = GS12_50_DAYS_DATA;

if (typeof window !== 'undefined') {
  window.GS12_50_DAYS_DATA = GS12_50_DAYS_DATA;
  window.IELTS_50_DAYS_DATA = GS12_50_DAYS_DATA;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { GS12_50_DAYS_DATA, IELTS_50_DAYS_DATA };
}
