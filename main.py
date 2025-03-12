import sys
import requests
from PyQt5.QtWidgets import (QApplication,QWidget,QLineEdit,QLabel,
                             QPushButton,QComboBox,QTextBrowser,QListWidget
                             ,QVBoxLayout,QFormLayout,QHBoxLayout,QCompleter)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
import inflect
import nltk
from nltk.corpus import wordnet
from textblob import TextBlob

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class Recipe_Finder(QWidget):
    def __init__(self):
        super().__init__()

        self.ingredients_label=QLabel("Ingredients(comma-separated)",self)
        self.ingredients_input=QLineEdit(self)
        self.dietary_restriction_label=QLabel("Dietary Restriction",self)
        self.dietary_restriction_input=QComboBox(self)
        self.cooking_time_label=QLabel("Max Cooking Time(mins)",self)
        self.cooking_time_input=QComboBox(self)
        self.recipe_amount_label=QLabel("Amount of Recipes")
        self.recipe_amount_input=QComboBox(self)
        self.search_recipes_button=QPushButton("Search Recipes",self)
        self.recipe_list=QListWidget(self)
        self.recipe_details=QTextBrowser(self)
        self.recipe_image_label=QLabel(self)

        self.iniUI()

    def iniUI(self):

        self.setWindowTitle("Recipe Finder")

        hBox=QHBoxLayout()
        vbox=QVBoxLayout()
        fBox=QFormLayout()
        
        fBox.addRow(self.ingredients_label,self.ingredients_input)
        fBox.addRow(self.dietary_restriction_label,self.dietary_restriction_input)
        fBox.addRow(self.cooking_time_label,self.cooking_time_input)
        fBox.addRow(self.recipe_amount_label,self.recipe_amount_input)

        vbox.addLayout(fBox)

        vbox.addWidget(self.search_recipes_button)

        hBox.addWidget(self.recipe_list,2)
        hBox.addWidget(self.recipe_details,3)
        hBox.addWidget(self.recipe_image_label,2)

        vbox.addLayout(hBox)

        self.setLayout(vbox)

        diets=["None","Gluten Free","Vegetarian","Lacto-Vegetarian","Vegan",
               "Whole30","Low FODMAP","Primal","Paleo","Ketogenic","Ovo-Vegetarian",
               "Pescetarian"]
        self.dietary_restriction_input.addItems(diets)
        self.dietary_restriction_input.setEditable(True)
        completer=QCompleter(diets)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.dietary_restriction_input.setCompleter(completer)

        times=["15","20","30","45","50","60","75","80","90","100",
               "110","120","130","140","150","160"]
        self.cooking_time_input.addItems(times)
        self.cooking_time_input.setEditable(True)
        completer=QCompleter(times)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.cooking_time_input.setCompleter(completer)

        amount=["5","10","15","20","25","30","35","45"]
        self.recipe_amount_input.addItems(amount)
        self.recipe_amount_input.setEditable(True)
        completer=QCompleter(amount)
        completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.recipe_amount_input.setCompleter(completer)

        self.recipe_image_label.setFixedSize(312,231)
        self.recipe_image_label.setAlignment(Qt.AlignCenter)
        self.recipe_image_label.setStyleSheet("border: 1px solid #4CAF50;")
        self.recipe_image_label.setText("No Image")

        self.ingredients_input.setObjectName("ingredients_input")
        self.dietary_restriction_input.setObjectName("dietary_restriction_input")
        self.cooking_time_input.setObjectName("cooking_time_input")
        self.recipe_amount_input.setObjectName("recipe_amount_input")
        self.search_recipes_button.setObjectName("search_recipes_button")
        self.recipe_list.setObjectName("recipe_list")
        self.recipe_details.setObjectName("recipe_details")
        self.ingredients_label.setObjectName("ingredients_label")
        self.dietary_restriction_label.setObjectName("dietary_restriction_label")
        self.cooking_time_label.setObjectName("cooking_time_label")
        self.recipe_amount_label.setObjectName("recipe_amount_label")

        self.setStyleSheet("""
            #ingredients_input {
                padding: 5px;
                font-size: 14px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
            }

            #ingredients_label {
                font-weight: bold;
                color: #333;
            }

            #dietary_restriction_input {
                padding: 5px;
                font-size: 14px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
            }

            #dietary_restriction_input QAbstractItemView {
                background-color: white;
                color: #333;
                selection-background-color: #4CAF50;
                border: 1px solid #4CAF50;
            }

            #cooking_time_input {
                padding: 5px;
                font-size: 14px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
            }

            #cooking_time_input QAbstractItemView {
                background-color: white;
                color: #333;
                selection-background-color: #4CAF50;
                border: 1px solid #4CAF50;
            }
            
            #recipe_amount_input {
                padding: 5px;
                font-size: 14px;
                border: 1px solid #4CAF50;
                border-radius: 5px;
            }

            #recipe_amount_input QAbstractItemView {
                background-color: white;
                color: #333;
                selection-background-color: #4CAF50;
                border: 1px solid #4CAF50;
            }

            #search_recipes_button {
                background-color: #4CAF50;
                color: white;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
                border: none;
            }

            #search_recipes_button:hover {
                background-color: #45a049;
            }

            #recipe_list {
                border: 1px solid #4CAF50;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px;
                margin: 0;
            }

            #recipe_details {
                border: 1px solid #4CAF50;
                border-radius: 5px;
                font-size: 14px;
                padding: 5px;
                margin: 0;
            }

            #recipe_list QScrollBar {
                border: none;
                background: none;
            }

            #recipe_details QScrollBar {
                border: none;
                background: none;
            }

            #ingredients_label, #dietary_restriction_label, #cooking_time_label, #recipe_amount_label {
                font-weight: bold;
                color: #333;
            }
                           
            QLabel{
                font-size:17px;               
            }
        """)

        self.search_recipes_button.clicked.connect(self.get_recipes)

    def keyPressEvent(self,event):

        if event.key()==16777220:
            self.get_recipes()

    def get_recipes(self):
        
        if self.ingredients_input.text()=="":
            self.display_error("No Recipes Have Found!")
        else:

            self.recipe_details.setText("")
            ingredients = self.ingredients_input.text().split(",")
            self.ingredients = [ingredient.strip() for ingredient in ingredients]
            self.ingredient =self.check_ingredients_typo(self.ingredients)
            ingredients_str = ",".join(self.ingredients)            

            diet=self.dietary_restriction_input.currentText()

            max_time=self.cooking_time_input.currentText()
            max_time=int(max_time)
            amount=self.recipe_amount_input.currentText()
            amount=int(amount)

            api_key="d89affa143a24e7c97171fbdba579a7c"
            url="https://api.spoonacular.com/recipes/complexSearch"

            params={

                "apiKey":api_key,
                "diet":diet,
                "includeIngredients":ingredients_str,
                "maxReadyTime":max_time,
                "addRecipeInformation":True,
                "addRecipeInstructions":True,
                "number":amount,
                "fillIngredients":True

            }

            try:

                response=requests.get(url,params=params)
                response.raise_for_status()
                data=response.json()

                if response.status_code==200:
                    self.display_recipes(data)

                else:
                    self.display_error("Error:\nAPI response was not successful")

            except requests.exceptions.HTTPError as http_error:

                match response.status_code:

                    case 400:
                        self.display_error("Bad request:\nPlease check your input")
                    case 401:
                        self.display_error("Unauthorized:\nInvalid API key")
                    case 403:
                        self.display_error("Forbidden:\nAccess is denied")
                    case 404:
                        self.display_error("Not found:\nRecipe not found")
                    case 500:
                        self.display_error("Internal Server Error:\nPlease try again later")
                    case 502:
                        self.display_error("Bad Gateway:\nInvalid response from the server")
                    case 503:
                        self.display_error("Service Unavailable:\nServer is down")
                    case 504:
                        self.display_error("Gateway Timeout:\nNo response from the server")
                    case _:
                        self.display_error(f"HTTP error occurred:\n{http_error}")

            except requests.exceptions.ConnectionError:
                self.display_error("Connection Error:\nPlease check your internet connection")
            except requests.exceptions.Timeout:
                self.display_error("Timeout Error:\nThe request timed out")
            except requests.exceptions.TooManyRedirects:
                self.display_error("Too many Redirects:\nCheck the URL")
            except requests.exceptions.RequestException as req_error:
                self.display_error(f"Request Error:\n{req_error}")

    def display_error(self,msg):

        error_label=self.recipe_details
        error_label.setText("")
        self.recipe_list.clear()
        self.recipe_image_label.clear()
        self.recipe_image_label.setText("No Image")
        error_label.setText(msg)

    def display_recipes(self,data):
        
        self.recipe_image_label.clear()
        self.recipe_details.clear()
        self.recipe_list.clear()
        recipes=data["results"]
        
        if not recipes:
            self.display_error("No Recipes Have Found!")
            return
        
        for recipe in recipes:

            recipe_name=recipe.get("title")
            recipe_image=recipe.get("image")
            recipe_instructions = recipe.get("analyzedInstructions", [])
            recipe_summary=recipe["summary"] if "summary" in recipe else "No summary available"
            recipe_ingredients=recipe.get("extendedIngredients",[])
            recipe_time=recipe.get("readyInMinutes")
            diet=data.get('results', [{}])[0].get('diets', [])

            self.recipe_list.addItem(recipe_name)

            item = self.recipe_list.item(self.recipe_list.count() - 1)
            item.setData(
                Qt.UserRole,
                {
                    "title": recipe_name,
                    "image": recipe_image,
                    "instructions": recipe_instructions,
                    "summary": recipe_summary,
                    "ingredients":recipe_ingredients,
                    "ready_time":recipe_time,
                    "diet":diet
                },
            )

        self.recipe_list.itemClicked.connect(self.on_recipe_selected)

    def on_recipe_selected(self):

        selected_item = self.recipe_list.currentItem()
        if selected_item is None:
            return

        recipe_data = selected_item.data(Qt.UserRole)
        recipe_title = recipe_data["title"]
        recipe_image_url = recipe_data["image"]
        recipe_instructions = recipe_data["instructions"]
        recipe_summary = recipe_data["summary"]
        recipe_ingredients=recipe_data["ingredients"]
        recipe_time=recipe_data["ready_time"]
        recipe_diet=recipe_data["diet"]

        details_html = f"<h2>{recipe_title}</h2><h4>Ready Time:{recipe_time} Minutes</h4><p>{recipe_summary}</p>"

        if not self.dietary_restriction_input.currentText()=="None":
            diet_html="<h3>Dietary Information:</h3><ul>"
            for diet in recipe_diet:
                diet_html+=f"<li>{diet.capitalize()}</li>"
            diet_html+="</ul>" if recipe_diet else "<p>No dietary information available</p></ul>"
            details_html+=diet_html
        else:
            pass
        
        details_html+=self.get_missing_ingredients_html(recipe_ingredients)

        ingredients_html="<h3>Ingredients:</h3><ul style='list-style-position: inside; padding-left: 0;'>"
        
        for ingredient in recipe_ingredients:
            name=ingredient.get("name")
            amount=ingredient.get("amount")
            unit=ingredient.get("unit")
            ingredients_html +=f"<li>{amount} {unit} of {name}</li>"
        ingredients_html+="</ul>"
        
        details_html+=ingredients_html

        instructions_html = "<h3>Instructions:</h3>"

        if recipe_instructions:

            for i, instruction in enumerate(recipe_instructions[0]["steps"], 1):
                instructions_html += f"<p><b>Step {i}:</b> {instruction['step']}</p>"
        else:
            instructions_html += "<p>No instructions available</p>"

        details_html += instructions_html

        self.recipe_details.setHtml(details_html)

        if recipe_image_url:

            image_data = requests.get(recipe_image_url).content
            pixmap = QPixmap()
            pixmap.loadFromData(image_data)
            scaled_pixmap = pixmap.scaled(
                self.recipe_image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.recipe_image_label.setPixmap(scaled_pixmap)
        else:
            self.recipe_image_label.setText("No Image")

    def get_missing_ingredients_html(self, recipe_ingredients):
        
        missing_ingredients_html = "<h3>Missing Ingredients:</h3><ul style='list-style-position: inside; padding-left: 0;'>"

        for ingredient in recipe_ingredients:
            name = ingredient["name"]

            # Check for matches using synonyms and plurals
            if not self.is_missing_ingredient_matched(name):
                missing_ingredients_html += f"<li>{name}</li>"
            else:
                continue

        missing_ingredients_html += "</ul>"

        return missing_ingredients_html

    def is_missing_ingredient_matched(self, ingredient_name):
    
        p = inflect.engine()

        # Correct typos in user ingredients
        corrected_user_ingredients = [
            self.correct_typo(ingredient) for ingredient in self.ingredients
        ]

        # Convert corrected ingredients and recipe ingredient to singular form
        user_ingredients_singular = [
            p.singular_noun(ingredient) or ingredient for ingredient in corrected_user_ingredients
        ]
        ingredient_singular = p.singular_noun(ingredient_name) or ingredient_name

        # Check for direct match
        if ingredient_singular in user_ingredients_singular:
            return True

        # Check synonyms
        for user_ingredient in user_ingredients_singular:
            user_synonyms = set(
                lemma.name()
                for syn in wordnet.synsets(user_ingredient)
                for lemma in syn.lemmas()
            )
            if ingredient_singular in user_synonyms:
                return True

        return False

    def correct_ingredients(self, ingredients):
        return [self.correct_typo(ingredient) for ingredient in ingredients]

    @staticmethod
    
    def correct_typo(word):
        return str(TextBlob(word).correct())
            
if __name__=="__main__":
    app=QApplication(sys.argv)
    window=Recipe_Finder()
    window.show()
    sys.exit(app.exec_())