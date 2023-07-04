from mtranslate import translate

class MarketplaceTranslator():

    def __init__(self):
        pass

    def translate_to_japanese(self, text: str) -> None:
        """
        Converts the provided text to japanese keeping the comma's from the original english.

        Args:
            text: str: The input string message to be converted to Japanese.
        """
        modified_text = text.replace(",", "|")
        japanese_result = translate(modified_text, 'ja', 'en')
        modified_japanese_result = japanese_result.replace("|", ",")
        print("{}\n".format(modified_japanese_result))

    def translate_to_german(self, text: str) -> None:
        german_translator = translate(text, 'de', 'en')
        print("{}\n".format(german_translator))

    def translate_to_french(self, text: str) -> None:
        french_translator = translate(text, 'fr', 'en')
        print("{}\n".format(french_translator))

    def translate_to_portuguese(self, text: str) -> None:
        portuguese_translator = translate(text, 'pt', 'en')
        print("{}\n".format(portuguese_translator))

    def translate_to_spanish(self, text: str) -> None:
        spanish_translator = translate(text, 'es', 'en')
        print("{}\n".format(spanish_translator))


if __name__ == "__main__":

    marketplace_translator = MarketplaceTranslator()

    product_title = "Purgatory. - Nautical Telescope"

    product_features = "\n1: {}\n2: {}\n3: {}\n4: {}\n5: {}\n".format(
        "Animated.",
        "Scripted to zoom in and out.",
        "Multiple textures.",
        "Materials Enabled.",
        "")

    product_description = """- Materials Enabled. 
- Includes 4 Textures with Hud. 
- Scripted Zoom (Hold Left click and press Page up or down)
- Non-Rigged Mesh.
- Bento Animations.

If you like this product please let me know by leaving a review.  

If you have any issues please feel free to leave me a note-card. ♥ """

    product_keywords = "Purgatory,Nautical,Telescope,Spy,Glass,Animated,Scripted,Mesh,HD,Non-Rigged,Scope,Leather,Materials,Enabled,Bento,Zoom,Zooming,Telescoping,Telescopic"


    # remove any duplicate keywords.
    cleaned_keywords = []
    keywords = product_keywords.split(",")
    for word in keywords:
        if word not in cleaned_keywords:
            cleaned_keywords.append(word)
    cleaned_product_keywords = ",".join(cleaned_keywords)

    keyword_count = len(cleaned_product_keywords)
    keyword_char_count = sum(len(word) for word in cleaned_product_keywords)

    if keyword_char_count >= 200:
        print("WARNING: The Keywords string is at or exceeds the 200 character limit.: keyword count:{} char count:{}".format(keyword_count, keyword_char_count))

    print("------------------------------------:Japanese Translation:------------------------------------")
    print("Product Title:")
    marketplace_translator.translate_to_japanese(product_title)
    print("Product Features:")
    marketplace_translator.translate_to_japanese(product_features)
    print("Product Description:")
    marketplace_translator.translate_to_japanese(product_description)
    print("Product Keywords:")
    marketplace_translator.translate_to_japanese(cleaned_product_keywords)

    print("------------------------------------:German Translation:------------------------------------")
    print("Product Title:")
    marketplace_translator.translate_to_german(product_title)
    print("Product Features:")
    marketplace_translator.translate_to_german(product_features)
    print("Product Description:")
    marketplace_translator.translate_to_german(product_description)
    print("Product Keywords:")
    marketplace_translator.translate_to_german(cleaned_product_keywords)

    print("------------------------------------:French Translation:------------------------------------")
    print("Product Title:")
    marketplace_translator.translate_to_french(product_title)
    print("Product Features:")
    marketplace_translator.translate_to_french(product_features)
    print("Product Description:")
    marketplace_translator.translate_to_french(product_description)
    print("Product Keywords:")
    marketplace_translator.translate_to_french(cleaned_product_keywords)

    print("------------------------------------:Portuguese Translation:------------------------------------")
    print("Product Title:")
    marketplace_translator.translate_to_portuguese(product_title)
    print("Product Features:")
    marketplace_translator.translate_to_portuguese(product_features)
    print("Product Description:")
    marketplace_translator.translate_to_portuguese(product_description)
    print("Product Keywords:")
    marketplace_translator.translate_to_portuguese(cleaned_product_keywords)

    print("------------------------------------:Spanish Translation:------------------------------------")
    print("Product Title:")
    marketplace_translator.translate_to_spanish(product_title)
    print("Product Features:")
    marketplace_translator.translate_to_spanish(product_features)
    print("Product Description:")
    marketplace_translator.translate_to_spanish(product_description)
    print("Product Keywords:")
    marketplace_translator.translate_to_spanish(cleaned_product_keywords)
