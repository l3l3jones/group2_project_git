# Seenit!

![Welcome to Seenit!](documentation/image1.png)

Seenit! was created as the group project requirement for the Code First Girls Degree - Summer 2023 Software Stream Cohort.

## CONTENTS

* [User Experience](#user-experience)
  * [Project Goals](#project-goals)
  * [User Stories](#user-stories)

* [Design](#design)
  * [Colour Scheme](#colour-scheme)
  * [Typography](#typography)
  * [Imagery](#imagery)
  * [Wireframes](#wireframes)

* [Features](#features)
  * [Elements Fount on Each Page](#elements-found-on-each-page)
  * [Future Implementations](#future-implementations)
  * [Accessibility](#accessibility)

* [Technologies Used](#technologies-used)
  * [Languages Used](#languages-used)
  * [Frameworks Used](#frameworks-used)
  * [Libraries & Packages Used](#libraries--packages-used)
  * [Programs Used](#programs-used)
    * [Movies API](#google-books-api)
    * [Error Handling](#error-handling)
  

* [Deployment & Local Development](#deployment--local-development)
  * [Local Development](#local-development)
    * [How to Fork](#how-to-fork)
    * [How to Clone](#how-to-clone)

* [Testing](#testing)
  
* [Credits](#credits)
  * [Code Used](#code-used)
  * [Content](#content)
  * [Media](#media)
  * [Acknowledgments](#acknowledgments)

- - -

## User Experience

### Project Goals

***Brief outline here***

### User Stories

#### __Target Audience__

The target audience for Seenit! is...

#### __First Time Visitor__

As a first time user of the site I want to be able to:

* Search for movie recommendations based on genre.
* Search for movie recommendations based on decade released.
* Search for movie recommendations based on keywords.
* Search for movie recommendations that currently appear in cinemas.

#### __Returning Visitor__

As a returning user of the site I want to be able to use the app in the same way in which a first time user interacts with the app.

- - -

## Design - CAN REMOVE THIS PART IF NEEDED

### Colour Scheme

I have taken inspiration from...

### Typography

Google Fonts was used to import the chosen fonts for use in the site.

I have used [FONT NAME](https://www.link-to-google-font-if-applicable.com) for the headings on the site. I have chosen to use this font as...

I have used [FONT NAME](https://www.link-to-google-font-if-applicable.com) for the body text on the site. FONT NAME is a sans-serif font which allows it to be legible and is a great choice for accessibility.

### Imagery

As the site is for people who love to watch movies, I have kept the imagery throughout the site to the theme of movies. Please view the media section for more information on where each image was sourced.

All images of the movies have been requested through the MOVIES API.

### Wireframes - CAN REMOVE IF NOT APPROPRIATE

Wireframes were created using NAME.


#### __Home Page__

![Home Page](documentation/wireframes/home.png)

- - -

### Future Implementations

In future implementations I would like to:

* Be able to create user profiles so that data and movie recommendations can be saved.
* Add change and reset password functionality to the profile section.
* Give users the option to delete their account in the profile section.
* Be able to give showtimes and locations of cinemas for movies shoing in theatres.

### Accessibility - THIS CAN BE REMOVED IF NEEDED

The group have been mindful during coding to ensure that the website is as accessible friendly as possible. This has been have achieved by:

* Using semantic HTML.
* Using descriptive alt attributes on images on the site.
* Providing information for screen readers where there are icons used and no text.
* Ensuring that there is a sufficient colour contrast throughout the site.

### Problems encountered and changes made

The initial brief included the use of a showtimes API to be able to list the cinema listings, times and locations of where the movie is being shown. Unfortunately, after enquiries witht he ASPI provider, due to the project not being classed as 'commercial use', there was a cost invloved with maing API calls.

Due to this issue, we discussed as a group and decided to change the brief slightly. Instead of showing cinema listings...




## Technologies Used - THIS WILL NEED EDITING!!!!!!!!

### Languages Used

HTML, CSS, Javascript, Python

### Frameworks Used

[Flask](https://pypi.org/project/Flask/) - A micro framework.

[Bootstrap](https://getbootstrap.com/) - version 5.2.0 - CSS Framework.

### Libraries & Packages Used


### Programs Used - WILL REQUIRE EDITING

[Pip](https://pypi.org/project/pip/) - Tool for installing python packages.

[Jinja](https://jinja.palletsprojects.com/en/3.1.x/) - Templating engine.

[Balsamiq](https://balsamiq.com/) - Used to create wireframes.

[Git](https://git-scm.com/) - For version control.

[Github](https://github.com/) - To save and store the files for the website.

[Google Fonts](https://fonts.google.com/) - To import the fonts used on the website.

[Bootstrap Icons](https://icons.getbootstrap.com/) - Version 1.8.3 - For the iconography on the website.

[Google Chrome Dev Tools](https://developer.chrome.com/docs/devtools/) - To troubleshoot and test features, solve issues with responsiveness and styling.

### Movies API - NEEDS EDITING

I have used the Google Books API to allow users of the site to search for books.

I made use of the NAME API [documentation](https://MOVIESAPIWEBSITE.COM) to learn how to fetch data from the API. The documentation also allowed me to amend my request to only fetch the fields I plan to use on my site. This reduces the amount of data returned to me and will speed up server processing.

As I am only using the API to search for...  the requests to the API contain my API key, the search term the user has created and the fields that I would like to be returned. I have chosen to only receive the movie title, actors, genre, description and thumbnail of the movie. I have set up the API request to ask for 30 results maximum.

### Error Handling - DOES THIS NEED TO BE INCLUDED?


## Local Development / Instructions on how to run the app

### Instructions on how to run the app

Using your IDE (PyCharm) in the Python terminal, the following command is used to install...


### Local Development

#### How to Fork

To fork the repository:

1. Log in (or sign up) to Github.

2. Go to the repository for this project, [Seenit!](https://github.com/GITHUBLINK).

3. Click the Fork button in the top right corner.

#### How to Clone

To clone the repository:

1. Log in (or sign up) to GitHub.

2. Go to the repository for this project, [Seenit!](https://github.com/GITHUBLINK).

3. Click on the code button, select whether you would like to clone with HTTPS, SSH or GitHub CLI and copy the link shown.

4. Open the terminal in your code editor and change the current working directory to the location you want to use for the cloned directory.

5. Type the following command in the terminal (after the git clone you will need to paste the link you copied in step 3 above):

    ```bash
    git clone { & THE LINK FROM STEP 3 }
    ```

6. Set up a virtual environment.

7. INSTALLATION PACKAGES COMMANDS NEED TO BE LISTED HERE Install the packages from the requirements.txt file by running the following command in the Terminal:

    ```bash
    pip3 install -r requirements.txt
    ```

- - -

## Testing


- - -

## Credits

### Content

Content for this project was written by Leah Jones, Dana Ciobotaru, Phoebe Cowan, Ella Rees, Anni Sutt and Delyth Jennings. 

The film descriptions, images, rating and streaming services information were provided throughthe movie API.

### Media
***INCLUDE ANY WEBSITES OF IMAGES/CLIPS used here***
* Named image - [Description](https://www.imagewebsitelink.com)
* Named image - [Description](https://www.imagewebsitelink.com)
* Named image - [Description](https://www.imagewebsitelink.com)

### Acknowledgments

I would like to acknowledge the following people who helped me along the way in completing this project:

* My family for their patience while I worked on this project.
* Hamed Pour and Jack Jorgensen for being excellent instructurs on the CFG Degree course.
* Fatihah and Abilash - the assistant instructors on our course for all the feedback on the homework and assessments.
* Hope - our project instructor for your help during the last few weeks of the course.
