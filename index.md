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
   <tr>
      <td></td>
   </tr>
</table>






### Markdown

Markdown is a lightweight and easy-to-use syntax for styling your writing. It includes conventions for

```markdown
Syntax highlighted code block

# Header 1
## Header 2
### Header 3

- Bulleted
- List

1. Numbered
2. List

**Bold** and _Italic_ and `Code` text

[Link](url) and ![Image](src)
```

For more details see [GitHub Flavored Markdown](https://guides.github.com/features/mastering-markdown/).

### Jekyll Themes

Your Pages site will use the layout and styles from the Jekyll theme you have selected in your [repository settings](https://github.com/BrightGu/SingleVC/settings/pages). The name of this theme is saved in the Jekyll `_config.yml` configuration file.

### Support or Contact

Having trouble with Pages? Check out our [documentation](https://docs.github.com/categories/github-pages-basics/) or [contact support](https://support.github.com/contact) and we’ll help you sort it out.
