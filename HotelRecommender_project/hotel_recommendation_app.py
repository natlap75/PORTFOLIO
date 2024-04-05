# pip3 install kivy
# pip3 install scikit-learn
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
import pandas as pd
from sklearn.neighbors import NearestNeighbors


# loading the aggregated hotel data from the CSV file
file_path = 'hotel_aggregates.csv'

class HotelRecommenderApp(App):
    """
    This class represents the main application using Kivy framework.
    It builds the user interface and handles the interaction.
    """
    def build(self):
        """
        Builds the main layout of the application including selection options for country, tag, and amenities.
        Returns the root widget of the application.
        """
        layout = BoxLayout(orientation='vertical')
        
        # dropdown for selecting a country
        self.country_spinner = Spinner(
            text='Choose Country',
            values=('Netherlands', 'United Kingdom', 'France', 'Spain', 'Italy', 'Austria')
        )

        # dropdown for selecting a tag
        self.tag_spinner = Spinner(
            text='Choose one Tag',
            values=('leisure trip','submitted from a mobile device',
                    'couple','stayed 1 night','stayed 2 nights',
                    'solo traveler','stayed 3 nights','business trip','group',
                    'family with young children','stayed 4 nights','double room')
        )

        # layout for amenities checkboxes
        self.amenities_layout = GridLayout(cols=6)
        self.amenities_checkboxes = {}
        amenities = ['spa', 'parking', 'wifi', 'balcony', 'pool', 'breakfast', 'view', 'location', 'service', 'clean', 'comfort', 'kitchen', 'friendly staff', 'air condition', 'pets']
        for amenity in amenities:
            cb = CheckBox()
            self.amenities_checkboxes[amenity] = cb
            self.amenities_layout.add_widget(Label(text=amenity))
            self.amenities_layout.add_widget(cb)

        # Adding widgets to the main layout    
        layout.add_widget(self.country_spinner)
        layout.add_widget(self.tag_spinner)
        layout.add_widget(Label(text='Choose up to three amenities'))
        layout.add_widget(self.amenities_layout)

        # Button to trigger hotel recommendations
        recommend_button = Button(text='Recommend hotels')
        recommend_button.bind(on_press=self.on_recommend_hotels_pressed)
        layout.add_widget(recommend_button)

        # Label to display the recommended hotels
        self.results_label = Label()
        layout.add_widget(self.results_label)
        return layout

    def on_recommend_hotels_pressed(self, instance):
        """
        Handles the event when the 'Recommend hotels' button is pressed.
        Fetches the user's selections, generates hotel recommendations, and updates the UI accordingly.
        
        Parameters:
            instance: The instance of the button that was pressed.
        """
        # Load the latest hotel data
        hotel_aggregates = pd.read_csv(file_path)
        selected_country = self.country_spinner.text
        selected_tag = self.tag_spinner.text 
        selected_amenities = [amenity for amenity, cb in self.amenities_checkboxes.items() if cb.active]
        
        # Limit the selection to up to three amenities
        if len(selected_amenities) > 3:
            self.results_label.text = "Please select up to three amenities."
            return
        
        # Fetch recommended hotels based on selected criteria
        recommended_hotels_info = self.recommend_hotels(selected_country, selected_tag, selected_amenities, hotel_aggregates, 5)
        # Display the recommendations
        results_text = '\n'.join([f'{hotel.Hotel_Name} : {hotel.Average_Score}' for index, hotel in recommended_hotels_info.iterrows()])
        self.results_label.text = "Recommended hotels:\n" + results_text

    def recommend_hotels(self, country, selected_tag, selected_amenities, hotel_aggregates, n_neighbors=5):
        """
        Recommends hotels based on the selected country, tag, and amenities using the NearestNeighbors algorithm.
        
        Parameters:
            country (str): The selected country.
            selected_tag (str): The selected tag.
            selected_amenities (list): List of selected amenities.
            hotel_aggregates (DataFrame): The DataFrame containing hotel data.
            n_neighbors (int): The number of hotel recommendations to generate.
            
        Returns:
            DataFrame: A DataFrame containing recommended hotels sorted by average score.
        """
        # Filter hotels by selected country
        country_hotels = hotel_aggregates[hotel_aggregates['Country'] == country]
        # Prepare the feature vector for the selected amenities and tag
        features_data = country_hotels.drop(columns=['Hotel_Name', 'Country', 'Average_Score'])
        ideal_features_vector = self.get_feature_vector(selected_tag, selected_amenities, features_data.columns.tolist())
        # Initialize and fit NearestNeighbors
        knn = NearestNeighbors(n_neighbors=n_neighbors, metric='cosine')
        # model training
        knn.fit(features_data.values)
    
        # Find nearest hotels based on the ideal feature vector
        distances, indices = knn.kneighbors([ideal_features_vector])
    
        # Retrieve recommended hotels and sort by average score
        recommended_indices = indices.flatten()
        recommended_hotels = country_hotels.iloc[recommended_indices][['Hotel_Name', 'Average_Score']]
    
        # Sort by GPA
        return recommended_hotels.sort_values(by='Average_Score', ascending=False)


    def get_feature_vector(self, selected_tag, selected_amenities, all_features):
        """
        Constructs a feature vector for the selected tag and amenities.
        
        Parameters:
            tags_to_use (str): The selected tag.
            amenities (list): List of selected amenities.
            all_features (list): List of all possible features (amenities and tags).
            
        Returns:
            list: A feature vector representing the selected tag and amenities.
        """
        # Initialize a feature vector with zeros
        feature_vector = [0] * len(all_features)

        # Set features to 1 for selected tag
        if selected_tag in all_features:
            index = all_features.index(selected_tag)
            feature_vector[index] = 1

        # Set features to 1-3 for selected amenities
        for amenity in selected_amenities:
            if amenity in all_features:
                index = all_features.index(amenity)
                feature_vector[index] = 3
  
        return feature_vector

if __name__ == '__main__':
    HotelRecommenderApp().run()
