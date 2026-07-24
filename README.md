# sd-forge-advanced-stylebox-and-widlcard
Extension for SD Forge Neo, it is made of two components.

First component "Live Edit" which creates new UI with expanded Style box with lot of QoL features compared to regular style selector box. 
Second Component is Style Wildcards, which let's user use wildcards by picking to-be randomized styles from Dropdown box.

##Live Edit
How styles affect the image are often affected by other loras, alternative models or just AIs mood.
I frequently find it nesessary to tweak styles to get the result I want, but to do that I must either apply the style to the prompt box or permanently modify the style. 
With this Live Edit you can select Styles and edit them on fly, without cluttering the the main prompt box or losing the original style. 


What are Sections?
In vanilla WebUI if style contains {prompt} string, the UI will split the main prompt is but in that position, effectively splitting the style in 2 parts.
This Extension takes use of that same functionality. If style contains {prompt} or original {section} keywords ,style gets seperated to seperated to Sections, 1 Section per {prompt}/{section}.
In Live Edit and wildcards Extra Settings, you can then pick which Sections you want to apply to the prompt.

{section} vs. {prompt}

If you use a Style that has multiple {prompt} keywords inside the vanilla Style-dropdown, the main propmt gets duplicated over every {prompt} keyword seperately.
If you decide to use {section} instead, remember that style won't be split if it comes from vanilla Style-dropdown. In eyes of the extension both {prompt} and {section} are interchangeable.





Recommended!
If you wan't more space for the UI, I recommend using "Insert Tool after..."´-options with "neg_prompt_row" as value.
This will put the UI under the main prompt boxes.
Additionally I recommend setting User Interface>UI Alternatives>Prompt Layout to "Compact".
This way Gallery/Result Image i will be right below the Generate-Button, reducing need to scroll. 
Downside of this is that built-int Style box gets moved inside Accordions. 

The basic behaviour is same as the default style dropdown, so this supports {prompt} syntax and comment removal. 

About Batch Sizes
Unfortunately only way I found to make Batch Size > 1 to run reliably was to cheat.
Instead of batch using a different seed, the script makes all images of the batch to use the same seed and force UI to use variations instead. 
If user doesn't already have variations enabled, script sets variations strength to 1.
However, even at variations strength of 1, the images can look quite similar within the batch.

The main reason for this problem is that if wildcards inside a batch result in different set of loras only one of sets gets actually loaded.
This workaround is not perfect, so if you run into issues I advice just using Batch Count > 1 instead.

Alternatively if you know for the fact that this won't cause issues for you, you can disable this workaround from Extensions settings.
