
# sd-forge-advanced-Stylebox-and-Wildcards
Extension for SD Forge Neo, it is made of two components.

First component **Live Edit** which creates customized Style Drodowns with lot of QoL features compared to regular Style Dropdown. <br/>

Second Component is **Style Wildcards**, which is a whole new way to use wildcards by simply selecting Styles from a Dropdown.

<img height="800" alt="2026-07-28 211650" src="https://github.com/user-attachments/assets/c88cd562-bd75-4a6d-9a14-fe03f1e596eb" /><br/>
## Main Features

+ Edit and use Dummy version of Styles, without losing the originals.
+ Easily convert Styles to Wildcards
+ Apply Styles to the prompt at custom insert points.
+ Extract only specific parts of a Style (Sections). 
+ Custom Filters for individual Styles-Dropdowns.
+ Highly Customizable
+ Automatic Style sorting

## Install

Open your WebUIs Extension-Tab. Go to Install from URL tab > Paste this repo's URL into the first field > Click Install

Or 

Manually clone this repo into your extensions folder:

`git clone https://github.com/TheZPerson/sd-advanced-stylebox-and-wildcards`

To ensure maximum compatibility, this extension should run as early as possible. At least before any other extension that use the prompt.
Easiest way to do this is rename the extensions install folder to something like: 0-sd-advanced-Stylebox-and-wildcards

> [!WARNING]
> On Forge Classic I noticed a bug, that causes WebUI to not load Setting-Slider defaults correctly.<br/>
> To get around this, I have for now set default number of both elements to 1. To add more,  go to the settings and adjust  "Number of Live Editor" and "Number of Wildcards" to higher values. 


## Live Edit
I am heavy user of Styles in WebUI, but they come with certain incoveniences. 

How Styles affect the image are often affected by other loras, alternative models or just AIs mood.<br/>
I frequently find it necessary to tweak Styles to get the result I want, but to do that I must either the apply the Style to the prompt box or permanently modify the Style. <br/>

With Live Edit you can select Styles and edit them on fly, without cluttering the the main prompt box or losing the original Style. 

Each Style will appear in their own textbox, and it is the content of these textboxes that get applied to the prompt, instead of the original Style.<br/>

You can use Apply-button (🖫) to save the Style, <ins>this will override the original Style.</ins> <br/>
You can create a new Style by changing the name of the Style with ✎-button before saving with (🖫). 

The maximum number of Live Edits is 4. You can change the amount of visible Live Edits in the Extension settings.

## Wildcards
You can select any Styles that you want with Wildcard-Dropdown and the script will automatically apply one of the randomly into the prompt.<br/>

If you have **Dropout-mode** enabled in Extension setting, the same Style can only be used once per process. <br/>
When script chooses a Style it automatically removes that Style from other wildcards.<br/>

Result of the Wildcards are tied to the seed of the process. <br/>
Keep in mind that if you do any changes to the prompt, Wildcards or Live Edits between first-pass and hires fix, those changes will apply to the hires fix.

The maximum number of wildcards is 6. You can change the amount of visible Wildcards in the Extension settings.

## What are Sections?
In vanilla WebUI, if Style contains {prompt} keyword, the UI will place the main prompt in that position, effectively splitting the Style in 2 parts with main prompt in the middle.<br/>

This Extension takes use of that same functionality. If a Style contains {prompt} or original {section} keywords, the Style gets separated to Sections <br/>

In Live Edit and Wildcards Extra Settings, you can then pick which Sections you want to apply to the prompt. <br/>

My most used use-case for this is when using Character-Styles with loras. <br/>
By seperation loras/Style and prompts to seperate Sections, I can easily use only the Character prompt without its default Style/loras.

<details>
  
  
<summary>Example</summary>


Style: **masterpiece <lora:superMario:1>, 3d, <lora:eyesize:5> {prompt} mario, blue overall, blue eyes, mustache, red hat** <br/>


| Section  |   Prompt   | 
|  :---         |     :---:      | 
| 0 |  masterpiece <<lora:superMario:1>>, 3d, <<lora:eyesize:5>>   |
| 1     |  mario, blue overall, blue eyes, mustache   | 

