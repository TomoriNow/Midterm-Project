# Midterm-Project

## Group Name and Members
* Muhammad Sakhran Thayyib AKA Duden 2206046790 
* Galih Ibrahim Kurniawan 2206046696
* Gregorius Samuel Hutahean 2206046701
* Muhammad Sean Arsha Galant 2206822963
* Alvin Zhafif Afilla 2206046632


## The story of the application and its benefits

### Midoku’s Story and Benefits

Keeping track of your reading progress can be a persistent challenge when delving into the world of books, especially in today’s digital age. This issue becomes even more pronounced with online books, manga, manhwa, and light novels, as they often receive sporadic updates, sometimes with significant gaps between new chapters. When you find yourself engrossed in multiple forms of literature simultaneously, it’s all too easy for your reading experiences to blur together, leaving you uncertain about what you’ve already perused.<br><br>

In this increasingly interconnected world of literature, the need to remember where you last left off is a constant concern. As avid readers, you don’t want to start a book from the beginning just because you’ve lost your place. That’s where Midoku comes in — your reliable companion for effortlessly tracking your reading adventures. Whether your interests lie in manga, light novels, manhwa or any other genre, “Midoku” is purpose-built to ensure you never lose your reading progress again. Designed with readers in mind, it empowers you to manage your literary journeys with ease, making sure you’re always in control of your reading experience, anytime, anywhere.<br><br>

—
" Midoku " isn't just your run-of-the-mill reading companion; it's a versatile tool designed to enhance your literary journey in more ways than one. With a vast catalog boasting over 100 titles, you can effortlessly curate your personal reading list, marking the books you've devoured and tracking your progress down to the last chapter. But that's not all—here's where the magic happens.<br><br>

What if you stumble upon a hidden gem that's not yet in our catalog? No need to fret! " Midoku " offers you the freedom to add any book, complete with all the relevant information, directly to your collection. This feature opens the door to a world of literary treasures that might be elusive or underappreciated, allowing you to share these newfound gems with your friends. There's a unique joy in introducing your buddies to a literary masterpiece that's yet to hit the mainstream.<br><br>

But wait, there's more! We've implemented a tagging system that lets you describe the key aspects of each piece of literature. Whether you're craving heart-pounding action, heart-fluttering romance, or side-splitting comedy, our tags simplify your search for the perfect read. Looking for something that defies categorization? Users can even submit their own tags for review by our diligent admins, expanding the available list of tags and ensuring you find precisely what you're looking for in your literary adventures. With " Midoku ," your reading experience is not just organized; it's tailor-made to suit your every literary whim.<br><br>

Each book is meticulously curated, accompanied by detailed plot descriptions that transport readers into the heart of the story. Whether you are a fan of gripping mysteries, heartwarming romances, mind-bending science fiction, or insightful non-fiction, Midoku has something for everyone. The plot descriptions provided on the website are not mere summaries but expertly crafted narratives that entice readers, giving them a glimpse into the intriguing twists and turns that await within the pages of each book. Exploring new literary adventures has never been more immersive and delightful.<br><br>

Apart from your usual manga-reading sites, our site provides you with your very own personal space where you can exclusively read and store information about your collection. Thinking about tracking your own progress in reading through a handful of manga at a time? Or do you keep forgetting the name of a book and have to search for it painstakingly? Fear not! You can now seamlessly track your own progress for every manga encountered and search through them with minimum effort. This way, you won’t have to worry about losing progress on any manga or book ever again and admire your glorious collection with all the privacy you need. If the book or manga you’re looking for is not listed within our catalog, then you can easily add your desired piece of literature without restriction to your list. Feel the freedom of adding countless manga and books to your list and even share it among your friends if you wish to!<br><br>

Made by you, and made for you. 

________________________
# List of modules (or, features) that will be implemented

Note: this is awork in progress, certain functions or implementations are subject to change
## List of functions
__Catalog page:__ 
 * **Description:** The list of all books from the catalog.
 * **Features:** View, Add books to own list(requires login).

__Other user's list page:__ 
 * **Description:** The list of other user's.
 * **Features:** View, Add books to own list(requires login), Delete Entries(requires login, must be admin or higher).

__User's list page:__ 
 * **Description:** Your own book list.
 * **Features:** View, Edit/Delete/Add entries(requires login, must be the user associated to the page), Change favourite book(requires login. must be user associated to the page)

__Admin page:__ 
 * **Description:** Page with all admin functions.
 * **Features:** {Accessable only after login and if the user is an admin, the same is trye for all related features}, View list of all users and requests, Accept or reject requests, Delete Users, make User an admin(must be the super user

## List of Models to be implemented

### User Model
__Username__

__Password__

__Admin and SuperUser flag - To identify whether they are admin or superuser. Implementation is subject to 

__Favourite book (Foreign Key to Book Entry)__

### Book Model (for the catalog) Attributes List:

__Number/ID — Number is according to when it is added, i.e. ID number 1 is added before ID number 3__

__Book Name__

__Book Type__:
1. Book, like a normal book
2. Manga / Comics
3. Manhwa
    
__Author__

__Book Status__  
1. Mostly prominent with Mangas/Manhwas
2. Finished, Ongoing, Hiatus, Cancelled

__Description / Summary__
1. Alphanumeric, by the user

__Tags — We keep a curated database of tags created by the admins (like in My Anime List) but users can submit new tags, which if approved by the admins, will be added to the website__
1. Vanilla, romance, horror, etc. (kinda like mal tags)
        
__Publisher (Optional)__

### Book Entry Model (in the User's list)

__Book - (foreign key to books in catalog, false if the book isn't in the catalog)__

__Custom Book(flag) - (True if the book isn't from the catalog, False otherwise)__

__Custom Book Attributes - the attributes from the Book model that the user fills out themselves. Empty if the book is from the catalog__

*__Reading Status — for user__
1. Not finished, reading, finished

__Last Chapter Read — entered by the user__

__Last Date Read — once last chapter read is updated, it will automatically update the last date read data__

__Notes - (where users can note info about the story, or certain chapters)__ 

__Text Review__

__Rating__
1. Numeric, from 0 to 10, can be decimal

________________________
## The source of the book catalog dataset
crxxom. “Manhwa dataset.” Kaggle, July 2023, https://www.kaggle.com/datasets/crxxom/manhwa-dataset. Accessed 10 October 2023.

AJ Pass. “TOP RANKED MANGAS MyAnimeList (MAL).” Kaggle, 9 March 2019, https://www.kaggle.com/datasets/ajpass/top-ranked-mangas-myanimelist-mal. Accessed 10 October 2023.

Soeiro, Victor. “Manga, Manhwa and Manhua Dataset.” Manga, Manhwa and Manhua Dataset - Kaggle, 9 March 2019, https://www.kaggle.com/datasets/victorsoeiro/manga-manhwa-and-manhua-dataset/. Accessed 10 October 2023.

________________________
## User roles
Owner/Superuser - The Owner (or the Superuser) in our web application has the ability add and remove admins. The Owner/Superuser is also able to perform all the operations that admins and user can do.

Admin - The Admin is capable of accepting or rejecting tag (such as adding tags) and book (such as adding books to the catalog) requests. However, the admin is not capable of adding more admins into the web application.

User - The User is able to add books to their own list (which can be from the catalog or they can add all of the details of the book that they have read themselves), share their lists to other users, as well as add reviews and edit the last-read attribute to books in their list. They can also submit possible book tags or books for the catalog that the admins can accept or deny before adding them to the web application for other users to see publicly. 
