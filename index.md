## SingleVC: Any2-to-one voice conversion

SingleVC performs A2O VC through a self-supervised task(\emph{X$_{i}$} $\to$ $\hat{\emph{X$_{i}^{s}$}}$ $\to$ $\hat{\emph{X$_{i}$}}$).  $\hat{\emph{X$_{i}^{s}$}}$ is  a PSDR-processed speech with pitch-shifted $s$. The more details can be access here.

This page provides converted speeches samples. The pretrained model is trained with p249(female, 22.5-minute) from VCTK corpus.

<audio id="audio" controls="" preload="none">
      <source id="wav" src="https://github.com/BrightGu/SingleVC/blob/gh-pages/1_BAC009S0234W0129.wav">
</audio>

### VCTK
1. F1, Ask her to bring these things with her from the store.
2. F2, She can scoop these things into three red bags, and we will go meet her Wednesday at the train station. 
3. M1, Please call Stella.
4. M2, He should have asked for a second opinion.

<table>
   <tr>
      <td>Utterance</td>
      <td>Source</td>
      <td>Convert</td>
   </tr>
   <tr>
      <td>F1_p310_002</td>
      <td><audio id="audio" controls="" preload="none"> <source id="VF1_s" src="converted_sample/VCTK/F1/1_p310_002.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="VF1_t" src="converted_sample/VCTK/F1/1_p310_002_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>F2_p240_005</td>
      <td><audio id="audio" controls="" preload="none"> <source id="VF2_s" src="converted_sample/VCTK/F2/1_p240_005.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="VF2_t" src="converted_sample/VCTK/F2/1_p240_005_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>M1_p374_001</td>
      <td><audio id="audio" controls="" preload="none"> <source id="VM1_s" src="converted_sample/VCTK/M1/1_p374_001.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="VM1_t" src="converted_sample/VCTK/M1/1_p374_001_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>M2_p245_062</td>
      <td><audio id="audio" controls="" preload="none"> <source id="VM2_s" src="converted_sample/VCTK/M2/4_p245_062.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="VM2_t" src="converted_sample/VCTK/M2/4_p245_062_generated_e2e.wav"> </audio></td>
   </tr>
</table>


### LibriSpeech
1. F1, The visit went off successfully, as was to have been expected.
2. F2, "He's Gilbert Blythe," said Marilla contentedly.
3. M1, All judgements do not require examination, that is, investigation into the grounds of their truth.
4. M2, And always that same pretext is offered--it looks like the thing.

<table>
   <tr>
      <td>Utterance</td>
      <td>Source</td>
      <td>Convert</td>
   </tr>
   <tr>
      <td>F1_225_131256_000006_000002</td>
      <td><audio id="audio" controls="" preload="none"> <source id="LF1_s" src="converted_sample/LirbiSpeech/F1/2_225_131256_000006_000002.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="LF1_t" src="converted_sample/LirbiSpeech/F1/2_225_131256_000006_000002_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>F2_188_135249_000012_000000</td>
      <td><audio id="audio" controls="" preload="none"> <source id="LF2_s" src="converted_sample/LirbiSpeech/F2/4_188_135249_000012_000000.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="LF2_t" src="converted_sample/LirbiSpeech/F2/4_188_135249_000012_000000_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>M1_296_129659_000004_000005</td>
      <td><audio id="audio" controls="" preload="none"> <source id="LM1_s" src="converted_sample/LirbiSpeech/M1/1_296_129659_000004_000005.wav"> </audio> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="LM1_t" src="converted_sample/LirbiSpeech/M1/1_296_129659_000004_000005_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>M2_272_130225_000010_000007</td>
      <td><audio id="audio" controls="" preload="none"> <source id="LM2_s" src="converted_sample/LirbiSpeech/M2/3_272_130225_000010_000007.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="LM2_t" src="converted_sample/LirbiSpeech/M2/3_272_130225_000010_000007_generated_e2e.wav"> </audio></td>
   </tr>
</table>

### VCC2020
1. F1, If not, it's about time somebody did.
2. F2, The figures are adjusted for seasonal variation.
3. M1, The trip was a disaster.
4. M2, Sometimes, it helps to take a step back.

