import re
import pandas as pd
import os

# 1. Provide the file path to your existing CSV
existing_file_path = "/Users/xylu/Desktop/Data/Database_Abort/Complete_LER_Event_Data_Analysis_Summary.xlsx"

# 2. Paste the NEW raw text inside the triple quotes
new_raw_text = """
original json file on abort database

Time	Abort Ring	Origin Ring	Source	I_LER
[mA]	I_HER
[mA]	Nb	Dia(L)
[mRad/s]	Dia(H)
[mRad/s]	Diamond
abort	LossMon
(L)	LossMon
(H)	BOR/BCM
(L)	BOR/BCM
(H)	BT orbit	Belle2 CLAWS	LMtiming
(L)	LMtiming
(H)	OptFbr
(L)	OptFbr
(H)	AbtBPM
(L)	AbtBPM
(L)	AbtBPM
(L)	AbtBPM
(H)	AbtBPM
(H)	AbtBPM
(H)	Clearing
Electrode	Pressure
burst	Category	Tags	Comment
2026-03-12 09:09:41
Zlog json TimeStamp grp
edit
Both
LER
D7 Master
+ Low THR VXD diamond
+ High THR VXD diamond
+(CLAWS D06V1)
1596
1118
2346
1279
100

1345 mRad
																	
D05_L22A
SBL
BeamLoss
Physics run
Pressure burst
QCS quench
SBL
2026-03-12 02:01:54
Zlog json TimeStamp grp
edit
Both
LER
Belle2 CLAWS
+ Low THR VXD diamond
1646
1138
2346
253
138

23.5 mRad
																	
BeamLoss
BeamLoss
Physics run
2026-03-12 00:15:04
Zlog json TimeStamp grp
edit
Both
LER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1645
1138
2346
1653
122

161.7 mRad
																	
BeamLoss
BeamLoss
Physics run
2026-03-11 22:51:40
Zlog json TimeStamp grp
edit
LER
LER
D7 Master
+(CLAWS D06V1)
1645
1078
2346
275
105
																	
BeamLoss
BeamLoss
Physics run
2026-03-11 12:18:40
Zlog json TimeStamp grp
edit
LER
LER
RF D08A
997
724
2346
101
159
																	
RF
Physics run
RF
D08A CAV#2 C-damper power
2026-03-11 11:36:49
Zlog json TimeStamp grp
edit
LER
LER
RF D08A
1223
867
2346
211
103
																	
RF
Physics run
RF
D08ステーションのWATER I/L
2026-03-10 23:31:02
Zlog json TimeStamp grp
edit
LER
LER
RF D05F
1595
1117
2346
267
149
																	
RF
Physics run
RF
2026-03-10 20:39:12
Zlog json TimeStamp grp
edit
Both
LER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1595
1058
2346
2048
17

268.2 mRad
																	

D05_L25
SBL
BeamLoss
Physics run
Pressure burst
SBL
2026-03-09 13:45:56
Zlog json TimeStamp grp
edit
LER
LER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1595
998
2346
2593
67

566.1 mRad
																	

D11_L14
GV(D11_L02)
SBL
BeamLoss
Physics run
SBL
D11_L14真空はねは90秒くらい前なので多分無関係（照井）
2026-03-08 18:43:06
Zlog json TimeStamp grp
edit
Both
LER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1497
1117
2346
576
76

191.9 mRad
																	
BeamLoss
BeamLoss
Physics run
2026-03-06 15:00:01
Zlog json TimeStamp grp
edit
LER
LER
RF D05A
898
718
2346
68
42
																	
RF
Physics run
RF
detune空洞におけるビーム励起でのRF I/Lの発報
2026-03-06 08:34:09
Zlog json TimeStamp grp
edit
LER
LER
RF D05D
0
0
2346
0
0
																	
RF
No beam
RF
2026-03-04 06:25:55
Zlog json TimeStamp grp
edit
LER
LER
RF D05E
0
68
2346
0
0
																	
RF
No beam
前日のRF D05EF-KPS CROWBAR WORKの調査（吉本）
2026-03-04 03:55:14
Zlog json TimeStamp grp
edit
LER
LER
RF D07E
0
157
2346
0
0
																	
RF
No beam
LLRF作業のため（BT Mag電源雨漏りトラブル中でビームなし）
2026-03-04 02:39:25
Zlog json TimeStamp grp
edit
LER
LER
RF D05D
197
405
2346
4
2
																	
RF
Physics run
RF
D05D空洞breakdown (RF D05D CAV-C DAMPER POWER I/L)
(BT Mag電源トラブルで蓄積電流decay中）
2026-03-03 13:52:30
Zlog json TimeStamp grp
edit
Both
LER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
997
798
2346
584
10

160.9 mRad
																	
BeamLoss
BeamLoss
Physics run
2026-03-03 08:39:52
Zlog json TimeStamp grp
edit
Both
LER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
998
798
2346
2183
24

1418.2 mRad
																	
D10_L07
QW3NLP
SBL
Pressure burst
QCS quench
2026-03-03 00:11:10
Zlog json TimeStamp grp
edit
Both
LER
RF D05F
998
798
2346
130
33
																	
RF
Physics run
RF
RF D05EF-KPS CROWBAR WORK (D04も伴連れで両リングアボート）
2026-03-02 21:12:58
Zlog json TimeStamp grp
edit
LER
LER
Loss Monitor D7-1
+ Low THR VXD diamond
+ High THR VXD diamond
1199
0
2346
2548
1

1378.2 mRad
																	
D05_L22A
SBL
BeamLoss
Physics run
Pressure burst
QCS quench
SBL
HERのPlotは１分前のHER beam loss abort↓
2026-03-02 20:40:25
Zlog json TimeStamp grp
edit
Both
LER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1339
1044
2346
2616
52

387.2 mRad
																	
BeamLoss
BeamLoss
Physics run

"""

