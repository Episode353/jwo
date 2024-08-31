from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditForm, CommentForm
from django.http import HttpResponseRedirect
from django.db.models import Q

# Create your views here.

#def home(request):
#    return render(request, 'home.html', {})

def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('article-detail', args=[str(pk)]))

class HomeView(ListView):
    model = Post
    template_name = 'bloghome.html'
    ordering = ['-post_date']
    #ordering = ['-id']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu
        return context

def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list':cat_menu_list})



def CategoryView(request, cats):
    cats_cleaned = cats.replace('-', ' ').title()  # Capitalize first letters for proper matching
    print(f"Requested category: {cats}")
    print(f"Cleaned category: {cats_cleaned}")

    # Try to find the category by name, ignoring case
    try:
        category = Category.objects.get(Q(name__iexact=cats_cleaned))
        category_posts = Post.objects.filter(category=category)
    except Category.DoesNotExist:
        print("Category does not exist")
        return render(request, '404.html', status=404)

    # Debugging
    print(f"Number of posts found: {category_posts.count()}")

    return render(request, 'categories.html', {
        'cats': category.name,
        'category_posts': category_posts
    })





class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)

        post = self.object
        author = post.author
        # Fetch the profile related to the author
        author_profile = getattr(author, 'profile', None)  # This assumes the related name for the profile is 'profile'

        context["page_user"] = author_profile
        context["cat_menu"] = Category.objects.all()
        context["total_likes"] = post.total_likes()
        context["liked"] = post.likes.filter(id=self.request.user.id).exists()

        return context




class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    # fields = '__all__'
    # fields = ('title', 'body')
    success_url = reverse_lazy('bloghome')

    def get_form(self, form_class=None):
        form = super(AddPostView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form

class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = 'update_post.html'
    #fields = ['title', 'title_tag', 'body']
    success_url = reverse_lazy('bloghome')

    def get_form(self, form_class=None):
        form = super(UpdatePostView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'
    # fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)

    success_url = reverse_lazy('bloghome')

class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    fields = '__all__'
    success_url = reverse_lazy('bloghome')

    def get_form(self, form_class=None):
        form = super(AddCategoryView, self).get_form(form_class)
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form




class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('bloghome')