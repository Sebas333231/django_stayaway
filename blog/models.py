from django.db import models
from django import forms
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from taggit.models import TaggedItemBase
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.contrib.taggit import ClusterTaggableManager
# Create your models here.

class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'PostPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )

class BlogTagIndexPage(Page):

    def get_context(self, request):

        # Filter by tag
        tag = request.GET.get('tag')
        postpage = PostPage.objects.filter(tags__name=tag)

        # Update template context
        context = super().get_context(request)
        context['postpage'] = postpage
        return context
    

class BlogPage(Page):
    intro = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('authors', widget= forms.CheckboxSelectMultiple),
    ]

class SeccionPage(Page):
    date = models.DateField('Post Date')
    summary = models.CharField(max_length=250)
    body = RichTextField()

    authors = ParentalManyToManyField('blog.Author', blank=True)

    content_panels = Page.content_panels +[
        FieldPanel('date'),
        FieldPanel('authors', widget= forms.CheckboxSelectMultiple),
        FieldPanel('summary'),
        FieldPanel('body'),
        InlinePanel('gallery_images', label="Gallery images")

    ]

    parent_page_type = [
        "PostPage"
    ]
    
class PostPage(Page):
    date = models.DateField('Post Date')
    summary = models.CharField(max_length=250)
    body = RichTextField()
    imagen = RichTextField(blank=True)
    authors = ParentalManyToManyField('blog.Author', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels +[
        FieldPanel('date'),
        FieldPanel('authors', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
        FieldPanel('summary'),
        FieldPanel('body'),
        FieldPanel('imagen'),
        InlinePanel('gallery_images', label="Gallery images")
    ]

    parent_page_type = [
        "BlogPage"
    ]
    subpage_types = [
        "SeccionPage"
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(PostPage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption')
    ]

class SeccionPageGalleryImage(Orderable):
    page = ParentalKey(SeccionPage, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption')
    ]

@register_snippet
class Author(models.Model):
    name = models.CharField(max_length=255)
    author_image = models.ForeignKey(
        'wagtailimages.Image', null=True, blank=True,
        on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)
    correo = models.CharField(blank=True, max_length=250)

    pannels = [
        FieldPanel('name'),
        InlinePanel('author_image', label="Gallery Images"),
        FieldPanel('caption'),
        FieldPanel('correo')
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Authors'

