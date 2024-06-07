from translate import Translator
def translate_urdu_to_english(text):
    # Split the input text into smaller segments (e.g., 500 characters each)
    segment_length = 500
    segments = [text[i:i+segment_length] for i in range(0, len(text), segment_length)]
    
    translated_segments = []

    for segment in segments:
        translator = Translator(from_lang="ur", to_lang="en")
        translation = translator.translate(segment)
        translated_segments.append(translation)

    # Join the translated segments to form the complete translated text
    translated_text = ' '.join(translated_segments)

    return translated_text

text='''پاکستان کی تاریخ

پاکستان کی تاریخ ایک دلچسپ اور غنی روایت سے بھرپور ہے۔ یہاں تک کہ اس کی تشکیل سال 1947 میں برطانوی راج سے آزادی کے بعد ہوئی تھی۔ پاکستان ایک اہم جنوب ایشیائی ملک ہے جس کی تشکیل کی زمینوں پر ایک نئی اور آزاد مملکت کی بنیاد رکھی گئی۔

پاکستان کی تشکیل کا عصر قدیم تاریخ سے لے کر آج کے دور تک جاتا ہے۔ یہاں تک کہ مغربی اور شرقی تاریخ، دھرم اور ثقافت کا مختلف مظاہر کو ایک مل کر پیش کرتی ہے۔

پاکستان کی تاریخ کا اہم حصہ قدیم زمین پر مشہور موہنجو داڑو کرنے والی موہنجو داڑو سبقت ہے، جو 2500 قبل مسیح کی تاریخ کے قریب بنی تھی۔ اس دوران، موہنجو داڑو ایک ترقی یافتہ اور تنصیب کار تنصیب کار تھیں، جو کرنسی اور اشیائے لوازم کی تجارت کرتے تھے۔

پاکستان کی تاریخ کا دوسرا اہم مرحلہ اسلامی حکومت کی تشکیل کا ہے، جو اسلامی تاریخ کی روشنی میں آیا۔ 711ء میں مسلم فاتح محمد بن قاسم کی طرف سے سندھ کا فتح کیا گیا، جس سے اسلام کی تشکیل کی بنیاد رکھی گئی۔

پاکستان کی تاریخ میں اندرونی اور بیرونی تبدیلیوں کے بعد، 1947 میں برطانوی راج کے خلاف آزاد ہوا اور پاکستان کا قیام ہوا۔ اس کے بعد، پاکستان نے اپنی تاریخ میں مختلف اقساط اور واقعات کو جینا اور گوارا کیا ہے۔

پاکستان کی تاریخ میں کئی معاشرتی، سیاسی، اور عسکری واقعات ہوئے ہیں جن کی بنیاد پر ملک کی فکری، سیاسی، اور معاشرتی ترقی میں تبدیلیاں آئی ہیں۔ یہ ملک ایک اہم دورانیہ میں ہے جب اس کی تاریخ میں نئی تشکیلات اور ترقی کے راستے پر کام کیا جا رہا ہے۔

پاکستان کی تاریخ نے اس ملک کی ثقافت، تاریخی وارثی، اور معاشرتی روایات کو شاندار اور رنگین بنایا ہے۔ یہ ملک اپنی تاریخ کی امتیازی گواہ ہے جو اس کی روشنی میں اپنی تاریخی میراث کو محفوظ کرتا 
'''


# print(translate_urdu_to_english(text))
# from sparknlp.pretrained import PretrainedPipeline 
# pipeline = PretrainedPipeline("translate_ur_en", lang = "xx") 
# # pipeline.annotate("Your sentence to translate!")
# from googletrans import Translator

# from translate import Translator

# # def translate_urdu_to_english(text):
# #     translator = Translator(from_lang="ur", to_lang="en")
# #     translation = translator.translate(text)
# #     translated_text = translation
# #     return translated_text

print(translate_urdu_to_english(text))
