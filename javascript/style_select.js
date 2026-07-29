function sendToPrompt(positive, negative, is_img2img, sendNegative, handleComment) {

    var positiveField = null;
    var negativeField = null;
    switch (is_img2img) {
        case false:
            positiveField = gradioApp().getElementById("txt2img_prompt").querySelector("textarea");
            negativeField = gradioApp().getElementById("txt2img_neg_prompt").querySelector("textarea");
            break;
        case true:
            positiveField = gradioApp().getElementById("img2img_prompt").querySelector("textarea");
            negativeField = gradioApp().getElementById("img2img_neg_prompt").querySelector("textarea");
            break;
    }

    positive = positive.replace(/,? *\{(?:prompt|section)\} *,?/, "")

    if (handleComment == true) {
        positive = positive.replace(/[^\S\n]*(\/\/|#).*/g, "")
        positive = positive.replace(/\/\*.*?\*\//s, "")


        negative = negative.replace(/[^\S\n]*(\/\/|#).*/g, "")
        negative = negative.replace(/\/\*.*?\*\//s, "")
    }


    positiveField.value = positiveField.value + (positiveField.value.length > 0 && positive.length ? "\n" : "") + positive;
    if (sendNegative == false) {
        negativeField.value = negativeField.value + (negativeField.value.length > 0 && negative.length ? "\n" : "") + negative;
    }
   

    return ['****','',false,false,false];
}