# Extract existing data
df_existing = pd.read_csv(existing_file_path)

# Parse the new events
date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
events_raw = date_pattern.split(new_raw_text)[1:] 

new_data = []
for i in range(0, len(events_raw), 2):
    time = events_raw[i].strip()
    lines = [line.strip() for line in events_raw[i+1].split('\n') if line.strip() != '']
    
    if len(lines) < 9:
        continue

    abort_ring = lines[1]
    origin_ring = lines[2]

    source_lines = [lines[3]]
    idx = 4
    while idx < len(lines) and not lines[idx].isdigit():
        source_lines.append(lines[idx])
        idx += 1
    source = ' '.join(source_lines)

    try:
        i_ler, i_her, nb, dia_l, dia_h = lines[idx:idx+5]
        idx += 5
    except ValueError:
        continue

    diamond_abort = ""
    category = ""
    tags = []
    comments = []

    known_categories = {'BeamLoss', 'Tuning', 'RF', 'EQ', 'Injection', 'SBL', 'Others', 'MAG'}
    known_tags = {'Physics run', 'No beam', 'Injection', 'Tuning', 'BeamLoss', 'RF', 'QCS quench', 'Pressure burst', 'Study', 'EQ'}

    for line in lines[idx:]:
        if line.endswith('mRad'):
            diamond_abort = line
        elif line in known_categories and not category:
            category = line
        elif line in known_tags or line in known_categories:
            tags.append(line)
        else:
            comments.append(line)

    new_data.append({
        'Time': time,
        'Abort Ring': abort_ring,
        'Origin Ring': origin_ring,
        'Source': source,
        'I_LER [mA]': i_ler,
        'I_HER [mA]': i_her,
        'Nb': nb,
        'Dia(L) [mRad/s]': dia_l,
        'Dia(H) [mRad/s]': dia_h,
        'Diamond Abort [mRad]': diamond_abort,
        'Category': category,
        'Tags': ', '.join(sorted(set(tags))),
        'Comment / Other Events': ' | '.join(comments)
    })

# Convert new data to DataFrame, append, and export
df_new = pd.DataFrame(new_data)
df_combined = pd.concat([df_existing, df_new], ignore_index=True)

# Export to a clean Excel file
output_filename = 'Updated_LER_Event_Data_Analysis.xlsx'
df_combined.to_excel(output_filename, index=False)
print(f"Successfully appended {len(df_new)} new events and saved to {output_filename}")