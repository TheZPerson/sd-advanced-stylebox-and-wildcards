# sd-forge-advanced-stylebox-and-widlcard
Extension for SD Forge Neo, it is made of two components.

First component "Live Edit" which creates new UI with expanded Style box with lot of QoL features compared to regular style selector box. 
Second Component is Style Wildcards, which let's user use wildcards by picking to-be randomized styles from Dropdown box.

##Live Edit
How styles affect the image are often affected by other loras, alternative models or just AIs mood.
I frequently find it nesessary to tweak styles to get the result I want, but to do that I must either apply the style to the prompt box or permanently modify the style. 
With this Live Edit you can select Styles and edit them on fly, without cluttering the the main prompt box or losing the original style. 


Recommended!
If you wan't more space for the UI, I recommend using "Insert Tool after..."´-options with "neg_prompt_row" as value.
This will put the UI under the main prompt boxes.
Additionally I recommend setting User Interface>UI Alternatives>Prompt Layout to "Compact".
This way Gallery/Result Image i will be right below the Generate-Button, reducing need to scroll. 
Downside of this is that built-int Style box gets moved inside Accordions. 

The basic behaviour is same as the default style dropdown, so this supports {prompt} syntax and comment removal. 
