
from unittest import TestCase
from django.test import Client,TestCase
from django.urls import reverse
from .models import Post, Group
from django.contrib.auth.models import User


class TestPostsUnauthorized(TestCase):
    def setUp(self):
        self.client = Client()

    def test_no_auth_user_redirect(self):
        resp = self.client.get(reverse('new_post'))
        self.assertRedirects(resp,"/auth/login/?next=/new/")

        resp = self.client.post(
            reverse('new_post'),
            data={'group':'', 'text':'test123'}
        )
        self.assertRedirects(resp,"/auth/login/?next=/new/")
        self.assertEqual(Post.objects.all().count(), 0)
     

class TestPostsAuthorized(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="Testuser",
            email="test@gmail.com",
            password="Raieqweqwe2seromwe!"
            )
        self.group = Group.objects.create(
            title="title",
            slug='slug-qwerewq',
            description='description'
            )
        self.client.force_login(self.user)

    def test_profile(self):
        response = self.client.get(
            reverse('profile', kwargs={'username': self.user.username})
            )
        self.assertEqual(response.status_code, 200)
            
    def test_auth_user_can_publish(self):
        resp = self.client.post(
            reverse("new_post"),
            data={'group': self.group.id, 'text': 'test'},
            follow=True
            )
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
        created_post = Post.objects.all().first()
        self.assertEqual(created_post.text, 'test')
        self.assertEqual(created_post.group, self.group)
        self.assertEqual(created_post.author, self.user)
        self.assertEqual(Post.objects.count(), 1)
    
    def test_check_post(self):
        post = Post.objects.create(text='text', author=self.user, group=self.group)
        list_urls = [
            reverse('index'),
            reverse('profile', kwargs={'username': self.user.username}),
            reverse('post', kwargs={'username': self.user.username, 'post_id': post.id})
        ]
        for url in list_urls:
            self.check_contain_post(url, self.user, self.group, post.text)

    def check_contain_post(self, url, user, group, text):
        resp = self.client.get(url)
        if 'paginator' in resp.context.keys():
            post = resp.context['page'][0]
        else:
            post = resp.context['post']
        self.assertEqual(post.text, text)
        self.assertEqual(post.group, group)
        self.assertEqual(post.author, self.user)

    def test_post_edit(self):
        post = Post.objects.create(text='text_test', author=self.user, group=self.group)
        url_edit = reverse('post_edit', kwargs={
            'username': self.user.username,
            'post_id': post.id,
            }
        )
        list_urls = [
            reverse('index'),
            reverse('profile', kwargs={'username': self.user.username}),
            reverse('post', kwargs={'username': self.user.username, 'post_id': post.id})
        ]
        resp = self.client.get(url_edit)

        self.assertEqual(resp.status_code, 200)

        new_group = Group.objects.create(
            title="new_title",
            slug='slug-new',
            description='new_description'
        )
        post_data = {
            'group': new_group.id,
            'text': 'text_ediq  weter',
        }

        self.client.post(url_edit, data=post_data)

        for url in list_urls:
            self.check_contain_post(url, self.user, new_group, post_data['text'])