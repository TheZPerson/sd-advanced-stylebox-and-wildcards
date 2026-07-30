from numpy import insert

import re,random,json
import gradio as gr
from modules import shared, script_callbacks, scripts, styles,ui_prompt_styles
from modules.processing import StableDiffusionProcessingTxt2Img
from modules.ui_components import InputAccordion,ToolButton

from ss_helpers.ss_helperclasses import ST_arguments,Split_prompt

# variables
extn_name = "Style Select"
extn_id = "st_public"

# regexes
re_prompt = re.compile(r",? *\{(?:prompt|section)\} *,? *", re.I)
re_section = re.compile(r",? *\{section\} *,? *", re.I)

def strip_comments(text: str) -> str:
    
    if getattr(shared.opts, "enable_prompt_comments",False) is False:
        return text

    # multi line comment (/* */)
    text = re.sub(r"\/\*.*?\*\/", "", text, flags=re.DOTALL)
    # single line comment (# | //)
    text = re.sub(r"[^\S\n]*(\#|\/\/).*", "", text)

    return text


def setup_components_before(component: gr.components.Component, **kwargs):
     if StyleSelect.insert_method == "Before":
        setup_components(kwargs.get("elem_id", None))


def setup_components_after(component: gr.components.Component, **kwargs):
     if StyleSelect.insert_method == "After":
        setup_components(kwargs.get("elem_id", None))


def setup_components(_id : str):
    """Setup where to insert the UI"""

    if _id == None or StyleSelect.insert_id == "":
        return
   
    # Create t2i-version of UI
    if _id == f"txt2img_{StyleSelect.insert_id}" and StyleSelect.UI_CACCHE[False] == None:
        StyleSelect.UI_CACCHE[False] = StyleSelect.createUI(False)

    # Create i2i-version of UI
    if _id == f"img2img_{StyleSelect.insert_id}" and StyleSelect.UI_CACCHE[True] == None:
        StyleSelect.UI_CACCHE[True] = StyleSelect.createUI(True)


script_callbacks.on_after_component(setup_components_after)
script_callbacks.on_before_component(setup_components_before)