</details>




## {section} vs. {prompt}

If you use a Style that has multiple {prompt} keywords inside the vanilla Style-Dropdown, the main prompt gets duplicated over every {prompt} keyword separately.<br/>

This issue can be averted by using {section} keyword instead. <br/>

When using {section}-keyword inside vanilla Style-Dropdown, these Styles are treated like normal un-splitted Styles and {section} -keywords get removed.<br/>

In eyes of the extension both {prompt} and {section} are interchangeable.


<details>

<summary>Example</summary>

Here is example of what happens when a Style with multiple {prompt}/{section} gets used inside a vanilla Style Dropdown.<br/>
**Keep in mind that this does not apply to the extension itself!** 

Main Prompt: <ins> **An awesome prompt with quality tags and stuff.** </ins>

| Style A | Style B |
|  :---         |     :---:      | 
|Style of all {prompt} character prompts that you need {prompt} and whatever else you want.  | Style of all {section} character prompts that you need {section} and whatever else you want.|

| Result A| Result B |
|  :---         |     :---:      | 
|Style of all,  <ins>**An awesome prompt with quality tags and stuff.**</ins>  ,character prompts that you need  <ins>**An awesome prompt with quality tags and stuff.** </ins> and whatever else you want.  |  <ins>**An awesome prompt with quality tags and stuff.**</ins>, Style of all character prompts that you need and whatever else you want. |

</details>

## Insert Points

In case you are using something like Forge Couple or Regional Prompter, you can use **Insert Points**-functionality to inject the Live Edits and Wildcards to arbitrary points in your main prompt. 
For example you can randomize Styles and characters with wildcards. <br/>

Same Insertion Point can be used multiple times inside the same prompt and also by multiple Wildcards at the same time. 

Here is example Setup. (In my case, I must use Section 1 for character to avoid applying loras):

| Prompt | Setup|
|  :---         |     :---:      | 
|##Style##<br/>{your_seperator}<br/>##Character1##<br/>{your_seperator}<br/>##Character2##<br/>|<img width="1287" height="467" alt="2026-07-29 001454" src="https://github.com/user-attachments/assets/56f45f0b-a5ab-4d04-b63e-a5aff2de970c" />|






## UI Recommendation
If you want more space for the UI, I recommend using "UI Insertion"-options with "neg_prompt_row" as value.<br/>
This will put the UI under the main prompt boxes.

<img width="1016" height="190" alt="2026-07-28 232553" src="https://github.com/user-attachments/assets/148ba12c-1652-474b-b8c9-552f33a08e9d" />


Additionally I recommend setting User Interface>UI Alternatives>Prompt Layout to "Compact".<br/>
(This setting may appear different on non-Neo forks!)

<img width="637" height="217" alt="2026-07-28 233154" src="https://github.com/user-attachments/assets/733c1c23-ee4c-4a02-bb6b-400a7874a112" />


This way Gallery/Result Image will be right below the Generate-Button, reducing excessive scrolling. <br/>





Downside of this set-up is that vanilla Style boxes are moved down inside Accordions. 



<details>

<summary>Example</summary>


<img width="2455" height="1142" alt="2026-07-28 232358" src="https://github.com/user-attachments/assets/a31b557b-a471-479e-95cd-71052557140a" />

</details>

## About Batch Sizes
Unfortunately only way I found to make Batch Size > 1 to run reliably was to cheat.
Instead of batch using a different seed, the script makes all images of the batch to use the same seed and force UI to use variations instead. 
If user doesn't already have variations enabled, script sets variations strength to 1.
However, even at variations strength of 1, the images can look quite similar within the batch.

The main reason for this problem is that, if wildcards inside a batch result in different set of loras, only one of sets gets actually loaded.
This workaround is not perfect, so if you run into issues I advice just using Batch Count > 1 instead.

Alternatively if you know for the fact that this won't cause issues for you, you can disable this workaround from Extensions settings.
