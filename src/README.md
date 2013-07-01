Danmaku video
=============

1. Pre-install
--------------

To compile and run the codes, you need:

- django-1.5.1
- python-2.7

> Note:
>
> 1. In the `settings.py`, set `DEBUG=True` in order to
>
>   `python manage.py runserver`
>
> 2. If you'd like to start with an empty database
>
>   `rm danmaku.db`  
>   `python manage.py syncdb`

>3. There are two accounts in `danmaku.db`, the (username, passwd) pairs are:

>- (koyabr, 123)
>- (tc, 123)

The `Makefile` is used for epydoc, I've already generate a `docstrings` directory. Want to regenerate? Make sure epydoc is installed, or you should:

    pip install epydoc
or download from http://epydoc.sourceforge.net

Now generate documents by:

    make clean
    make

**Please email me if you run into any trouble when deploying the site. I've removed any third-party packages from my design to achieve best compatibility, but anything unexpected may happen, so please contact me before judgement, thanks.**

2. Website Guide
-------------------

To visit this site, you need:
* A modern web browser (firefox recommended) with JavaScript enabled
* Flash Player 11 or higher

The sitemap is quite simple:

- **Home page**: Show posts (a post contains links to a video and a thumbnail, with optional text notes) of different categories. 
- **Post page**: View details of a post, watch video, leave comments and follow people.
- **Manage page (post)**: organize your posts, publish a new one or edit an old one. 
- **Manage page (people)**: See who you are following and followed.

###Guides for tourist:


- Find interesting videos on homepage, you can switch categories or search from the top navbar, and sort posts by data/title.
- Watch videos and leave comments as you like, no need to login.
- Register if you like my site! Only members can rate posts and add them to favorite, or follow each other.

###Guides for member user:

- In order to have an avatar, please register your email at http://www.gravatar.com.

- You can rate posts in their detail page, add great ones to favorite, and follow the authors as you like.

- Manage your posts through "navbar -> right button -> My posts", publish/edit posts as you like, a post consists of:
    - title
    - category
    - vid (sina video)
    - thumbnail (external link)
    - text notes (optional, leave blank as you like)
    
    >Note: to add a sina video, you should provide its vid instead of pure url. 
    >
    >Find videos from http://you.video.sina.com.cn/c or upload your video to sina server.
    >
    >A typical url of sina video page is like http://video.sina.com.cn/v/b/57455040-1640601392.html, number before the dash is the vid we want (here it is 57455040).

- See other people through "navbar -> right button -> My people", click on their avatars/names to view their posts.

###For all users (members&tourists):

- The extra comment board below the flash player in every post is powered by Disqus, you must register ay their site or use a google/facebook/twitter account in order to comment. 
- Take it easy, the danmaku comment system is independent for use without any registration.


3. Code References
---------------

1. The danmaku flash player is provided by:

    http://code.google.com/p/mukioplayer/

2. The front-end framework is provided by:

    http://twitter.github.io/bootstrap/
    
3. The avatar service is powered by:

    http://www.gravatar.com
    
4. The comment board system is powered by:

    http://www.disqus.com
    
**Thanks to all developers for making it ful of joy to design&build a website.**