<table>
   <tr>
      <td>Utterance</td>
      <td>Source</td>
      <td>Convert</td>
   </tr>
   <tr>
      <td>F1_TEF1_E10061</td>
      <td><audio id="audio" controls="" preload="none"> <source id="CF1_s" src="converted_sample/VCC2020/F1/1_TEF1_E10061.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="CF1_t" src="converted_sample/VCC2020/F1/1_TEF1_E10061_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>F2_SEF2_E10066</td>
      <td><audio id="audio" controls="" preload="none"> <source id="CF2_s" src="converted_sample/VCC2020/F2/5_SEF2_E10066.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="CF2_t" src="converted_sample/VCC2020/F2/5_SEF2_E10066_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>M1_SEM1_E10033</td>
      <td><audio id="audio" controls="" preload="none"> <source id="CM1_s" src="converted_sample/VCC2020/M1/3_SEM1_E10033.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="CM1_t" src="converted_sample/VCC2020/M1/3_SEM1_E10033_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>M2_TEM2_E20042</td>
      <td><audio id="audio" controls="" preload="none"> <source id="CM2_s" src="converted_sample/VCC2020/M2/1_TEM2_E20042.wav"> </audio> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="CM2_t" src="converted_sample/VCC2020/M2/1_TEM2_E20042_generated_e2e.wav"> </audio> </audio></td>
   </tr>
</table>

### LJSpeech
1. F1, especially as no more time is occupied, or cost incurred, in casting, setting, or printing beautiful letters
2. F2, fourteen sixty-nine, fourteen seventy.


<table>
   <tr>
      <td>Utterance</td>
      <td>Source</td>
      <td>Convert</td>
   </tr>
   <tr>
      <td>F1_LJ001-0045</td>
      <td><audio id="audio" controls="" preload="none"> <source id="LF1_s" src="converted_sample/LJSpeech/F1/1_LJ001-0045.wav"> </audio> </td>
      <td><audio id="audio" controls="" preload="none"> <source id="LF1_t" src="converted_sample/LJSpeech/F1/1_LJ001-0012_generated_e2e"> </audio></td>
   </tr>
   <tr>
      <td>F2_LJ001-0045</td>
      <td><audio id="audio" controls="" preload="none"> <source id="LF2_s" src="converted_sample/LJSpeech/F2/3_LJ001-0045.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="LF2_t" src="converted_sample/LJSpeech/F2/3_LJ001-0045_generated_e2e.wav"> </audio></td>
   </tr>
</table>

### LJSpeech
1. F1, 购房节奏暂时性放缓.
2. M2, 目前房地产整体形势不是特别景气.


<table>
   <tr>
      <td>Utterance</td>
      <td>Source</td>
      <td>Convert</td>
   </tr>
   <tr>
      <td>F1_BAC009S0234W0141</td>
      <td><audio id="audio" controls="" preload="none"> <source id="AF1_s" src="converted_sample/AISHELL/F1/3_BAC009S0234W0141.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="AF1_t" src="converted_sample/AISHELL/F1/3_BAC009S0234W0141_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>F2_BAC009S0091W0160</td>
      <td><audio id="audio" controls="" preload="none"> <source id="AM1_s" src="converted_sample/AISHELL/M1/5_BAC009S0091W0160.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="AM1_t" src="converted_sample/AISHELL/M1/5_BAC009S0091W0160_generated_e2e.wav"> </audio></td>
   </tr>
</table>


### Wild
1. M1, 我国发展仍然处于重要战略机遇期，但
2. M2, food_and_medical_supplies.


<table>
   <tr>
      <td>Utterance</td>
      <td>Source</td>
      <td>Convert</td>
   </tr>
   <tr>
      <td>F1_kh_42_2</td>
      <td><audio id="audio" controls="" preload="none"> <source id="WM1_s" src="converted_sample/Wild/M1/1_kh_42_2.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="WM1_t" src="converted_sample/Wild/M1/1_kh_42_2_generated_e2e.wav"> </audio></td>
   </tr>
   <tr>
      <td>F2_SEF2_E10066</td>
      <td><audio id="audio" controls="" preload="none"> <source id="WM2_s" src="converted_sample/Wild/M2/3_trumps.wav"> </audio></td>
      <td><audio id="audio" controls="" preload="none"> <source id="WM2_t" src="converted_sample/Wild/M2/3_trumps_generated_e2e.wav"> </audio></td>
   </tr>
</table>
