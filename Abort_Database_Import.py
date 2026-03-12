import re
import pandas as pd

# 1. Paste your ENTIRE raw text inside the triple quotes below
raw_text = """
New Abort Database webpage (under construction)==>here
[Abort manual by Ikeda-san] [ RF abort verification ] [ SBL verification ] [LINAC orbit of injection aborts]
[Diamond plots (zoom) (unzoom) ] [LossMon timing plots] [Belle2 CLAWS waveforms] (2025c) [NLC CLAWS waveforms]
[BOR/BCM plots (raw) (calib) (BOR/iGp) (RFSoC) (BOR phase) (BOR HER hor fo inj. timing) ]
[Pressure bursts (ccgpatrol) (2025c) (Summary report by Kenta) (abort_list) ]
[AbortBPM plots] [BTorbit plots] [Linac pulse missing] [Earthquakes (jma) (tkb) ] [Clearing Electrode signal]

Beam Abort Database
Search conditions
 Show all aborts (incl. <60mA)  Hide LER aborts  Hide HER aborts  Injection-related aborts only  Non-injection aborts only
 QCS quench only  SBL events only  BeamLoss events only  >300mRad diamond aborts only  Inj. kicker accidentl fire only  Aborts with pressure burst only
 Diamond aborts only  High THR only  Low THR only  Diamond but no other abort  CLAWS D05V1 w/o VXD diamond  Earthquake aborts only
 Show LMtiming plots  Show more BOR plots  Show more CLAWS plots  Show OpticalFiber plots  Show AbortBPM plots  edit mode
Time period: 
2026-01-26
 ~ 
2026-12-31
     Show last 
800
 aborts     
LER abort	HER abort	Both ring abort	Diamond >300mRad	QCS quench
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
(H)	BT orbit	Belle2 CLAWS	Clearing
Electrode	Pressure
burst	Category	Tags	Comment
2026-03-12 15:04:36
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1197
958
2346
122
116
						
BeamLoss
BeamLoss
Physics run
2026-03-12 11:38:45
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
0
0
2346
4
0
							
Tuning
Injection
Tuning
2026-03-12 11:38:20
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
6
641

19.7 mRad
							
Tuning
Injection
Tuning
2026-03-12 11:37:33
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
37
38
2346
6
495
							
Tuning
Injection
Tuning
2026-03-12 03:47:40
Zlog json TimeStamp grp
edit
HER
HER
RF D10C
1398
1117
2346
160
140
						
RF
Physics run
RF
2026-03-12 02:33:34
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
997
798
2346
75
95

86.7 mRad
							
BeamLoss
BeamLoss
Physics run
2026-03-11 20:31:20
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1644
968
2346
292
276
						
BeamLoss
BeamLoss
Physics run
2026-03-11 19:49:59
Zlog json TimeStamp grp
edit
HER
HER
RF D04G
1524
1111
2346
243
113
						
BeamLoss
BeamLoss
Physics run
LER beam lossによるRFアークセンサー発報
2026-03-11 18:55:52
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1645
1117
2346
253
103

87.1 mRad
							
D09_H16
D09V2collimator
BeamLoss
BeamLoss
Physics run
Pressure burst
2026-03-11 11:53:21
Zlog json TimeStamp grp
edit
HER
HER
RF D10C
225
998
2346
123
16
						
RF
Physics run
RF
Tuner制御系が怪しい
最終的には空洞BDと思われる
2026-03-11 10:37:11
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1596
1111
2346
416
201
							
BeamLoss
BeamLoss
Physics run
2026-03-10 15:28:45
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1396
958
2346
234
268
						
EQ
EQ
Physics run
つくば市震度1　震源地:福島県沖
2026-03-10 12:36:24
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1396
1090
2346
252
132

393.4 mRad
							
BeamLoss
BeamLoss
Physics run
HERVertical軌道が数tarnでずれている（Tobiyama）
2026-03-10 11:01:17
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1621
1098
2346
307
85

87.7 mRad
							
D05_H15A
QR7ORE
BeamLoss
BeamLoss
Physics run
Pressure burst
tuneが4k跳んでいた(Tobiyama）
2026-03-09 13:45:55
Zlog json TimeStamp grp
edit
HER
HER
RF D11C
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
↑のLER起因両リングabort
D11のtime stamp問題
2026-03-09 07:52:10
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1409
1012
2346
186
1975

77.6 mRad
						
BeamLoss
BeamLoss
Physics run
2026-03-09 06:24:44
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
1397
1078
2346
176
110

33.2 mRad
							
BeamLoss
BeamLoss
Physics run
2026-03-09 05:40:24
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
+ High THR VXD diamond
1496
1117
2346
230
79

205.3 mRad
							
BeamLoss
BeamLoss
Physics run
2026-03-09 01:25:17
Zlog json TimeStamp grp
edit
HER
HER
RF D04F
1497
1117
2346
220
111
						
RF
Physics run
RF
D10B起因
2026-03-07 21:47:37
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
499
275
2346
50
330
							
Injection
Injection
2026-03-07 21:28:25
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
498
247
2346
46
208
							
Injection
Injection
2026-03-07 21:07:31
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1499
1118
2346
221
1552

44 mRad
							
BeamLoss
BeamLoss
Physics run
2026-03-07 13:02:15
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1497
1097
2346
270
140

57.2 mRad
							
BeamLoss
BeamLoss
Physics run
2026-03-07 06:10:32
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1497
1198
2346
305
85

1677.2 mRad
							
SBL
BeamLoss
Physics run
QCS quench
SBL
大きなビームロスの前にVertcal振動あり

2026-03-07 05:15:04
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-2
1497
1198
2346
253
91
						

D04_L03
QDWOP.5
BeamLoss
BeamLoss
Physics run
2026-03-07 01:16:10
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-2
1496
1198
2346
239
90
						
BeamLoss
BeamLoss
Physics run
2026-03-06 23:43:22
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
1123
913
2346
110
57
							

D03_L04
D03V4collimator
BeamLoss
BeamLoss
Physics run
2026-03-06 23:02:23
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1497
1197
2346
266
55

187.8 mRad
							
SBL
BeamLoss
Physics run
SBL
2026-03-06 08:34:08
Zlog json TimeStamp grp
edit
HER
HER
RF D04C
0
0
2346
0
0
							
RF
No beam
RF
2026-03-06 02:55:03
Zlog json TimeStamp grp
edit
HER
HER
RF D10B
1398
1118
2346
228
75
						
RF
Physics run
RF
2026-03-05 21:53:58
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1398
1118
2346
207
64

64.3 mRad
							
BeamLoss
BeamLoss
Physics run
2026-03-05 13:15:33
Zlog json TimeStamp grp
edit
HER
HER
Belle2 CLAWS
1397
1118
2346
321
68
							
BeamLoss
BeamLoss
Physics run
2026-03-05 11:40:46
Zlog json TimeStamp grp
edit
HER
HER
RF D04C
1398
0
2346
296
4
						
RF
No beam
RF
2026-03-05 10:54:00
Zlog json TimeStamp grp
edit
HER
HER
RF D04C
1398
12
2346
263
65
						
RF
RF
2026-03-05 10:34:06
Zlog json TimeStamp grp
edit
HER
HER
RF D04C
1398
0
2346
276
3
						
RF
No beam
RF
2026-03-05 10:25:12
Zlog json TimeStamp grp
edit
HER
HER
RF D04C
1397
1118
2346
235
63
						
RF
Physics run
RF
2026-03-05 02:22:15
Zlog json TimeStamp grp
edit
HER
HER
RF D04C
1297
1038
2346
209
39
						
RF
Physics run
RF
RF D04C-CAV#1-S TUNER DRIVER異常発報
2026-03-04 22:04:40
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1297
1038
2346
224
3839

682.9 mRad
							
D08_H05
D09V1collimator
D07_L02
FBL_kicker/taper/GV(D07_L01)
SBL
BeamLoss
Physics run
Pressure burst
SBL
2026-03-04 07:58:00
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
1097
878
2346
130
12

27.9 mRad
							
BeamLoss
BeamLoss
Physics run
2026-03-03 16:09:31
Zlog json TimeStamp grp
edit
HER
HER
RF D04C
997
798
2346
155
36
						
RF
Physics run
RF
D04C CAV#1-S TUNER DRIVER異常
2026-03-02 21:11:29
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
+ Low THR VXD diamond
+ High THR VXD diamond
1191
958
2346
163
17
						
BeamLoss
BeamLoss
Physics run
LERのplotは１分後のLER SBLのもの↑

no HER injection
2026-03-02 19:49:36
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1398
1118
2346
275
52

222 mRad
							
SBL
BeamLoss
Physics run
SBL
no HER injection
2026-03-02 13:23:48
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1398
1118
2346
304
143

1493.4 mRad
							
D02_H24

D08_H05
D09V1collimator
D02_H24
SBL
BeamLoss
Physics run
Pressure burst
QCS quench
SBL
HER v-tuneが大きくずれて (4kHz強上がった)FB出来ない状況になった。　3rd stop bandに引き込まれたのかも。しばらく不安定が続いていたが、最後のターンで大きく軌道が出た。by Tobiyama
通常のSBLとは異なる。


この後Optics Correction実行
2026-03-02 10:37:05
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1596
1277
2346
376
75

1364.2 mRad
							
D02_H24
SBL
BeamLoss
Physics run
Pressure burst
QCS quench
SBL
HER v-tuneが大きくずれている (4kHz強上がった)　by Tobiyama





time difference from HER injection: 57 ms
2026-03-02 08:14:47
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1595
1276
2346
419
91

77.2 mRad
							

D07_L00
FBT_kicker/GV(D08_L06)
BeamLoss
BeamLoss
Physics run
Pressure burst
no injection
D7＿H0真空跳ねは１分前
2026-03-02 04:31:15
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1397
1118
2346
409
98
							
D04_H09
taper/GV(D04_H04)
BeamLoss
BeamLoss
Physics run
Pressure burst
no injection
2026-03-01 23:20:22
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
184
2346
6
430

13 mRad
							
Injection
Injection
time difference from HER injection: ~550 us
2026-03-01 23:02:40
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1547
1238
2346
329
3817

1406.9 mRad
							
D09_H15
D09V2collimator/B2E.43
BeamLoss
BeamLoss
Physics run
Pressure burst
no injection
2026-03-01 22:23:19
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1548
1237
2346
310
80

40 mRad
							
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝9ms

2026-03-01 12:13:02
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1546
1238
2346
354
94

1657.5 mRad
							

D05_L23
D05V1collimator
SBL
BeamLoss
Physics run
Pressure burst
QCS quench
SBL
入射との時間差＝13ms
2026-03-01 09:37:32
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1547
1278
2346
357
74

30.5 mRad
							

D05_L23
D05V1collimator
BeamLoss
BeamLoss
EQ
Physics run
Pressure burst
同時刻に地震あり(震源宮崎県、震源付近での最大震度2)
S波到達前にアボート発生
偶然タイミングが被っただけでアボート原因はビームロス?

入射との時間差＝32ms
2026-03-01 07:43:33
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1546
281
2346
389
154
							
Injection
Injection
Physics run
2026-03-01 07:20:11
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1547
1237
2346
372
143
						
BeamLoss
BeamLoss
Physics run
no injection
2026-03-01 05:01:07
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
496
222
2346
80
1197

51.4 mRad
							
Tuning
Injection
Tuning
2026-03-01 03:56:15
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
482
16
2346
84
246
						
Tuning
2026-03-01 03:51:14
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
481
14
2346
88
307
						
Tuning
2026-03-01 01:19:08
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1596
1277
2346
387
55

912.2 mRad
							
SBL
BeamLoss
Physics run
QCS quench
SBL
入射との時間差＝11ms
2026-02-28 21:46:48
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
85
2346
11
1573

12.3 mRad
							
Injection
Injection
2026-02-28 21:33:37
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1298
1038
2346
291
41

776.9 mRad
							
D02_H22
IRpickup/iBump(SUS)/taper/GV(D02_H04)
SBL
BeamLoss
Physics run
Pressure burst
SBL
2026-02-28 20:47:13
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1547
1238
2346
401
70

272.1 mRad
							
D08_H22
injkicker/GV(D08_H03)dummy
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝79ms
2026-02-28 02:20:56
Zlog json TimeStamp grp
edit
HER
HER
RF D11C
1547
1238
2346
1466
80
							
D05_L23
D05V1collimator
↑のLER起因両リングabort（HERはD4G ARC COUPLER）
D11のtime stamp問題
2026-02-27 22:56:17
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
12
1263

53.7 mRad
							
Injection
Injection
2026-02-27 22:53:14
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
499
113
2346
151
1

15.7 mRad
							
Injection
Injection
2026-02-27 22:33:14
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
896
102
2346
209
731

6.4 mRad
							
Injection
Injection
2026-02-27 21:54:13
Zlog json TimeStamp grp
edit
HER
HER
RF D04C
798
638
2346
181
8
						
RF
Physics run
RF
RF D04C-CAV#1-S TUNER DRIVER 異常
2026-02-27 20:58:39
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
36
2346
12
1297

55.9 mRad
							
Tuning
Injection
Tuning
2026-02-27 20:51:57
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
10
689

14.1 mRad
							
Tuning
Injection
Tuning
2026-02-27 20:43:20
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
599
477
2346
115
1419

52.2 mRad
							
Injection
Injection
Physics run
2026-02-27 18:20:38
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1545
1238
2346
513
105

1615.8 mRad
							
SBL
BeamLoss
Physics run
QCS quench
SBL
入射との時間差＝5ms
2026-02-27 16:52:55
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
6
2346
21
0

24.6 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:50:27
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
11
1720

12.5 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:49:50
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
12
1024

27 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:49:13
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
9
0

51 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:48:23
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
9
1502

44.1 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:42:22
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
47
0
2346
10
1225

57.2 mRad
							
Injection
Injection
Tuning
2026-02-27 16:35:51
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
103
2346
14
1261

86.5 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:17:27
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
13
0

54.7 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:16:24
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
14
0

52.4 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:16:10
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
16
1056

62.5 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:15:32
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
17
0

106.1 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:14:54
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
16
0

105.2 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:14:38
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
15
0

89.3 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:14:15
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
13
1813

53.3 mRad
							
Tuning
Injection
Tuning
2026-02-27 16:12:19
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
122
2346
20
2234

87.3 mRad
							
Tuning
Injection
Tuning
2026-02-27 15:51:22
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
76
19
2346
109
1930

76.1 mRad
							
Injection
Injection
2026-02-27 15:03:57
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ High THR VXD diamond
1596
1278
2346
414
101

110.3 mRad
							
Injection
Injection
Physics run
2026-02-27 08:36:17
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1619
1317
2346
444
248

366.9 mRad
							
BeamLoss
BeamLoss
Physics run
no injection
2026-02-27 02:55:49
Zlog json TimeStamp grp
edit
HER
HER
RF D11C
+ Low THR VXD diamond
+ High THR VXD diamond
1520
1237
2346
353
1606

350.6 mRad
							
D02_H23
BLC2RE/SRmask
SBL
BeamLoss
Physics run
Pressure burst
SBL
入射との時間差＝16ms
2026-02-26 23:05:05
Zlog json TimeStamp grp
edit
HER
HER
RF D04H
1493
1198
2346
368
134
						
RF
Physics run
RF
2026-02-26 12:33:38
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1596
1278
2346
303
114

45.3 mRad
							
BeamLoss
BeamLoss
Physics run
no injection
2026-02-26 09:18:10
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1566
1286
2346
305
877

18 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝42ms
2026-02-26 06:25:21
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1568
1123
2346
316
58
							
D08_H16A
injBPM
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝21ms
2026-02-26 05:24:46
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1566
1253
2346
956
120
						
D02_L17
QLX1RP.2/BLX4RP.2/BLX2RP.2
EQ
EQ
Physics run
Pressure burst
2026-02-25 22:34:12
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1573
1258
2346
302
104

1316.7 mRad
							
SBL
BeamLoss
Physics run
QCS quench
SBL
入射との時間差＝72ms
2026-02-25 21:28:32
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
82
2346
4
168

6.7 mRad
						
Injection
Injection
2026-02-25 21:11:13
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1597
1251
2346
340
101

484.5 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝4ms
2026-02-25 18:16:07
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
39
0
2346
7
0

18.6 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:57:17
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
11
0

13.6 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:56:57
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
11
0

13.2 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:55:26
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
6
0

12.3 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:55:09
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
6
0

12.4 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:54:44
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
9
0

21.6 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:52:56
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
15
0

28.5 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:51:22
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
11
0

18.7 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:50:57
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
6
0

10 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:49:55
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
5
0

21.7 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:49:20
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
9
2346
5
774

8.4 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:44:50
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
8
2346
12
2008

12.1 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:42:18
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
1
2346
12
845

13.7 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:41:14
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
18
2958

51.8 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:40:29
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
1
2346
17
1081

50.9 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:39:29
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
18
0

48 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:39:08
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
16
0

16.5 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:38:23
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
11
0

11.5 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:38:04
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
9
0

17.8 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:37:50
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
9
594

22.5 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:36:32
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
3
2346
0
0

6.7 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:36:19
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
3
2346
13
936

4.1 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:34:57
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
8
0

20.6 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:34:25
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
4
2346
20
2719

13.2 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:33:09
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
33
2346
17
2539

12.3 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:24:47
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
2
2346
32
0

22.7 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:23:43
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
6
0

12.4 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:23:05
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
0
0

13.6 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:22:28
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
7
2346
17
2259

16.5 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:17:10
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
12
1272

18.1 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:16:26
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
8
2346
10
1049

13.3 mRad
							
Tuning
Injection
Tuning
2026-02-25 17:09:27
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1644
138
2346
391
1343

12.1 mRad
							
D07_L05
Injection
Injection
Physics run
Pressure burst
2026-02-25 16:49:03
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1646
1297
2346
479
235
						
D05_L23
D05V1collimator
D02_L17
QLX1RP.2/BLX4RP.2/BLX2RP.2
EQ
EQ
Physics run
Pressure burst
2026-02-25 11:29:17
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1547
1216
2346
306
119

268.5 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝32ms
2026-02-25 08:32:47
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1547
1217
2346
322
116

14.3 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝18ms
2026-02-24 19:33:02
Zlog json TimeStamp grp
edit
HER
HER
High THR VXD diamond
0
31
2346
8
684

50.6 mRad
						
Injection
Injection
2026-02-24 19:25:30
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
499
180
2346
92
1302

54.8 mRad
							
Injection
Injection
2026-02-24 19:15:43
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
167
9
2346
90
48

48.4 mRad
							
Injection
Injection
2026-02-24 17:01:52
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
473
116
2346
102
1026

49.8 mRad
							
Injection
Injection
2026-02-24 16:47:09
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1548
1217
2346
319
61

126.5 mRad
							
SBL
BeamLoss
Physics run
SBL
入射との時間差＝31ms
2026-02-23 23:30:42
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1396
897
2346
269
53

26.5 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝71ms
2026-02-23 16:09:40
Zlog json TimeStamp grp
edit
HER
HER
RF D10C
42
79
2346
4
507
						
RF
RF
2026-02-23 14:12:32
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D10-2
1396
1117
2346
268
57
							
D09_H06
D09H1collimator
Others
Injection kicker failure
Physics run
Pressure burst
Injection Kicker K3 Serious Failure
2026-02-23 09:48:31
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1396
1117
2346
278
546
						
BeamLoss
BeamLoss
Physics run
no injection
2026-02-22 18:46:10
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
+ High THR VXD diamond
1397
1118
2346
272
1483

166.1 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝68ms
2026-02-22 17:22:27
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1396
1118
2346
283
65

156.2 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝14ms
2026-02-22 15:26:15
Zlog json TimeStamp grp
edit
HER
HER
RF D04C
1396
1118
2346
275
78
						
RF
Physics run
RF
2026-02-22 11:22:06
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1396
1118
2346
298
24

462.9 mRad
							
D08_H23
taper/abtwindow&kicker
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝30ms
2026-02-22 03:28:22
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1298
997
2346
243
70

312.7 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝3ms
2026-02-22 02:50:13
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1396
1118
2346
262
65

71.7 mRad
							
D01_H10
stopper
BeamLoss
BeamLoss
Physics run
Pressure burst
no injection
2026-02-21 23:57:51
Zlog json TimeStamp grp
edit
HER
HER
RF D11C
+ Low THR VXD diamond
+ High THR VXD diamond
1496
1198
2346
330
58

1368.2 mRad
							
D01_H08
D01V1collimator
D01_H07
D01H3collimator
SBL
BeamLoss
Physics run
Pressure burst
SBL
no injection
2026-02-21 18:34:40
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1497
1198
2346
316
881

18.6 mRad
							
D05_H23
QFWOE
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝68ms
2026-02-21 16:14:50
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1496
1197
2346
312
92
							
D08_H05
D09V1collimator
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝78ms
2026-02-21 12:57:56
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1527
1236
2346
346
91

1039.4 mRad
							
SBL
BeamLoss
Physics run
QCS quench
SBL
入射との時間差＝33ms
2026-02-21 05:46:27
Zlog json TimeStamp grp
edit
Both
Both
Soft Abort
0
0
2346
0
0
							
Manual
入域
2026-02-20 23:39:32
Zlog json TimeStamp grp
edit
HER
HER
RF D11A
1545
1239
2346
442
92
						
RF
Physics run
RF
2026-02-20 18:19:01
Zlog json TimeStamp grp
edit
HER
HER
RF D04F
0
0
2346
0
0
						
RF
No beam
RF
D04F Recover中(ビームなし)
2026-02-20 17:53:55
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1568
1278
2346
482
82
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝28ms
2026-02-20 10:38:42
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1297
1038
2346
447
36

419.8 mRad
							
SBL
BeamLoss
Physics run
SBL
no injection
2026-02-20 09:49:58
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1297
991
2346
582
52
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝35ms
2026-02-19 21:25:17
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1596
1226
2346
418
75

615.4 mRad
							
SBL
BeamLoss
Physics run
SBL
入射との時間差＝6ms
2026-02-19 16:43:39
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1199
0
2346
264
0
						
Tuning
Injection
Tuning
2026-02-19 16:43:16
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
268
95
						
Tuning
Injection
Tuning
2026-02-19 16:41:33
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1198
0
2346
263
0
						
Tuning
Injection
Tuning
2026-02-19 16:34:14
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
287
0
						
Tuning
Injection
Tuning
2026-02-19 16:32:11
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1199
0
2346
276
9
						
Tuning
Injection
Tuning
2026-02-19 16:30:18
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1198
0
2346
270
9
						
Tuning
Injection
Tuning
2026-02-19 16:26:10
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
291
7
						
Tuning
Injection
Tuning
2026-02-19 16:25:47
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
306
89
						
Tuning
Injection
Tuning
2026-02-19 16:25:20
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1196
0
2346
296
0
						
Tuning
Injection
Tuning
2026-02-19 16:24:57
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1199
0
2346
277
0
						
Tuning
Injection
Tuning
2026-02-19 16:24:28
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
273
0
						
Tuning
Injection
Tuning
2026-02-19 16:24:00
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
292
0
						
Tuning
Injection
Tuning
2026-02-19 16:23:20
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
268
33
						
Tuning
Injection
Tuning
2026-02-19 16:22:39
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
276
24
						
Tuning
Injection
Tuning
2026-02-19 16:21:56
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
270
0
						
Tuning
Injection
Tuning
2026-02-19 16:21:02
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
303
30
						
Tuning
Injection
Tuning
2026-02-19 16:20:22
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1198
0
2346
274
30
						
Tuning
Injection
Tuning
2026-02-19 16:18:36
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
277
0
						
Tuning
Injection
Tuning
2026-02-19 16:16:59
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
279
32
						
Tuning
Injection
Tuning
2026-02-19 16:16:00
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
254
19
						
Tuning
Injection
Tuning
2026-02-19 16:14:45
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
1197
0
2346
252
29
						
Tuning
Injection
Tuning
2026-02-19 15:53:16
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1197
6
2346
286
39
						
Tuning
Injection
Tuning
2026-02-19 14:38:30
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1495
1078
2346
435
722

186.2 mRad
							
SBL
BeamLoss
Physics run
SBL
no injection
2026-02-19 08:08:24
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1397
1099
2346
301
59
						
BeamLoss
BeamLoss
Physics run
入射との時間差＝7ms
2026-02-19 06:10:39
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D10-2
+ Low THR VXD diamond
+ High THR VXD diamond
1396
1097
2346
311
60

551.2 mRad
							
SBL
BeamLoss
Physics run
SBL
入射との時間差＝19ms
2026-02-19 03:20:02
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1397
1118
2346
355
59

842.5 mRad
							
D07_H04
FBmonitor
D01_H08
D01V1collimator
SBL
BeamLoss
Physics run
Pressure burst
SBL
入射との時間差＝66ms
2026-02-18 16:33:23
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
18
0
2346
6
0

20 mRad
							
Tuning
BeamLoss
Tuning
2026-02-18 16:05:08
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
30
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-18 08:47:07
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-3
122
246
2346
6
1
						
BeamLoss
BeamLoss
no injection
2026-02-18 03:42:12
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1298
1036
2346
274
41

30.3 mRad
							
BeamLoss
BeamLoss
Physics run
no injection
2026-02-17 18:08:02
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
4
526
						
Tuning
Injection
Tuning
2026-02-17 18:07:30
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
5
2346
3
1
						
Tuning
Injection
Tuning
2026-02-17 18:04:00
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
28
2709

56.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:03:42
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
18
1844
							
Tuning
Injection
Tuning
2026-02-17 18:03:19
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
21
3

116.9 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:02:59
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor TSUKUBA B4
+ High THR VXD diamond
0
0
2346
20
2

69.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:02:44
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
60
0

153.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:02:30
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
88
782

252.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:02:15
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
158
0

264 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:01:59
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
158
3

297.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:01:39
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
159
4

449.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:01:23
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
165
0

351.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:00:57
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
14
0

75.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 18:00:43
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
12
0

81.9 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:59:58
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
16
0

94.9 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:59:46
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
77
0

238.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:59:32
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
60
0

217.9 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:59:20
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
24
29

185.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:59:06
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
6
0

70.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:58:50
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
11
2074

68.9 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:58:33
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
9
0
							
Tuning
Injection
Tuning
2026-02-17 17:58:19
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
16
3

71 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:58:04
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
6
0
							
Tuning
Injection
Tuning
2026-02-17 17:57:48
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
8
0
							
Tuning
Injection
Tuning
2026-02-17 17:57:33
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
12
0

82.9 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:57:17
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
9
0
							
Tuning
Injection
Tuning
2026-02-17 17:57:03
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
18
0

90 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:56:28
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
10
1360

101.9 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:55:51
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
0
19
							
Tuning
Injection
Tuning
2026-02-17 17:55:28
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
10
0

96.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:54:46
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
0
108
						
Tuning
Injection
Tuning
2026-02-17 17:53:51
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
121
							
Tuning
Injection
Tuning
2026-02-17 17:53:17
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
10
0

103.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:53:03
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
8
0

88.9 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:52:45
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
8
0

93.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:52:27
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
9
78

100.1 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:48:28
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
16
0

163.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:48:13
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
14
0

137.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:47:58
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
12
0

120.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:47:46
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
8
540

87.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:47:31
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
8
2326

85.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:46:15
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
9
1075

105.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:45:22
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
0
276
							
Tuning
Injection
Tuning
2026-02-17 17:44:40
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
79
3164

373.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:43:39
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
46
1

349.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:43:08
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
245
6

961.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:42:40
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
78
2

466.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:06:33
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
91
0

480.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:06:01
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
35
2

303.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:05:42
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
44
0

338.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:05:08
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
16
325

164.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:03:02
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
1
181
							
Tuning
Injection
Tuning
2026-02-17 17:01:48
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
16
1

149.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 17:01:32
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
15
1218

127.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:58:28
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
13
998

92.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:56:36
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
12
0

102.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:56:22
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
13
1144

108.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:56:04
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
18
0

125.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:51:35
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
19
0

107.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:51:23
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
19
0

124.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:51:11
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
21
0

125.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:50:57
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
26
0

151.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:50:44
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
12
945

90.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:49:47
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
13
522

105.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:48:29
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
44
3

212.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:46:35
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
51
0

248.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:46:18
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
14
0

120.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:45:58
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
21
0

139.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:45:22
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
30
2173

183 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:13:34
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
33
						
Tuning
Injection
Tuning
2026-02-17 16:13:11
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
3
801
						
Tuning
Injection
Tuning
2026-02-17 16:12:43
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
3
0
						
Tuning
Injection
Tuning
2026-02-17 16:12:07
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
3
354
						
Tuning
Injection
Tuning
2026-02-17 16:10:13
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
5
737
							
Tuning
Injection
Tuning
2026-02-17 16:09:43
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
12
0

114.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:09:25
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
36
0

204.1 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:09:05
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
31
1033

170.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 16:07:11
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
2
466
						
Tuning
Injection
Tuning
2026-02-17 16:06:44
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
2
0
						
Tuning
Injection
Tuning
2026-02-17 16:05:49
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
2
0
						
Tuning
Injection
Tuning
2026-02-17 16:05:00
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-17 16:03:33
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
0
126
						
Tuning
Injection
Tuning
2026-02-17 16:03:09
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
2
0
						
Tuning
Injection
Tuning
2026-02-17 16:02:41
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
2
663
						
Tuning
Injection
Tuning
2026-02-17 16:02:10
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
3
763
						
Tuning
Injection
Tuning
2026-02-17 16:01:46
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
2
0
						
Tuning
Injection
Tuning
2026-02-17 16:01:24
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
9
1511
							
Tuning
Injection
Tuning
2026-02-17 16:00:37
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
3
744
							
Tuning
Injection
Tuning
2026-02-17 16:00:13
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
5
717

54.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:59:51
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
5
1136

65.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:59:29
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
3
1
							
Tuning
Injection
Tuning
2026-02-17 15:58:50
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
5
900
							
Tuning
Injection
Tuning
2026-02-17 15:58:26
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
10
645

57.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:57:40
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
9
835
						
Tuning
Injection
Tuning
2026-02-17 15:57:06
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D9 (Optical Fiber)
0
0
2346
3
709
						
Tuning
Injection
Tuning
2026-02-17 15:55:29
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
10
1114
						
Tuning
Injection
Tuning
2026-02-17 15:53:27
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
14
1489

47.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:53:15
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
17
1489

123.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:52:14
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
97
0

267.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:52:02
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
18
2

104 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:51:50
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
129
651

270.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:51:38
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
172
0

361.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:51:24
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
175
0

543.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:51:08
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
53
0

275 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:50:56
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
48
0

273.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:50:31
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
48
1072

259.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:50:19
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
58
5

301.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:35:06
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
77
0

237 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:34:54
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
11
0

89.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:34:40
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
51
4

193.1 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:33:52
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
70
4

221.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:32:59
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
67
4

216.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:32:36
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
72
0

228.3 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:26:05
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
128
0

392.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:25:54
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
92
0

348.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:25:43
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
16
0

114.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:25:31
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
25
2342

139.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:25:20
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
25
2342

143.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:24:58
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
10
3
							
Tuning
Injection
Tuning
2026-02-17 15:24:48
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
7
3

70.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:24:21
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
29
3

139.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:24:06
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
17
0

56.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:23:54
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
14
1199

100.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:23:33
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
21
0

86.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:23:23
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
21
0

116 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:23:13
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
15
0

103.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:22:56
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
11
1634

78.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:21:57
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
8
1372

73.4 mRad
							
Tuning
Injection
Tuning
2026-02-17 15:21:01
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
44
0
2346
17
1797

107.9 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:55:38
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
37
0
2346
27
0

205.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:15:13
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
11
989

85.8 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:14:54
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
10
896

80.1 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:10:52
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
9
0

75.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:10:33
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
8
426

70.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:07:31
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
14
1087

137.6 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:03:47
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
8
910

53.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:03:06
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
120
0

503.2 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:02:40
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
18
3295

179 mRad
							
Tuning
Injection
Tuning
2026-02-17 13:01:49
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
25
0
2346
103
9

507.5 mRad
							
Tuning
Injection
Tuning
2026-02-17 11:00:37
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
20
0

148.7 mRad
							
Tuning
Injection
Tuning
2026-02-17 10:59:51
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
20
0
2346
7
0

60 mRad
							
Tuning
Injection
Tuning
2026-02-17 10:59:34
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
20
0
2346
13
0
							
Tuning
Injection
Tuning
2026-02-17 10:58:32
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
21
0
2346
11
0
						
Tuning
Injection
Tuning
2026-02-17 10:57:57
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
21
0
2346
10
0
						
Tuning
Injection
Tuning
2026-02-17 10:57:18
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
21
0
2346
9
0
						
Tuning
Injection
Tuning
2026-02-17 10:56:52
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
18
0
2346
10
0
						
Tuning
Injection
Tuning
2026-02-17 10:53:58
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
40
0
2346
50
0

268.3 mRad
							
Tuning
Injection
Tuning
2026-02-15 04:48:30
Zlog json TimeStamp grp
edit
Both
Both
QC1LE PS I/L
1544
1199
2346
355
162
							
MAG
MAG
Physics run
QCS quench
L側He圧縮機の制御盤のプレーカーがトリップしたためQC1LE PSに停止命令
2026-02-15 02:24:30
Zlog json TimeStamp grp
edit
HER
HER
RF D11C
+ Low THR VXD diamond
1496
1186
2346
353
741

20.5 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝29ms
2026-02-14 19:55:32
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1471
1178
2346
338
159

106.1 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝22ms
2026-02-14 18:48:10
Zlog json TimeStamp grp
edit
Both
Both
RF D04G
1098
878
2346
234
81
							
RF
Physics run
RF
大穂未処理水系統の流量が一時的に低下したことが原因
2026-02-05 14:56と同じ症状

2026-02-14 16:32:52
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
1545
1198
2346
338
172

55.4 mRad
							
D04_H06A
taper/SRM/HOM/GV(D04_H03)
BeamLoss
BeamLoss
Physics run
Pressure burst
no injection
2026-02-14 13:33:04
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1547
1218
2346
313
169
							
D04_H06A
taper/SRM/HOM/GV(D04_H03)
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝59ms
2026-02-14 08:56:01
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1389
1091
2346
268
124

33.9 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝7ms
2026-02-14 05:19:15
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1198
848
2346
200
452
						
D02_H23
BLC2RE/SRmask
D07_H04A
FBT_kicker/GV(D07_H02)
D02_H23
BLC2RE/SRmask
BeamLoss
BeamLoss
Physics run
Pressure burst
HER vertical振動。
pilot bunch tuneを見失ってvertical tuneが+3kHz程ずれ、フィードバックシステムが不安定になっていた.

入射との時間差＝33ms

2026-02-14 04:24:41
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1407
1127
2346
272
156

139.3 mRad
							
BeamLoss
BeamLoss
Physics run
no injection
2026-02-13 17:13:06
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
38
53
2346
64
1564

57 mRad
						
Injection
Injection
Physics run
2026-02-13 16:49:43
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
548
51
2346
109
995
							
Injection
Injection
Physics run
2/13からDiamond abort 閾値8→12に変更
2026-02-13 16:37:22
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
548
437
2346
78
130
						
BeamLoss
BeamLoss
Physics run
no injection
2026-02-12 05:53:28
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1397
1135
2346
301
157
						
BeamLoss
BeamLoss
Physics run
入射との時間差＝34ms
2026-02-12 04:24:50
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1296
1037
2346
217
71

527 mRad
							
SBL
BeamLoss
Physics run
SBL
入射との時間差＝2ms
2026-02-12 03:04:02
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1396
1158
2346
264
136

36.5 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝47ms
2026-02-11 12:21:53
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
997
798
2346
112
63

39.9 mRad
							
D02_H23
BLC2RE/SRmask
D02_H24
BeamLoss
BeamLoss
Physics run
Pressure burst
no injetion
2026-02-11 11:48:37
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1493
1168
2346
309
126
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝32ms
2026-02-11 07:54:06
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1496
1149
2346
330
101

12.8 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝56ms
2026-02-11 02:16:35
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
1466
1130
2346
289
31

57.9 mRad
							
Injection
Injection
Physics run
linac Klystron down
2026-02-11 00:25:56
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1496
1157
2346
315
86

20.3 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝45ms
2026-02-10 18:33:46
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1492
1153
2346
316
141

41.9 mRad
					
BeamLoss
BeamLoss
Physics run
入射との時間差＝20ms
2026-02-10 16:06:34
Zlog json TimeStamp grp
edit
HER
HER
RF D04H
1495
1169
2346
304
164
						
RF
Physics run
RF
2026-02-10 08:25:50
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1496
1198
2346
326
193

33.5 mRad
							
D07_H04A
FBT_kicker/GV(D07_H02)
BeamLoss
BeamLoss
Physics run
Pressure burst
FBT_kicker区間で真空が跳ねているが、機器に特に異常はなく、定期的に跳ねる区間（Abort時以外も）なので、気にしないで良い。from Tobiyama

入射との時間差＝1ms
2026-02-10 06:29:17
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1466
1198
2346
341
79

29.5 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝20ms
2026-02-10 03:26:49
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ Low THR VXD diamond
+ High THR VXD diamond
1496
1178
2346
343
162

1724.4 mRad
							
D08_H05
D09V1collimator
SBL
BeamLoss
Physics run
Pressure burst
SBL
入射との時間差＝27ms
2026-02-10 00:36:57
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1495
1186
2346
343
215

7.8 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝33ms
2026-02-09 21:28:09
Zlog json TimeStamp grp
edit
Both
Both
Loss Monitor TSUKUBA B4
1296
1038
2346
462
158
							
EQ
EQ
Physics run
2026-02-09 20:22:36
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1296
1037
2346
493
150

387.5 mRad
							

D07_H04A
FBT_kicker/GV(D07_H02)
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝14ms
2026-02-09 04:11:08
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1430
1158
2346
23
3

92.1 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝3ms
2026-02-08 20:47:31
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1446
1158
2346
23
3
							
BeamLoss
BeamLoss
Physics run
no injection
2026-02-08 15:31:40
Zlog json TimeStamp grp
edit
HER
HER
RF D04F
1397
1038
2346
23
3
						
RF
Physics run
RF
2026-02-08 11:30:50
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
999
593
2346
23
3

15.2 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝19ms
2026-02-08 10:55:21
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1396
1038
2346
23
3
							
BeamLoss
BeamLoss
Physics run
no injection
2026-02-08 07:55:37
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1395
974
2346
23
3

17.8 mRad
							
D02_H24
BeamLoss
BeamLoss
Physics run
Pressure burst
HER no injection (BS モードでビーム確認中)
2026-02-08 01:36:00
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-2
1396
932
2346
23
3
						
D02_H24
BeamLoss
BeamLoss
Physics run
Pressure burst
D9V1/V4 collimator

no injection
2026-02-07 17:20:28
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
+ High THR VXD diamond
1397
1038
2346
23
3

227.2 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝36ms
2026-02-07 14:54:36
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
+ High THR VXD diamond
1397
1037
2346
23
3

322.7 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝26ms
2026-02-07 08:59:17
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor D9 (Optical Fiber)
+ High THR VXD diamond
1397
1118
2346
23
3

82.3 mRad
							
Injection
Injection
Physics run

2026-02-07 05:40:11
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1396
1117
2346
23
3

10 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝41ms
2026-02-07 00:58:38
Zlog json TimeStamp grp
edit
Both
Both
Loss Monitor TSUKUBA B4
934
597
2346
23
3
							

D07_L09
abtkicker(1V)/injkicker(3H)/taper/GV(D07_L04)
EQ
EQ
Physics run
つくば市震度1
2026-02-07 00:31:38
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1396
1117
2346
23
3

19 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝39ms
2026-02-06 22:13:38
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1396
1118
2346
23
3

22.2 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝1ms
2026-02-06 20:44:52
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1396
1117
2346
23
3

34.3 mRad
							
D10_H28
GV(D10_H05)
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝11ms
2026-02-06 10:57:34
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
798
945
2346
57
25

60.2 mRad
							
BeamLoss
BeamLoss
Physics run
この後LossMonitor Abort:D10-2_2 (D9V1 collimator)　の閾値を５V→10Vに変更

no injection
2026-02-06 06:43:19
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1397
1118
2346
402
36

10.4 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝68ms
2026-02-06 00:15:21
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1444
837
2346
441
68
							
D02_H23
BLC2RE/SRmask
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝77ms
2026-02-05 23:39:26
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-2
1403
1157
2346
434
117
						
BeamLoss
BeamLoss
Physics run
入射との時間差＝2ms
2026-02-05 20:37:59
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-2
1197
832
2346
460
76
						
BeamLoss
BeamLoss
Physics run
入射との時間差＝2ms
2026-02-05 18:43:52
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1394
1118
2346
367
97

93.4 mRad
							
D01_H10
stopper
D01_H11
GV(D01_H02)
BeamLoss
BeamLoss
Physics run
Pressure burst
no injection
2026-02-05 16:18:05
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-2
1198
999
2346
271
70
						
BeamLoss
BeamLoss
Physics run
入射との時間差＝2ms
2026-02-05 14:56:45
Zlog json TimeStamp grp
edit
Both
Both
RF D04G
1336
1087
2346
393
92
							
RF
Physics run
RF
D04C, D04G, D05Bで HPRF CIRCULATOR WATERが発報
大穂地区HER,LERで同時多発
一時的に大穂地区の未処理水の流量低下が起こったか
2026-02-05 13:05:07
Zlog json TimeStamp grp
edit
HER
HER
RF D11C
1160
1119
2346
318
125
						
RF
Physics run
RF
D11D-KLY VACUUM IL発報によるHV Off
2026-02-05 10:40:37
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1297
865
2346
299
18

70.8 mRad
							
BeamLoss
BeamLoss
Physics run
no injection
2026-02-05 06:46:27
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1396
1118
2346
372
83

104.8 mRad
							
D08_H05
D09V1collimator
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝63ms
2026-02-05 04:09:09
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-2
1396
1118
2346
370
78
						
BeamLoss
BeamLoss
Physics run
入射との時間差＝2ms
2026-02-05 01:14:52
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-2
953
422
2346
200
327
						

D07_L09
abtkicker(1V)/injkicker(3H)/taper/GV(D07_L04)
BeamLoss
BeamLoss
Physics run
Pressure burst
入射との時間差＝2ms
2026-02-05 00:53:48
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
1348
1078
2346
373
111

34.3 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝30ms
2026-02-04 23:46:35
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1251
774
2346
299
126

187.1 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝79ms
2026-02-04 23:19:20
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1347
1078
2346
448
76

114.7 mRad
							
BeamLoss
BeamLoss
Physics run
no injection
2026-02-04 19:45:57
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1342
1077
2346
401
77

128.3 mRad
							
BeamLoss
BeamLoss
Physics run
no injection
2026-02-04 18:13:01
Zlog json TimeStamp grp
edit
HER
HER
RF D10B
1245
998
2346
287
59
						
RF
Physics run
RF
HER -1モードのノイズの件の調査に伴う
2026-02-04 11:57:08
Zlog json TimeStamp grp
edit
HER
HER
RF D10C
1495
1117
2346
211
47
							
RF
Physics run
RF
2026-02-04 04:27:55
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1398
934
2346
245
537
						
D02_H23
BLC2RE/SRmask
D02_H22
IRpickup/iBump(SUS)/taper/GV(D02_H04)
D07_H04A
FBT_kicker/GV(D07_H02)
BeamLoss
BeamLoss
Physics run
Pressure burst
HER 積み上げ中にtuneを見失い　"TKW(4,1,7) forward" Alarm多発して，治る前にHER Abort
入射との時間差＝40ms
2026-02-04 03:36:41
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-3
1396
1077
2346
270
58
						
D02_H23
BLC2RE/SRmask
EQ
EQ
Physics run
Pressure burst
つくば市震度1
2026-02-03 23:24:18
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
1398
1073
2346
250
64

40.3 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝59ms
2026-02-03 18:03:38
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
1397
1116
2346
3737
102
							
D02_L17
QLX1RP.2/BLX4RP.2/BLX2RP.2
D10_L12
GV(D10_L03)
D06_L11
EQ
BeamLoss
EQ
Physics run
つくば市震度2
2026-02-03 15:58:20
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
+ Low THR VXD diamond
1394
1118
2346
307
105
						
BeamLoss
BeamLoss
Physics run
LERは１分後のアボートデータ

入射との時間差＝47ms
2026-02-03 10:24:32
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
0
998
2346
4
1057

106.7 mRad
							
BeamLoss
BeamLoss
Physics run
入射との時間差＝2ms
2026-02-03 08:06:21
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
1196
998
2346
185
53
							
BeamLoss
BeamLoss
Physics run
2026-02-02 21:55:41
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1196
998
2346
212
31

972.8 mRad
							
BeamLoss
BeamLoss
Physics run
2026-02-02 15:04:09
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
+ High THR VXD diamond
1197
998
2346
309
76

586 mRad
							
SBL
BeamLoss
Physics run
SBL
入射との時間差＝9ms
2026-02-01 14:40:57
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
9
0
							
Tuning
Injection
Tuning
2026-02-01 14:40:22
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
14
200

82.6 mRad
							
Tuning
Injection
Tuning
2026-02-01 14:39:37
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
2
0
						
Tuning
Injection
Tuning
2026-02-01 14:39:10
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 14:38:41
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
2
38
						
Tuning
Injection
Tuning
2026-02-01 14:21:42
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
60
						
Tuning
Injection
Tuning
2026-02-01 14:20:45
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 14:20:07
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
61
						
Tuning
Injection
Tuning
2026-02-01 14:17:24
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
35
0

179 mRad
							
Tuning
Injection
Tuning
2026-02-01 13:54:19
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
27
0

123.9 mRad
							
Tuning
Injection
Tuning
2026-02-01 13:53:42
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
44
1

198.9 mRad
							
Tuning
Injection
Tuning
2026-02-01 13:53:18
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
53
0

200.7 mRad
							
Tuning
Injection
Tuning
2026-02-01 13:52:49
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
3
0
							
Tuning
Injection
Tuning
2026-02-01 13:52:10
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
19
0

120.5 mRad
							
Tuning
Injection
Tuning
2026-02-01 13:51:24
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
32
484

156.7 mRad
							
Tuning
Injection
Tuning
2026-02-01 13:49:26
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:36:16
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:32:52
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:32:33
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:32:11
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:31:48
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:30:58
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:30:37
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:30:18
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
26
						
Tuning
Injection
Tuning
2026-02-01 13:29:44
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:29:26
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:29:09
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:28:31
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:28:06
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:27:48
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
32
						
Tuning
Injection
Tuning
2026-02-01 13:27:20
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:26:57
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:26:34
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:26:13
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:25:51
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:25:24
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
33
						
Tuning
Injection
Tuning
2026-02-01 13:23:47
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
34
						
Tuning
Injection
Tuning
2026-02-01 13:22:00
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
5
82

53 mRad
							
Tuning
Injection
Tuning
2026-02-01 13:20:24
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
1
139
						
Tuning
Injection
Tuning
2026-02-01 13:12:11
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
31
						
Tuning
Injection
Tuning
2026-02-01 13:11:05
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:10:38
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:10:18
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 13:09:42
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
47
						
Tuning
Injection
Tuning
2026-02-01 13:05:37
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
11
						
Tuning
Injection
Tuning
2026-02-01 13:04:11
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
6
10

54.2 mRad
							
Tuning
Injection
Tuning
2026-02-01 13:01:48
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
33
493

214.9 mRad
							
Tuning
Injection
Tuning
2026-02-01 12:56:36
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
1
503
						
Tuning
Injection
Tuning
2026-02-01 12:50:44
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
						
Tuning
Injection
Tuning
2026-02-01 12:50:09
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
0
0
							
Tuning
Injection
Tuning
2026-02-01 12:49:34
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
4
2
							
Tuning
Injection
Tuning
2026-02-01 12:49:07
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
36
0

212.9 mRad
							
Tuning
Injection
Tuning
2026-02-01 12:48:41
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
1
2
							
Tuning
Injection
Tuning
2026-02-01 12:48:13
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
0
2

119.7 mRad
							
Tuning
Injection
Tuning
2026-02-01 12:47:07
Zlog json TimeStamp grp
edit
Both
HER
Loss Monitor TSUKUBA B4
+ High THR VXD diamond
0
0
2346
13
0

113.1 mRad
							
Tuning
Injection
Tuning
2026-02-01 08:28:27
Zlog json TimeStamp grp
edit
HER
HER
RF D10C
0
0
2346
0
0
						
Others
Others
RF KPSタップ切り替えのためRF, HV OFF
Linac施設水トラブル待機中の節電のため、低圧タップに切り替えてあった
2026-02-01 08:25:08
Zlog json TimeStamp grp
edit
HER
HER
RF D04F
0
0
2346
0
0
						
Others
No beam
Others
RF KPSタップ切り替えのためRF, HV OFF
Linac施設水トラブル待機中の節電のため、低圧タップに切り替えてあった
2026-01-31 22:45:02
Zlog json TimeStamp grp
edit
Both
Both
ESR1 PS I/L
5
111
2346
0
0
							
MAG
QCS quench
2026-01-31 09:39:32
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-3
898
700
2346
174
8
						
BeamLoss
BeamLoss
Physics run
入射との時間差＝9ms

HER Horizontal 振動
2026-01-31 03:47:41
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
898
717
2346
798
70
							
D09_L18
EQ
Physics run
つくば市震度2
2026-01-30 20:30:56
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
498
368
2346
127
498

55.5 mRad
							
Injection
Injection
Physics run
2026-01-30 18:00:51
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor D10-3
39
0
1565
0
1
						
Tuning
Injection
Tuning
2026-01-30 16:32:22
Zlog json TimeStamp grp
edit
Both
Both
Safety System
12
0
1565
0
0
							
Others
D9 の安全系PLC down
2026-01-30 00:28:51
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
117
58
393
72
2
						
Others
Injection
Study
Collimator Study
2026-01-29 23:32:07
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
119
58
393
240
113
						
Others
Injection
Study
Collimator Study
2026-01-29 16:15:46
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
12
2346
1
0
						
Tuning
Tuning
HER βy = 1mm セット後

この後17:35にLER AbortでHERが道連れabortされないように、Loss Monitor D7-3-2の積
分器への入力ケーブルを抜いた。
2026-01-29 14:52:31
Zlog json TimeStamp grp
edit
Both
HER
Low THR VXD diamond
0
0
2346
18
4

10.7 mRad
							
Tuning
Injection
Tuning
2026-01-29 14:52:06
Zlog json TimeStamp grp
edit
Both
HER
Belle2 CLAWS
+ Low THR VXD diamond
0
0
2346
15
0

23.7 mRad
							
Tuning
Injection
Tuning
2026-01-29 14:51:28
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
9
2346
5
815

48.3 mRad
							
Tuning
Injection
Tuning
2026-01-29 14:48:56
Zlog json TimeStamp grp
edit
HER
HER
Loss Monitor TSUKUBA B4
0
0
2346
1
0
						
Tuning
Injection
Tuning
2026-01-29 14:41:07
Zlog json TimeStamp grp
edit
Both
HER
High THR VXD diamond
0
0
2346
20
2811

87.8 mRad
							
Tuning
Injection
Tuning

"""

# Regex to find dates denoting the start of an event
date_pattern = re.compile(r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})')
events_raw = date_pattern.split(raw_text)[1:] # Drop UI preamble

data = []
for i in range(0, len(events_raw), 2):
    time = events_raw[i].strip()
    lines = [line.strip() for line in events_raw[i+1].split('\n') if line.strip() != '']
    
    if len(lines) < 9:
        continue

    # lines[0] is always 'Zlog json TimeStamp grp edit'
    abort_ring = lines[1]
    origin_ring = lines[2]

    # Source can span multiple lines (e.g. starting with +)
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

    # Categorize the remaining lines
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

    data.append({
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

# Export directly to Excel
df = pd.DataFrame(data)
df.to_excel('Complete_HER_Event_Data_Analysis_Summary.xlsx', index=False)
print(f"Successfully exported {len(df)} events to Complete_HER_Event_Data_Analysis_Summary.xlsx")