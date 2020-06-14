
from unittest import TestCase
from django.test import Client,TestCase
from django.urls import reverse
from .models import Post, Group
from django.contrib.auth.models import User

class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.adminuser = User.objects.create_superuser(username="Raiqw2eserom", email="Raiqw2eserom@gmail.com", password="Raiqwe2seromwe!")
        self.user = User.objects.user(username="Ivanыфв1ew234", email="Raiqw2esqeqweeeqwerom@gmail.com", password="Raieqweqwe2seromwe!",follow=True)
        self.group = Group.objects.create(title="title", slug='slug-qwerewq', description='description')

    def test_profile(self):
        self.client.login(username="")
        response = self.client.get("/Ivan/")
        self.assertEqual(response.status_code, 200)

    def test_auth_user_can_publish1(self):
        self.client.login(username="Ivan")
        post = Post()
        post.text = "Text"
        resp = self.client.post("/new/", kwargs={'post': post}, follow=True)
        self.assertEqual(resp.status_code, 200)

    def test_no_auth_user_can_not_publish(self):
        resp = self.client.get(reverse('new_post'))
        self.assertRedirects(resp,"/auth/login/?next=/new/")
            
#вариант 2
    def test_auth_user_can_publish0(self):
        resp = self.client.post(reverse("new_post"), data={'group': self.group.id, 'text': self.text}, follow=True)
        self.assertEqual(resp.status_code, 200)
        created_post = Post.objects.filter(author=self.user).all().first()
        self.assertEqual(created_post.text, self.text)
        self.assertEqual(created_post.group, self.group)
        self.assertEqual(created_post.author, self.user)
        self.assertEqual(Post.objects.all().count(), 1)
    
    def test_check_post(self,user, group):
        post = Post.objects.create(text=self.text, author=self.user, )
        list_urls = (reverse('index'), reverse('profile', kwargs={'username': self.user.username}),
                 reverse('post', kwargs={'username': self.user.username, 'post_id': post.id}))
        for url in list_urls:
            self.check_contain_post(url, self.user, self.group)
    
    def check_contain_post(self, url, user, group):
        latest_post = Post.objects.filter(author=self.user).all().first()
        resp = self.client.get(url)
        if resp.context['paginator'].count == 1:
            post = resp.context['page'][0]
        else:
            post = resp.context['post']
        self.assertEqual(post.text, self.text)
        self.assertEqual(post.group, self.group)
        self.assertEqual(post.author, self.user)