# class
class StyleSelect(scripts.Script):

    sorting_priority = getattr(shared.opts, f"{extn_id}_sortOrder",-997)
    insert_id = getattr(shared.opts, f"{extn_id}_insertUI_ID","")
    insert_method = getattr(shared.opts, f"{extn_id}_insertUI_method","")
    styleCache = None

    styleApplySetting =  getattr(shared.opts, f"{extn_id}_promptApply","Before Main Prompt")

    UI_CACCHE  = {True:None,False:None}

    #´Callbacks for 'Send To Prompt'-buttons need to be set after UI has been fully created, for this purposes we store needed information in this dictionary.
    STYLE_DROPDOWNS = {True:[],False:[]}

    def __init__(self):
        super().__init__()

        #Fill the StyleCacche for the first time
        if StyleSelect.styleCache is None:
            StyleSelect.createCacchedStyles()

    def title(self):
        return extn_name



    def RegisterStyleDropdownCallbacks(is_img2img):
        for le in StyleSelect.STYLE_DROPDOWNS[is_img2img]:

            if le[2] is None:
                continue

            if is_img2img:
                le[2].click(StyleSelect.RefreshAll_i2i, inputs = [], outputs = StyleSelect.GetDropdowns(True) )
            else:
                le[2].click(StyleSelect.RefreshAll_t2i, inputs = [], outputs = StyleSelect.GetDropdowns(False))

    def createCacchedStyles():
        """To reduce potential lag, cacche all used style lists."""
        
        
        allStyles = [shared.prompt_styles.no_style]

        sort = getattr(shared.opts, f"{extn_id}_auto_sort",True) 
        
        tmp = list(shared.prompt_styles.styles.values())

      

        if sort:
            #Remove .csv names
            tmp =[style for style in tmp if not "------" in style.name]
            
            tmp.sort()
             
            

        allStyles = [style.name for style in (allStyles + tmp)]


        StyleSelect.styleCache = {}


        #Create key-value pairs to make readign settings easier
        filter_kv = {}

        for i in range(ST_arguments.total_live_Edits):
            filter_kv[f"Live{i+1}"] = f"{extn_id}_liveEdit_filter{i+1}"

        for i in range(ST_arguments.total_wildcards):
            filter_kv[f"WC{i+1}"] = f"{extn_id}_wildcards_filter{i+1}"
        
        def addFilter(key,filterOption):
            StyleSelect.styleCache[key] = [style for style in allStyles if getattr(shared.opts, filterOption,"").lower() in style.lower() or "none" in style.lower()]
        
        for x,y in filter_kv.items():
           addFilter(x,y)
        

    
    def RefreshAll_t2i():
        #Refresh all t2i Style Selectors
        StyleSelect.createCacchedStyles()

        returnValues = []

        for le in StyleSelect.STYLE_DROPDOWNS[False]:
            returnValues.append(gr.Dropdown.update(choices=StyleSelect.styleCache[le[1]]))

        return returnValues    
    

    def RefreshAll_i2i():
        #Refresh all i2i Style Selectors
        StyleSelect.createCacchedStyles()

        returnValues = []
        for le in StyleSelect.STYLE_DROPDOWNS[True]:
            returnValues.append(gr.Dropdown.update(choices=StyleSelect.styleCache[le[1]]))

        return returnValues

    def GetDropdowns(is_i2i):
        return [item[0] for item in StyleSelect.STYLE_DROPDOWNS[is_i2i]]

    def show(self, is_img2img: bool):
        return scripts.AlwaysVisible
             
    def ui(self, is_img2img):
        t_id = getattr(shared.opts, f"{extn_id}_insertUI_ID","")

        #if UI's aren't created in setup_components, we create them here instead
        if t_id == "" and StyleSelect.UI_CACCHE[is_img2img] == None:
            StyleSelect.UI_CACCHE[is_img2img] = StyleSelect.createUI(is_img2img)

        return StyleSelect.UI_CACCHE[is_img2img]

    def ornagizeLiveEdits(numbervisible,orientation,is_img2img,liveEdits):

        def createSimple():
             with gr.Column(scale=1):
                liveEdits[0].createLiveEdit(is_img2img, True)
                liveEdits[1].createLiveEdit(is_img2img)
                liveEdits[2].createLiveEdit(is_img2img)
                liveEdits[3].createLiveEdit(is_img2img)

        if orientation == "Vertical":

            if getattr(shared.opts, f"{extn_id}_max_le_per_row",2) == 4:
               with gr.Row(equal_height=False, variant="compact"):
                    liveEdits[0].createLiveEdit(is_img2img, True)
                    liveEdits[1].createLiveEdit(is_img2img)
                    liveEdits[2].createLiveEdit(is_img2img)
                    liveEdits[3].createLiveEdit(is_img2img)
                    return

            if numbervisible == 1:

                createSimple()

            elif numbervisible == 2 :

                container = gr.Row(variant="compact") if getattr(shared.opts, f"{extn_id}_max_le_per_row",2) == 2 else gr.Column()

                with container:
                    
                    liveEdits[0].createLiveEdit(is_img2img, True)
                    
                    liveEdits[1].createLiveEdit(is_img2img)
                 
                liveEdits[2].createLiveEdit(is_img2img)
                liveEdits[3].createLiveEdit(is_img2img)

            elif numbervisible == 3:
                  container = gr.Row(equal_height=False, variant="compact") if getattr(shared.opts, f"{extn_id}_max_le_per_row",2) > 1 else gr.Column()

                  with container:
                        liveEdits[0].createLiveEdit(is_img2img, True)
                        liveEdits[1].createLiveEdit(is_img2img)

                        if getattr(shared.opts, f"{extn_id}_max_le_per_row",2) == 3:
                            liveEdits[2].createLiveEdit(is_img2img)

                  if getattr(shared.opts, f"{extn_id}_max_le_per_row",2) == 2:
                      with gr.Row():
                            liveEdits[2].createLiveEdit(is_img2img)
                  liveEdits[3].createLiveEdit(is_img2img)

            elif numbervisible == 4:
                  container1 = gr.Row(variant="compact") if getattr(shared.opts, f"{extn_id}_max_le_per_row",2) >= 2 else gr.Column()
                  container2 = gr.Row(variant="compact") if getattr(shared.opts, f"{extn_id}_max_le_per_row",2) >= 2 else gr.Column()

                  with container1:
                    liveEdits[0].createLiveEdit(is_img2img, True)
                    liveEdits[1].createLiveEdit(is_img2img)

                    if getattr(shared.opts, f"{extn_id}_max_le_per_row",2) == 3:
                        liveEdits[2].createLiveEdit(is_img2img)

                  with container2:
                    if getattr(shared.opts, f"{extn_id}_max_le_per_row",2) == 2:
                        liveEdits[2].createLiveEdit(is_img2img, True)
                    liveEdits[3].createLiveEdit(is_img2img)
            else:
                 createSimple()
        else:
             createSimple()

    def createUI(is_img2img):

             with InputAccordion(True, label='Style Select') as ss_enable:

                orientation = getattr(shared.opts,f"{extn_id}_orientation","Vertical")
                container = gr.Column() if orientation == "Vertical" else gr.Row(variant="compact")


                with container:

                    num_liveEdits = getattr(shared.opts, f"{extn_id}_visible_live_edits",1)
                    with InputAccordion(False, label='Live Edits', visible = num_liveEdits > 0 ) as liveEdit_enable:
                   
                        liveEdits = []

                        for i in range(ST_arguments.total_live_Edits):
                            liveEdits.append(LiveEdit(is_img2img, filterkey = f"Live{i+1}", label=getattr(shared.opts, f"{extn_id}_liveEdit_label{i+1}",f"{i+1}") , visible = num_liveEdits >= i+1,index=i+1))


                        StyleSelect.ornagizeLiveEdits(num_liveEdits,orientation,is_img2img,liveEdits)


                    def createWildcard(index, filterkey, i_label):

                         show = getattr(shared.opts, f"{extn_id}_visible_wildcards",0) >= index 

                         with gr.Column(scale=1, visible = show,variant="compact" ):
                             with gr.Row(visible = True):
                                 refresh_btn = ToolButton('🗘', elem_id=f"ss_wc_rfr_wc_{filterkey}{index}", tooltip = "Refresh Styles", visible = (index == 1) ,elem_classes=[f"ss_styleresresh_btn"] )
                                 drp =gr.Dropdown(choices= StyleSelect.styleCache[filterkey],elem_id= f"st_wc_{filterkey}_{index}",multiselect=True,label=f'🎲 {i_label} ({index})',allow_custom_value= False)

                             with gr.Accordion("Extra Settings", open = False,  visible = getattr(shared.opts, f"{extn_id}_extras_wc",True)):
                                 with gr.Row(visible = True):
                                    skipNegative = gr.Checkbox(label = f"Skip Negative {index}",elem_id=f"ss_wc_neguse_{filterkey}{index}",value = False,tooltip = "Do not use Negative Prompt?")
                                    insert = gr.Text(label = f"Insert Point {index}",elem_id=f"ss_wc_ins_{filterkey}{index}", value = "", placeholder = "Insert Point", show_label = True, max_lines= 1, lines = 1 ,tooltip = "Replace this string in main prompt with Live Edits positive prompt") 
                                    sect = gr.Text(show_label= True, label=f"Sections {index}", elem_id=f"ss_wc_sect_{filterkey}{index}",value ="",placeholder = "0,1,2 empty = all",max_lines = 1, tooltip = "Pick which Sections (seperated by {prompt}) to apply to the prompt)")
                                    
                               
                         if show:
                            StyleSelect.STYLE_DROPDOWNS[is_img2img].append([drp,filterkey,refresh_btn])
                     
                         return [drp,insert,sect,skipNegative]

                    wildcards = []
                    with InputAccordion(False, label='Wildcards', visible =  getattr(shared.opts, f"{extn_id}_visible_wildcards",1) > 0) as wildcards_enabled:
                         with gr.Row(visible = True):
                            for i in range(ST_arguments.total_wildcards):
                                wildcards.extend(createWildcard(i+1, f"WC{i+1}",getattr(shared.opts, f"{extn_id}_wildcards_label{i+1}",f"{i+1}")))


                unpacked  = liveEdits[0].unpack() + liveEdits[1].unpack() +liveEdits[2].unpack()+liveEdits[3].unpack()

                outputlist = [ss_enable,         
                    liveEdit_enable,
                    wildcards_enabled]+wildcards+unpacked
                    

             StyleSelect.RegisterStyleDropdownCallbacks(is_img2img)

             return outputlist

    def randomSelection(self, selection, rand):
            """Takes a List of options and returns random element"""
            if selection is None:
                return "None"

            if len(selection) == 0:
                return "None"

            if not isinstance(selection, list):
                return selection 
    
            copyofinput = list(selection)
            rand.shuffle(copyofinput)
              
            return copyofinput[0]

    
    def process(self, p,*args):

        #Remove section tags, they are probably from default Style box or user prompt.
          batch_size = p.batch_size
          for b_idx in range(p.n_iter):

                for s_offs in range(batch_size):

                    s_idx = b_idx * batch_size + s_offs

                    p.all_prompts[s_idx]=re.sub(re_section," ",p.all_prompts[s_idx])


          if args[0] is False or hasattr(p, "_ad_inner"):

              return

          StyleSelect.styleApplySetting =  getattr(shared.opts, f"{extn_id}_promptApply","Before Main Prompt")

          st_args = ST_arguments(args)

          def parse_prompt(inputPrompt,input_negative,seed):

              #Collection of styles chosen by boxes
        
              rand = random.Random(seed)
              collected_negative = []           
              all_insertpoints = []

              randomizedwithInsert = st_args.wildcards
              stylesAplliedToNegative = []

              selectedwildcards = []

              def ApplyLiveEdit(mainprompt, le : ST_arguments.LiveEditInfo ):

                 if le.enable is False:
                     return mainprompt

                 inserpointExists = (le.insertpoint in mainprompt) if (le.insertpoint != "" and le.insertpoint != None) else False

                 prompt = Split_prompt(inputString=le.positive, negative= le.negative)


                 if inserpointExists:

                      output = prompt.getSegments(le.section)


                      mainprompt = re.sub(le.insertpoint, le.insertpoint+output,mainprompt)  

                      #To make inserpoints re-usable, we clear them at the end using this list
                      all_insertpoints.append(le.insertpoint)
                      if not le.skipNegative:
                        collected_negative.append(le.negative)

                 else:

                     mainprompt = prompt.applyToPrompt(mainprompt,le.section, StyleSelect.styleApplySetting)

                     if not le.skipNegative:
                        collected_negative.append(prompt.neg)


                 return mainprompt
             


              def clearInsertPoints(allInserPoints, prompt):
                if len(allInserPoints) == 0:
                      return prompt

                # Join words with '|' (OR operator) and escape special characters
                pattern = "|".join(map(re.escape, allInserPoints))

                # Substitute matches with an empty string
                return  re.sub(pattern, "", prompt)



              def ApplyWildcards(mainprompt, wildcard, inserpoint, section, skipneg):

                 if wildcard == None:
                    return mainprompt


                 inserpointExists = (inserpoint in mainprompt) if (inserpoint != "" and inserpoint != None) else False


                 
                 wc = list(wildcard)

                 #if wildcards are set to dropout mode, remove all previously selected wildcards from the list by creating temporary clone
                 if getattr(shared.opts, f"{extn_id}_wc_dropout",False) is True:
                     for prev_wc in selectedwildcards:
                         if prev_wc in wildcard:                     
                              wc.remove(prev_wc)


                 selectedStyle = self.randomSelection(wc,rand)


                 if selectedStyle != "None":

                         selectedwildcards.append(selectedStyle)

                         prompt = Split_prompt(inputStyle=selectedStyle)

                         if inserpointExists:

                             mainprompt = re.sub(inserpoint,inserpoint+prompt.getSegments(section),mainprompt)  
                              #To make inserpoints re-usable, we clear them at the end using this list
                             all_insertpoints.append(inserpoint)
                         else:

                             mainprompt = prompt.applyToPrompt(mainprompt,section, StyleSelect.styleApplySetting)

                         if skipneg is False:
                            collected_negative.append(prompt.neg)

                 return mainprompt

              if st_args.liveEdit_enable is True:
                  for le in st_args.liveEdits:
                    inputPrompt= ApplyLiveEdit(inputPrompt,le)

              if st_args.wildcards_enable is True:
                for wc in randomizedwithInsert:
                  inputPrompt = ApplyWildcards(inputPrompt, wc[0],wc[1],wc[2],wc[3])

              negative = input_negative +(",".join(collected_negative))
          
              inputPrompt = clearInsertPoints(all_insertpoints,inputPrompt)
            
              return strip_comments(inputPrompt), strip_comments(negative)

          is_t2i = isinstance(p, StableDiffusionProcessingTxt2Img)
          hr_enabled = p.enable_hr if is_t2i else True
          batch_size = p.batch_size

          #Implement dirty workaround to get Batch Size>1 working
          forceSeed = getattr(shared.opts, f"{extn_id}_enable_force_same_seed",True) if batch_size > 1 else False
            
          if forceSeed and p.subseed_strength == 0:
              p.subseed_strength = 1
              p.seed_enable_extras = True
              
               #Loop throught each batch and make each image in batch have same seed
              for b_idx in range(p.n_iter):
                for s_offs in range(batch_size):
                    s_idx = b_idx * batch_size + s_offs
                    p.all_seeds[s_idx] =p.all_seeds[b_idx * batch_size]


          for b_idx in range(p.n_iter):

            for s_offs in range(batch_size):

                s_idx = b_idx * batch_size + s_offs  # offset of the prompt in all_prompts

                p.all_prompts[s_idx],p.all_negative_prompts[s_idx]= parse_prompt(p.all_prompts[s_idx], p.all_negative_prompts[s_idx], p.all_seeds[s_idx])
                                  
                if is_t2i and hr_enabled:
                    p.all_hr_prompts[s_idx],  p.all_hr_negative_prompts[s_idx]= parse_prompt(p.all_hr_prompts[s_idx],  p.all_hr_negative_prompts[s_idx], p.all_seeds[s_idx])


