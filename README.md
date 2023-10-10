# Midterm-Project

## Group Name and Members
* Muhammad Sakhran Thayyib AKA Duden 2206046790 
* Galih Ibrahim Kurniawan 2206046696
* Gregorius Samuel Hutahean 2206046701
* Muhammad Sean Arsha Galant 2206822963
* Alvin Zhafif Afilla 2206046632


## The story of the application and its benefits

________________________
## List of Modules to be implemented


### Book Model Attributes List:

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

*__Reading Status — for user__
1. Not finished, reading, finished

__Last Chapter Read — entered by the user__

__Last Date Read — once last chapter read is updated, it will automatically update the last date read data__

__Text Review__

__Rating__
1. Numeric, from 0 to 10, can be decimal
        
__Publisher (Optional)__

________________________
## The source of the book catalog dataset
Soeiro, Victor. “Manga, Manhwa and Manhua Dataset.” Manga, Manhwa and Manhua Dataset - Kaggle, 9 March 2019, https://www.kaggle.com/datasets/victorsoeiro/manga-manhwa-and-manhua-dataset/. Accessed 10 October 2023.

________________________
## User roles
Owner - Adds and removes admins. Are also able to perform tasks that admins and user can do.

Admin - Accepts/rejects tag (adding tags) or book (adding books to the catalog) requests, is able to see other users' list. Can not add more admins.

User - Able to add books to their own list ( can be from the catalog or they can the book add all of the details themselves), share their lists to other users, add reviews and edit the last read attribute to books in their list. They can also submit possible book tags or books for the catalog that the admins can accept or deny
