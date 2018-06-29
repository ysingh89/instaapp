import json

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse

from .forms import Login, UserSignUp, PostForm
from .models import Comment, Follow, Likes, Posts, Users

# Create your views here.

def getCount(u_id):
    u = ""
    m = tuple()
    try:
        u = Users.objects.get(pk=u_id)
    except Exception as e:
        print(e)
        return "User doesn't exist"
    else:
        posts_count = Posts.objects.filter(userid__pk=u_id).count()
        followers_count = Follow.objects.filter(following__pk=u_id).count()
        following_count = Follow.objects.filter(follower__pk=u_id).count()
        m = (u,posts_count,followers_count,following_count)
    return m


def ajaxObj(request):
    obj = json.dumps([{1:{'Uno':"One"},2:"Two",3:"Three"}])
    return HttpResponse(obj)
    # pass




def likedBy(request, post_id):
    post = Posts.objects.get(pk=post_id)
    usersLiked = Likes.objects.filter(postid__pk=post_id)
    # print(usersLiked)
    return render(request, 'myapp/likedby.html', {'post':post, 'usersLiked':usersLiked})


def likePost(request, post_id):
    l = ""
    try:
        l = Likes.objects.get(postid__pk=post_id, userid__pk=request.session['username'])
    except Exception as e:
        l = Likes(
            postid=Posts.objects.get(pk=post_id),
            userid=Users.objects.get(pk=request.session['username'])
        )
        l.save()
    else:
        l.delete()
    return home(request)

def makeComment(request, post_id):
    if request.method == 'POST':
        post = Posts.objects.get(pk=post_id)
        user = Users.objects.get(pk=request.session['username'])
        c = Comment(
            content = request.POST['comment'],
            postid = post,
            userid = user
        )
        c.save()
        return home(request)


def following(request):
    data=""
    try:
        data = Follow.objects.filter(follower__pk=request.POST['profile_id'])
    except Exception as e:
        HttpResponseRedirect('home')
    else:
        return render(request, 'myapp/following.html', {'data':data, 'id':request.POST['profile_id']})

def followers(request):
    data = ""
    try:
        data = Follow.objects.filter(following__pk=request.POST['profile_id'])
    except Exception as e:
        HttpResponseRedirect('home')
    else:
        return render(request, 'myapp/followers.html', {'data':data, 'id':request.POST['profile_id']})

def follow(request):
    form = request.POST
    # print(form)
    if request.session.has_key('username'):
        follower = Users.objects.get(pk=request.session['username'])
        following = Users.objects.get(pk=form['user_id'])
        redirect_url = "profile/"+form['user_id']
        print(redirect_url)
        # Check if submit value unfollow
        if form['submit'] == 'Unfollow':
            # delete entry
            to_delete = Follow.objects.get(follower__pk=request.session['username'], following__pk=form['user_id'])
            to_delete.delete()
            return HttpResponseRedirect(redirect_url)
        else:
            table = Follow(
            follower = follower,
            following = following
            )
            table.save()
            return HttpResponseRedirect(redirect_url)
    else:
        return HttpResponseRedirect('login')


def displayImage(request, post_id):
    print(post_id)
    post = Posts.objects.get(pk=post_id)
    return render(request, 'myapp/displayimage.html', {'post':post})

def profilePage(request, u_id):
    data = getCount(u_id)
    context = dict()
    flag=""
    if request.session['username'] != u_id:
        flag=True
        # print("Same person")
    # Check if logged in user already follows that profile
    try:
        Follow.objects.get(follower__pk=request.session['username'], following__pk=u_id)
    except Exception as e:
        print(e)
        context['follow'] = False
    else:
        context['follow'] = True
    if type(data) == tuple:
        context['user_info'] = data[0]
        context['posts_count'] = data[1]
        context['followers_count'] = data[2]
        context['following_count'] = data[3]
        context['posts'] = Posts.objects.filter(userid__pk=u_id).order_by('-timestamp')
        if flag:
            context['not_same_person'] = True
        return render(request, 'myapp/profile.html', context)
    else:
        return render(request, 'myapp/profile.html', {'no_user':"No user found with that ID."})
        print("No user found")

def searchProfile(request):
    # print(request.POST['search'])
    u = Users.objects.filter(username__startswith=request.POST['search'])
    q = request.POST['search']
    return render(request, 'myapp/searchuser.html', {'users':u, 'query':q})



def makePost(request):
    if request.POST:
        formPost = request.POST
    if request.FILES:
        formFile = request.FILES
    user= Users.objects.get(pk=request.session['username'])
    p = Posts(
        title = formPost['title'],
        image = formFile['image'],
        userid = user
    )
    p.save()
    print(formPost,formFile)
    return HttpResponseRedirect('home')

def usersIFollows(user_id):
    return Follow.objects.filter(follower__pk=user_id)

def getUsersIdsIFollow(var):
    return [user.following.username for user in var]

def getSortedPostsList(username):
    usersIds = getUsersIdsIFollow(usersIFollows(username))
    sortedPosts = Posts.objects.filter(userid__pk__in = usersIds).order_by('-timestamp')
    postList = list()
    for post in sortedPosts:
        count = Likes.objects.filter(postid__pk=post.id).count()
        like = ""
        try:
            Likes.objects.get(postid__pk=post.id, userid=username)
        except Exception as e:
            like = False
        else:
            like = True
        comments = ""
        try:
            comments = Comment.objects.filter(postid__pk=post.id).order_by('-timestamp')
        except Exception as e:
            comments = False
        else:
            comments = list(comments)
        postList.append((count,post,like,comments))
    return postList


def home(request):
    if request.session.has_key('username'):
        q = Users.objects.get(pk=request.session['username'])
        context = dict()
        context['form'] = PostForm()
        context['name'] = q.fname+" "+q.lname
        context['postList'] = getSortedPostsList(q.username)
        return render(request, 'myapp/home.html', context)
    else:
        return render(request, 'myapp/home.html')

def logOut(request):
    if request.session.has_key('username'):
        request.session.flush()
    return HttpResponseRedirect('home')



def logIn(request):
    if request.method=='POST':
        form = request.POST
        q=""
        # Check if username exist
        try:
            q = Users.objects.get(username=form['username'])
        except Exception as e:
            print(e)
            return HttpResponseRedirect('signup')
        else:
            # if password matches
            if q.password == form['password']:
                request.session['username'] = form['username']
                return HttpResponseRedirect('home')
            else:
                reform = Login()
                wrongpassword = "The password was wrong. Please retry"
                return render(request, 'myapp/login.html', {'form':reform, 'message': wrongpassword})
        return render(request, 'myapp/login.html')
    else:
        form = Login()
        return render(request, 'myapp/login.html', {'form':form})


def signUp(request):
    if request.method=='POST':
        form = request.POST
        try:
            Users.objects.get(pk=form['username'])
        except Exception as e:
            print(e)
            image = ""
            if request.FILES:
                image = request.FILES['userimage']
            table = Users(
                username = form['username'],
                password = form['password'],
                userimage = image,
                fname = form['fname'].title(),
                lname = form['lname'].title(),
                phone = form['phone'],
                email = form['email']
            )
            table.save()
            return HttpResponseRedirect('login')
        else:
            return HttpResponseRedirect('signup')
    else:
        form = UserSignUp()
        return render(request, 'myapp/signup.html', {'form':form})