# register callbacks
def on_ui_settings():
    section = (extn_id, extn_name)
    
    if getattr(shared.opts, f'enable_prompt_comments',None) is None:
        shared.opts.add_option(f'enable_prompt_comments', shared.OptionInfo(True, "Remove Comments", section=section))  

    shared.opts.add_option( f"{extn_id}_orientation",  shared.OptionInfo(
        default="Vertical",
        label="Orientration of Live Edits and Wildcards",

        component=gr.Dropdown,
        component_args=
        {
            "choices": ("Vertical","Horizontal"),
        },
        section=section
    ).needs_reload_ui())

    shared.opts.add_option( f"{extn_id}_promptApply",  shared.OptionInfo(
        default="After Main Prompt",
        label="Apply Resulting Prompt?",

        component=gr.Dropdown,
        component_args=
        {
            "choices": ("After Main Prompt","Before Main Prompt"),
        },
        section=section
    ).needs_reload_ui())

    shared.opts.add_option(f"{extn_id}_auto_sort", shared.OptionInfo(False, "Sort Styles alphabetically?", section=section))  

    shared.opts.add_option(f"{extn_id}_enable_force_same_seed", shared.OptionInfo(True, " Implement Batch Size Fix ", section=section).info("Force-enable variation-mode when Batch size>1. Variation strength will be 1 if current value is 0  (Strongy Recommended to keep Enabled!"))

    shared.opts.add_option(f"{extn_id}_insertUI_ID", shared.OptionInfo("", "UI Insertion ID", section=section).info('Insert Tool before/after specific object by id. (Id for under the  main prompt is: neg_prompt_row)').needs_reload_ui())   

    shared.opts.add_option( f"{extn_id}_insertUI_method",  shared.OptionInfo(
        default="After",
        label="When above option is set, insert UI before/after the element",

        component=gr.Dropdown,
        component_args=
        {
            "choices": ("Before","After"),
        },
        section=section
    ))



    shared.opts.add_option(f"{extn_id}_sortOrder",shared.OptionInfo(default=-995,label="Extension Sort Order (Does nothing if above option is used)", component=gr.Number, component_args = {'precision':0},section=section).needs_reload_ui())

    shared.opts.add_option(f"{extn_id}_wc_dropout",shared.OptionInfo(default=False,label="Use Dropout mode for wildcards", component=gr.Checkbox,section=section).info("Ensures that same style cannot be selected by multiple wildcards."))

    shared.opts.add_option(f"{extn_id}_extras_le",shared.OptionInfo(default=True,label="Show Extra Options for Live Edits?", section=section).needs_reload_ui())

    shared.opts.add_option(f"{extn_id}_negative_in_extras", shared.OptionInfo(False, "Place Negative Prompts inside Live Edit Extra Settings? ", section=section).needs_reload_ui())    

    shared.opts.add_option(f"{extn_id}_extras_wc",shared.OptionInfo(default=True,label="Show Extra Options for Wildcards?", section=section).needs_reload_ui())

    shared.opts.add_option( f"{extn_id}_sending",  shared.OptionInfo(
        default="Disable Live Edit",
        label="Live Edit behaviour when sending style to prompt",

        component=gr.Dropdown,
        component_args=
        {
            "choices": ("Disable Live Edit","Clear Live Edit","Do Nothing"),
        },
        section=section
    ).needs_reload_ui())



    shared.opts.add_option(f'{extn_id}_remove_comments_sending', shared.OptionInfo(False, "Remove Comment when using Send to Prompt(⬆)-button?", section=section).info('Does nothing if global Remove Comment setting is False').needs_reload_ui())  

    shared.opts.add_option(f"{extn_id}_visible_live_edits",shared.OptionInfo(1,"Number of Live Editor", gr.Slider,{"minimum": 0, "maximum": ST_arguments.total_live_Edits, "step": 1},section=section).needs_reload_ui())

    shared.opts.add_option(f"{extn_id}_max_le_per_row",shared.OptionInfo(2,label="Max. Live edits per row",
            component=gr.Slider,component_args={"minimum": 1, "maximum": 4, "step": 1},section=section,).info('Only applies when orientation is set to Vertical').needs_reload_ui())

    shared.opts.add_option(f"{extn_id}_visible_wildcards",shared.OptionInfo(1,label="Number of Wildcards",
            component=gr.Slider,component_args={"minimum": 0, "maximum": ST_arguments.total_wildcards, "step": 1},section=section,).needs_reload_ui())


    for i in range(ST_arguments.total_live_Edits):
        shared.opts.add_option(f"{extn_id}_liveEdit_label{i+1}",shared.OptionInfo(default = f"Live Edit",label=f"Live Edit {i+1} Label",section=section).info('Changing this will make you lose current default values on this Live Edit').needs_reload_ui())    

        shared.opts.add_option(f"{extn_id}_liveEdit_filter{i+1}",shared.OptionInfo(default = "",label=f"Live Edit {i+1} Filter",
                component=gr.Text,component_args= {"max_lines": 1},section=section))    

  
    for i in range(ST_arguments.total_wildcards):
        shared.opts.add_option(f"{extn_id}_wildcards_label{i+1}",shared.OptionInfo(default = f"Wildcard",label=f"Wildcard {i+1} Label",
        component=gr.Text,component_args= {"max_lines": 1},section=section).info('Changing this will make you lose current default values on this Wildcard').needs_reload_ui())   
    
        shared.opts.add_option(f"{extn_id}_wildcards_filter{i+1}",shared.OptionInfo(default = "",label=f"Wildcards {i+1} Filter",
        component=gr.Text,component_args= {"max_lines": 1},section=section))  



   


