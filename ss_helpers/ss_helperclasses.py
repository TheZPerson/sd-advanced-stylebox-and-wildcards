import re
from modules.shared import prompt_styles

re_prompt = re.compile(r",? *\{(?:prompt|section)\} *,? *", re.I)
re_section = re.compile(r",? *\{section\} *,? *", re.I)
class ST_arguments():
            """Helpter classes to organize the arguments"""

            #Here is number on MAXIMUN amount of each element and how many arguments they have. Some stuff is left over from my personal branch.
            total_characters = 0
            character_arguments = 0

            total_wildcards = 6
            wildcard_aruments = 4

            total_live_Edits = 4
            live_edit_arguments = 7

            #Number on base arguments
            n_base_args = 3

            n_extracols = 0

            n_wc = wildcard_aruments*total_wildcards
            n_charas = character_arguments*total_characters
            n_les = live_edit_arguments * total_live_Edits

            total_arguments = n_wc + n_charas + n_les + n_base_args + n_extracols

            class LiveEditInfo():
             
                 def __init__(self,inputs):
                      self.enable = inputs[0]
                      # 1 not used
                      self.positive= inputs[2]
                      self.negative= inputs[3]
                      self.skipNegative = inputs[4]

                      self.insertpoint= inputs[5]
                      self.section= re.split(",", inputs[6]) if len(inputs[6]) > 0 else []

            def __init__(self,inputs):

                inum = 0
                basicArguments = inputs[0:ST_arguments.n_base_args]
                self.ss_enable = basicArguments[0]
             
                self.liveEdit_enable = basicArguments[1]
                self.wildcards_enable = basicArguments[2]

                #helper integer to help iterate arguments
                inum = ST_arguments.n_base_args

                #increment the iterator by amount of processed arguments to move on to next arguments.               
                inum += ST_arguments.n_extracols

                wildcards_temp = inputs [inum:inum+ST_arguments.n_wc]
                inum += ST_arguments.n_wc

                wildcards_vals =  wildcards_temp[::ST_arguments.wildcard_aruments]
                wildcards_inserts =  wildcards_temp[1::ST_arguments.wildcard_aruments]
                wildcards_sections =  wildcards_temp[2::ST_arguments.wildcard_aruments]
                wildcards_skipnegs=  wildcards_temp[3::ST_arguments.wildcard_aruments]

                self.wildcards = []

                for i in range(len(wildcards_vals)):
                    self.wildcards.append([wildcards_vals[i],
                                           wildcards_inserts[i],re.split(",", wildcards_sections[i]) if len(wildcards_sections[i]) > 0 else [],
                                           wildcards_skipnegs
                                           ])



                inum +=ST_arguments.n_charas

                def sliceChara(index, inputList, arg_n):
                    return inputList[arg_n*index:arg_n*index+arg_n]

                liveEdits_temp = inputs [inum:]
       
                self.liveEdits = []


                self.liveEdits.append(ST_arguments.LiveEditInfo(sliceChara(0,liveEdits_temp, ST_arguments.live_edit_arguments)))               
                self.liveEdits.append(ST_arguments.LiveEditInfo(sliceChara(1,liveEdits_temp, ST_arguments.live_edit_arguments)))
                self.liveEdits.append(ST_arguments.LiveEditInfo(sliceChara(2,liveEdits_temp, ST_arguments.live_edit_arguments)))
                self.liveEdits.append(ST_arguments.LiveEditInfo(sliceChara(3,liveEdits_temp, ST_arguments.live_edit_arguments)))

class Split_prompt():
    """Helper class that splits text in Sections"""
    def __init__(self, inputStyle = None, inputString = "", negative = "" ):

        self.style = inputStyle
        if inputStyle != None and inputStyle != "None":
            self.prompt,self.neg =self.splitStyle(inputStyle)
        else:
            self.prompt = re_prompt.split(inputString)

            self.neg = negative


    def splitStyle(self,style):
        """Gets style with given name and splits it to Sections"""
        if style == None or not style in  prompt_styles.styles:
            return [],""

        text = prompt_styles.styles[style].prompt
        negative = prompt_styles.styles[style].negative_prompt
        parts = re_prompt.split(text)
        return parts, negative

    def getMerged(self):
        """Return all section merged in single string"""
        return ",".join(self.prompt)

    def getPromptAfter1st(self):
        """Return all section exept 0 as single string"""
        if len(self.prompt) == 1:
            return self.prompt[0]
        elif len(self.prompt) == 0:
            return ""

        tmp = list(self.prompt)
        tmp.pop(0)

        return ",".join(tmp)


    def getSegments(self,sections):
        """Return all given sections as single string"""
        if len(sections) == 0 or sections[0] =="":
            return self.getMerged()

        tmp = []
        for index in sections:
            if int(index) < len(self.prompt) and int(index)>=0:
                tmp.append(self.prompt[int(index)])

        return ",".join(tmp)

    def getSegment(self, segment):
        """Return all given sections as single string"""
        if segment == -1:
            return ",".join(self.prompt)
            
        if len(self.prompt)-1 > segment:
            return self.prompt[segment]
        else:
            #print(f"Segment {segment} is out of bounds for input string")
            return ""
