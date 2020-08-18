# Sehir University Faculty Member Searcher

This Software Builted for Sehir University. Student can benefits from this software to search their academian according to keyword.

## How It Looks Like
When the program run first time it will be looks like :
![1](https://user-images.githubusercontent.com/63451008/90455077-ad79a680-e0fd-11ea-8f17-ce65aa7366d4.PNG)



## Fetching Profiles
This is Sehir University Academians Link : https://www.sehir.edu.tr/en/academics/college-of-engineering-and-natural-sciences/academic-staff
When the student click Fetch profile program will be looks like and selenium webdriver will be opened.:
![2](https://user-images.githubusercontent.com/63451008/90455198-2416a400-e0fe-11ea-9851-9d73b32acaf8.PNG)


After that, webdriver automatically shuts down and BeautifulSoup proccess the professors informations.
While BeautifulSoup proccess informations process bar will be move according to professors numbers.
![3](https://user-images.githubusercontent.com/63451008/90455256-4dcfcb00-e0fe-11ea-8757-d420d4e52367.PNG)


When the informations collected  database which include professors informations will be created, and program will looks like that:
![4](https://user-images.githubusercontent.com/63451008/90455345-81aaf080-e0fe-11ea-8ab9-22c9ff45d4c3.PNG)


## Searching
When the search with given keywords program will brings informations about professors, and her/his score . Score is specifying according to keyword, program counts keywords and give them score.
![5](https://user-images.githubusercontent.com/63451008/90455562-039b1980-e0ff-11ea-81d4-39e64d35a36f.PNG)


Also, searching can be limited in terms of professors department. Example:
![7](https://user-images.githubusercontent.com/63451008/90455851-d307af80-e0ff-11ea-889c-a9f518e016a5.PNG)



## Double Clicking to Professors
If the student double clicking to professors, webdriver automatically open the professors link and student can examine its professors.
![6](https://user-images.githubusercontent.com/63451008/90455780-a18ee400-e0ff-11ea-9830-f2cbb76f4538.PNG)


## DatabaseSystem
Student don't have to fetch profile again and again every time. When program fetch profile one time its done.
If program re-run , at the first time it will be check professors informations again because new informations may be added.
It will be looks like that:
![8](https://user-images.githubusercontent.com/63451008/90455949-1d892c00-e100-11ea-8268-4d19247da561.PNG)


If no need to fetch profiles again(Professors informations not changed) database loaded successfully informations will be displayed.
![9](https://user-images.githubusercontent.com/63451008/90455980-398ccd80-e100-11ea-8dec-5a79c7f606b4.PNG)




## License
For Everyone