script_callbacks.on_ui_settings(on_ui_settings)

class LiveEdit():

    def __init__(self,is_img2img, filterkey, label, visible, index):
        self.filterkey = filterkey     
        self.index = f"# {index}"
        self.label = f"🎨 {label}"
        self.visible = visible
        self.enable : gr.Accordion = None
        self.dropdown : gr.Dropdown = None
        self.positive: gr.Textbox = None
        self.negative: gr.Textbox= None

        self.skipNegative : gr.Textbox = None
        self.insertpoint : gr.Textbox = None
        self.section : gr.Text = None
        self.is_img2img = is_img2img


    def unpack(self):
        """Returns Components as list so that we can merge components to outputs in createUI"""
        return [self.enable,self.dropdown,self.positive,self.negative, self.skipNegative,self.insertpoint, self.section]


    def UpdateLiveEdit(self, selectedStyle, renameField):
        """Update UI values when Live Edit Dropdown selection has been changed"""

        #Empty UI elements if Selection is None or not a style.
        if selectedStyle == "None" or not selectedStyle in shared.prompt_styles.styles:
            return "","",""

        #Read actual prompt saved styles
        text = shared.prompt_styles.styles[selectedStyle].prompt
        negative = shared.prompt_styles.styles[selectedStyle].negative_prompt

        #Send prompts and selected style to components
        return text, negative, selectedStyle

    def createLiveEdit(self,is_img2img, create_refreshbutton = False):
            """Create the actual visual UI"""

            with InputAccordion(True, label=f"{self.label} ({self.index})" , visible = self.visible) as self.enable:
                with gr.Column():
                        with gr.Row(variant="compact",elem_classes=[f"ss_style_dp_row"]):              
                            refresh_btn = ToolButton('🗘', elem_id=f"ss_le_rfr_{self.filterkey}", tooltip = "Refresh Styles", visible = create_refreshbutton ,elem_classes=[f"ss_styleresresh_btn"])
                            self.dropdown = gr.Dropdown(choices= StyleSelect.styleCache[self.filterkey],multiselect=False,value = None,label=f"{self.label} {self.index}",show_label=False,allow_custom_value= True) 

                            with gr.Row(elem_classes=[f"ss_style_dp_row"]):
                        
                                clear_btn = ToolButton('x',elem_id=f"ss_le_clr_{self.filterkey}", tooltip = "Clear this Live Edit")
                            
                                if self.visible:
                                    StyleSelect.STYLE_DROPDOWNS[is_img2img].append([self.dropdown,self.filterkey,refresh_btn])
                               
                                send = ToolButton('⬆',  elem_id=f"ss_le_send_{self.filterkey}",  tooltip = "Send To Prompt")   
                                apply = ToolButton('🖫', elem_id=f"ss_le_app_{self.filterkey}",tooltip = "Save Style")
                                rename = ToolButton('➕',  elem_id=f"ss_le_rnm_{self.filterkey}",  tooltip = "Save as new")   

                        #Create hidden rename field
                        row = gr.Row(visible = False)
                        with row:                                    
                            liveEdit_rename_field = gr.Textbox(label='Rename')
                            renameHide = ToolButton('👁',elem_classes=["tool"], elem_id=f"ss_le_rnmhide_{self.filterkey}",tooltip = "Hide This Field. (Use 🖫-button to apply rename)")
                            apply2 = ToolButton('🖫', elem_id=f"ss_le_app_{self.filterkey}_2",tooltip = "Save Style")

                        self.positive = gr.Textbox(show_label= True, label=f"Positive {self.index}",show_copy_button=True, placeholder = "Positive Prompt" ,elem_classes=["sts_multiinput", "prompt"], elem_id=f"le_inpt_{self.filterkey}_pos")
                           
                        #Create negative prompt if user has not opted to put it in Extra Settings
                        if getattr(shared.opts, f"{extn_id}_negative_in_extras",False) is False:
                            self.negative = gr.Textbox(show_label= True,label=f"Negative {self.index}", show_copy_button = True, placeholder = "Negative Prompt" , elem_classes=["sts_multiinput", "prompt"], elem_id=f"le_inpt_{self.filterkey}_neg")

                        with gr.Accordion("Extra Settings", open = False, visible = getattr(shared.opts, f"{extn_id}_extras_le",True)):

                            #Create negative prompt if user has  opted to put it in Extra Settings
                            if getattr(shared.opts, f"{extn_id}_negative_in_extras",False) is True:
                                self.negative = gr.Textbox(show_label= True,label=f"Negative {self.index}", show_copy_button = True, placeholder = "Negative Prompt" , elem_classes=["sts_multiinput", "prompt"], elem_id=f"le_inpt_{self.filterkey}_neg")

                            with gr.Row():    
                                self.skipNegative = gr.Checkbox(label = f"Skip Negative {self.index}",tooltip = "Do not use Negative Prompt?", value = False,elem_id=f"le_sendneg_{self.filterkey}")

                            with gr.Row():
                                self.insertpoint = gr.Text(show_label= True, label=f"Insert To {self.index}",tooltip = "Replace this string in main prompt with Live Edits positive prompt",show_copy_button=True, value = "",elem_id=f"le_insert_{self.filterkey}")
                                self.section = gr.Text(show_label= True, label=f"Sections {self.index}", placeholder = "0,1,2 empty = all",max_lines = 1,tooltip = "Pick which Section (seperated by {prompt}) to apply to the prompt)",elem_id=f"le_sect_{self.filterkey}")

                        #Call function to refresh UI when Style selection has been changed by user.
                        self.dropdown.input(fn=self.UpdateLiveEdit,inputs = [self.dropdown], outputs = [self.positive , self.negative,liveEdit_rename_field])


                        def applywrap(liveEdit_rename,liveEdit_Pos, liveEdit_Neg):
                            if liveEdit_rename != "None" and liveEdit_rename != "":
                                ui_prompt_styles.save_style(liveEdit_rename,liveEdit_Pos, liveEdit_Neg)
                                return gr.Row.update(visible=False), gr.Dropdown.update(value = liveEdit_rename)
                            else: 
                                return gr.Row.update(visible=False), gr.Dropdown.update(value = "None")
                            
                        def sendToPrompt(stylePromptValue,styleNegValue,ist21, skipneg, comment):
         
                            if getattr(shared.opts, f"{extn_id}_sending","Disable") == "Disable Live Edit":
                                return gr.Checkbox.update(value=False)
                            elif getattr(shared.opts, f"{extn_id}_sending","Disable") == "Clear Live Edit" :
                                return gr.Dropdown.update(value="None"), gr.Textbox.update(value=None), gr.Textbox.update(value=None),gr.Textbox.update(value=None), gr.Row.update(visible=False)
                          

                        def showRename():
                                return gr.Row.update(visible=True)
                        def hideRename():
                                return gr.Row.update(visible=False)
                        def clear():
                            return gr.Dropdown.update(value="None"), gr.Textbox.update(value=None), gr.Textbox.update(value=None),gr.Textbox.update(value=None), gr.Row.update(visible=False)



                        apply.click(applywrap, inputs = [liveEdit_rename_field,self.positive,  self.negative], outputs = [row, self.dropdown])
                        apply2.click(applywrap, inputs = [liveEdit_rename_field,self.positive,  self.negative], outputs = [row, self.dropdown])
                        
                        #Create Dummy Statse that get send to javascript to determine is_img2img state, these could be moved elsewhere prevent duplication
                        ist21 = gr.Checkbox(value = is_img2img, visible = False)
                        comment = gr.Checkbox(value = getattr(shared.opts, f'{extn_id}_remove_comments_sending',False) is True and getattr(shared.opts, f'enable_prompt_comments',False) is True, visible = False  )
                     
                        #Register inputs and outputs depending on settings,(To Do: Figure out a ways to do this without UI reload)
                        if getattr(shared.opts, f"{extn_id}_sending","Disable") == "Disable Live Edit":
                            send.click(sendToPrompt, inputs = [self.positive,self.negative,ist21, self.skipNegative,comment], outputs = [self.enable],_js = 'sendToPrompt')
    
                        elif getattr(shared.opts, f"{extn_id}_sending","Disable") == "Clear Live Edit":
                            send.click(sendToPrompt, _js = 'sendToPrompt',inputs = [self.positive,self.negative,ist21, self.skipNegative,comment], outputs = [self.dropdown,self.positive, self.negative,liveEdit_rename_field,row])
                        else:
                            send.click(sendToPrompt, _js = 'sendToPrompt', inputs = [self.positive,self.negative,ist21, self.skipNegative,comment], outputs = [])

                        rename.click(showRename, inputs = [], outputs = [row])
                        renameHide.click(hideRename, inputs = [], outputs = [row])
                        clear_btn.click(clear, inputs = [], outputs = [self.dropdown,self.positive, self.negative,liveEdit_rename_field,row])
                        