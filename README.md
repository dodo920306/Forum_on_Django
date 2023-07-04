# Forun on Django
## Prerequisites
Please ensure that you already have Docker & Docker-compose on your computer, you can find more information according to your system [on this docker official page](https://docs.docker.com/engine/install/). Please prepare an email account and password for the forum, and ensure that this password **can be used as app password** as shown in [this page](https://support.google.com/accounts/answer/185833).

## Installation
First of all, please clone this repo to the local directory.
```!bash
$ git clone https://github.com/dodo920306/Forum_on_Django.git
```
Next, run the script to initialize the project.
```!bash
$ ./init.sh
```
Please follow the instructions from the script to enter the email account and password as mentioned in prerequisites, after that you should provide the port this website should be on.

You can use the command:
```!bash
$ cat ./.env
```
to check out if the project has been configured successfully or not. Three variable, PORT, EMAIL_USER, and EMAIL_PASSWORD, should be changed according to your previous input.

You may want to add your ip in order to be able to access the website later. Just add it in the DJANGO_ALLOWED_HOSTS variable in the .env file. Note that you should use space to seperate different hosts.

You may also want to change the SECRET_KEY variable for security reasons. You can use tools like [Djecrety](https://djecrety.ir/) to get you personal key if you don't have one.

If every thing in .env is OK, run
```!bash
$ ./setup.sh
```
to set up the website.

You can use command like
```!bash
$ curl -L http://localhost:<port>
```
to check that whether the website is running or not. By default, the website can also be access through localhost unless you delete it from DJANGO_ALLOWED_HOSTS in .env. ":\<port>" can be ommitted if PORT variable in .env is 80 as default.

You should get a html file for the login page if the website is fine.

Then, please use the below command to register a super user as website admin:
```!bash
$ sudo docker-compose -f docker-compose.yml exec web python manage.py createsuperuser
```
Please follow the instructions to finish signing up an admin and memorize the account and the password.

Now, you can use any one of the hosts you see in DJANGO_ALLOWED_HOSTS variable in .env to access to the webiste by url like http://\<DJANGO_ALLOWED_HOST>:\<port> by your browser. ":\<port>" can be ommitted if PORT variable in .env is 80 as default.

If you successfully enter the login page on your browser, use the account and password you use to register the super user previously. If you succeed to login, you can see a barely empty page with title 「看板列表」.

You can see the option 「控制台」 on the upper right corner. Click it to enter the admin page. You can find the option "Board" on the page, you can use it to create new boards in your forum and assign moderators for them.

Return to the website, if you find the boards you just create shown on the page. Congratulations. You just finished the preliminarily setup of the website.

The last thing you should do is check if email works fine. You can register new users by the 「立即註冊」 option on the login page. The forum will send an email to new users if they filled in their email when registration to verify their email.

Please check out if users can receive the email verification emails successfully.

If you encounter any problem, use
```!bash
$ ./log.sh
```
to get more information.

Last but not least, you can use
```!bash
$ ./off.sh
```
to pause the website if needed.

If you encounter any further question, please contact with me.

## Installation illustration
If there is any thing confusing during installation, please check out [the installation illustration video](https://youtu.be/KiJNDyjdVDU).