# sd-forge-advanced-stylebox-and-widlcard
Extension for SD Forge Neo, it is made of two components.

First component "Live Edit" which creates new UI with expanded Style Drodowns (max. 4)  with lot of QoL features compared to regular style selector box. 
Second Component is Style Wildcards, which let's user use wildcards by picking to-be randomized styles from Dropdown box (max. 6).

##Main Features

+Edit and use Dummy version of styles, without losing the originals.
+Easily convert styles to Wildcards
+Send styles to prompt the at custom insert points.
+Extract only specific parts of the style. 
+Custom Filters for individual Styles-dropdowns.
+Highly Customizable
+Automatic style sorting


To ensure maximum compatibility, this extension should run as early as possible. At least before any other extension that modifies prompts.
Easiest way to do this is rename the extensions install folder to something like: 0-sd-advanced-stylebox-and-wildcards


##Live Edit
How styles affect the image are often affected by other loras, alternative models or just AIs mood.
I frequently find it nesessary to tweak styles to get the result I want, but to do that I must either apply the style to the prompt box or permanently modify the style. 
With Live Edit you can select Styles and edit them on fly, without cluttering the the main prompt box or losing the original style. 

Each style appears in their own textbox, and it is content of these textboxes that get applied to the prompt instead of the original style.
The maximum number of Live Edits is 4. Yo can change the amount of visible Live Edits in Extension settings.

##Wildcards
You can select any Styles that you want with Wildcard-dropdown and the script will automatically apply one of the randomly into the prompt.
If you have Dropdown-mode enabled in Extension setting, the same style can only be used once per process. When script chooses a style it automatically removes that style from other wildcards.
The maximum number of wildcards is 6.

##What are Sections?
In vanilla WebUI if style contains {prompt} string, the UI will place the main prompt in that position, effectively splitting the style in 2 parts with main prompt in the middle.
This Extension takes use of that same functionality. If style contains {prompt} or original {section} keywords ,style gets separated to Sections, 1 new Section per {prompt}/{section}.
In Live Edit and wildcards Extra Settings, you can then pick which Sections you want to apply to the prompt.

##{section} vs. {prompt}

If you use a Style that has multiple {prompt} keywords inside the vanilla Style-dropdown, the main propmt gets duplicated over every {prompt} keyword seperately.
This issue can be averted by using {section} keyword instead. When using {section}-keyword inside vanilla Style-dropdown, these styles are treated like normal un-splitted styles and {section} -keywords get removed.
In eyes of the extension both {prompt} and {section} are interchangeable.

Main Prompt: An awesome prompt with quality tags and stuff.

Style A: Style of all {prompt} character prompts that you need {prompt} and whatever else you want

Style B: Style of all {section} character prompts that you need {section} and whatever else you want.

Result:

Result A: Style of all An awesome prompt with quality tags and stuff. character prompts that you need An awesome prompt with quality tags and stuff. and whatever else you want

Result B: Style of all character prompts that you need and whatever else you want. An awesome prompt with quality tags and stuff



##Recommended!
If you want more space for the UI, I recommend using "Insert Tool after..."´-options with "neg_prompt_row" as value.
This will put the UI under the main prompt boxes.
Additionally I recommend setting User Interface>UI Alternatives>Prompt Layout to "Compact".
This way Gallery/Result Image i will be right below the Generate-Button, reducing need to scroll. 
Downside of this is that built-int Style box gets moved inside Accordions. 

The basic behaviour is same as the default style dropdown, so this supports {prompt} syntax and comment removal. 

##About Batch Sizes
Unfortunately only way I found to make Batch Size > 1 to run reliably was to cheat.
Instead of batch using a different seed, the script makes all images of the batch to use the same seed and force UI to use variations instead. 
If user doesn't already have variations enabled, script sets variations strength to 1.
However, even at variations strength of 1, the images can look quite similar within the batch.

The main reason for this problem is that, if wildcards inside a batch result in different set of loras, only one of sets gets actually loaded.
This workaround is not perfect, so if you run into issues I advice just using Batch Count > 1 instead.

Alternatively if you know for the fact that this won't cause issues for you, you can disable this workaround from Extensions settings.
