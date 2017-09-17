![](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/000/535/238/datas/gallery.jpg)

# ToroGo

Let Data Science decide the perfect neighborhood for you in Toronto

https://devpost.com/software/torogo

![](https://challengepost-s3-challengepost.netdna-ssl.com/photos/production/software_photos/000/535/574/datas/gallery.jpg)

## Inspiration

We travelled all the way from India and while booking our AirBnb we were overwhelmed with the options available to us. Although, websites like tripadvisor help with reviews of an area, it is often not enough. Toronto welcomes over 40 million visitors annually, and is the leading tourism destination in Canada. So we decided to use the power of data science to help travellers like us solve where to stay.
 
## What it does

### Find a Place

In our discussions we came up with three important things that users look at while deciding where to live in a new city:
- Price
- Safety 
- Reviews

The app requests the user to enter his priority for the above mentioned features and suggests the top 5 suggested places that would suit the user based on data analysis. 

### Currency Converter

Along with that we provide the user easy access to check the live currency exchange rates using **XE.com** powerful api instantly from the app. It supports searching from 100s of currencies and can instantly give the live exchange rate.

## How we built it

We used open datasets available from the Canadian Open Dataset website and Airbnb to build an aggregate score of around 130 sub-areas of Toronto City. We chose three parameters, 
- **Locality Ratings** based on Sentiment Analysis of Reviews
- **Safety Ratings** based on Crime Data such as Assaults
- **Priceyness Ratings** based on the cost of listings of Airbnbs in a Neighborhood.

The data analysis can be viewed in our [iPython Notebooks](https://github.com/rhnvrm/htn/tree/master/dataset)

[![Imgur](https://i.imgur.com/gzjo6f2.png)](https://github.com/rhnvrm/htn/tree/master/dataset)

After this, we wrote an algorithm based on Euclidean Distance between these ratings and the user's preferences to suggest the most suitable locations for the user. 

The currency converter is powered by **XE.com**'s API and we were able to make an intuitive UX for searching through the currencies.


## Challenges we ran into

- Data was easy to find but aggregation was tough to do based on the neighborhood level.
- Getting the heatmap to work based on neighborhood on Android
- We tried to integrate the Microsoft Azure Chatbot API but were unable to integrate it with the app.

## Accomplishments that we're proud of

- A full ranking of the neighborhoods based on reviews, safety and priceyness of Toronto
- A fully functional App and API.
- Firebase Authentication

