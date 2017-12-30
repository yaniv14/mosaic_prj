from builtins import super

import folium
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView
from folium.plugins import MarkerCluster
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotFound
from django.shortcuts import render

from main.forms import TagForm, MosaicSiteForm, MosaicItemForm, MosaicItemUpdateForm
from main.models import Tag, MosaicItem, MosaicPicture, MosaicSite
from django.utils.translation import ugettext as _

from mosaic_prj.base_views import IAAUIMixin


class HomeView(IAAUIMixin, TemplateView):
    template_name = 'main/home.html'
    page_title = _('Home page')
    page_name = 'home'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['popular_site'] = MosaicSite.objects.filter(featured=True)[:5]
        return context


class MosaicView(DetailView):
    model = MosaicItem
    template_name = 'main/mosaic_detail.html'
    context_object_name = 'mosaic'


class TagCreateView(IAAUIMixin, CreateView):
    template_name = 'main/tag_form.html'
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('main:tag_create')
    page_title = _('Tag create')
    page_name = 'tag_create'

    def get_context_data(self, **kwargs):
        d = super(TagCreateView, self).get_context_data(**kwargs)
        d['tags'] = Tag.objects.all()
        return d


class TagUpdateView(IAAUIMixin, UpdateView):
    template_name = 'main/tag_form.html'
    model = Tag
    form_class = TagForm
    success_url = reverse_lazy('main:tag_create')
    page_title = _('Tag update')
    page_name = 'tag_update'


class TagDeleteView(IAAUIMixin, DeleteView):
    model = Tag
    success_url = reverse_lazy('main:tag_create')


class MosaicSiteCreateView(SuccessMessageMixin, IAAUIMixin, CreateView):
    template_name = 'main/mosaic_site_form.html'
    model = MosaicSite
    form_class = MosaicSiteForm
    success_url = reverse_lazy('main:site_create')
    success_message = _('Mosaic site created successfully')
    page_title = _('Mosaic site create')
    page_name = 'mosaic_site_create'

    def get_context_data(self, **kwargs):
        d = super(MosaicSiteCreateView, self).get_context_data(**kwargs)
        d['sites'] = MosaicSite.objects.all()
        return d


class MosaicSiteUpdateView(SuccessMessageMixin, IAAUIMixin, UpdateView):
    template_name = 'main/mosaic_site_form.html'
    model = MosaicSite
    form_class = MosaicSiteForm
    success_url = reverse_lazy('main:site_create')
    success_message = _('Mosaic site updated successfully')
    page_title = _('Mosaic site update')
    page_name = 'mosaic_site_update'


class MosaicSiteDeleteView(IAAUIMixin, DeleteView):
    model = MosaicSite
    success_url = reverse_lazy('main:site_create')


class MosaicItemCreateView(SuccessMessageMixin, IAAUIMixin, CreateView):
    template_name = 'main/mosaic_item_form.html'
    model = MosaicItem
    form_class = MosaicItemForm
    success_message = _('Mosaic item created successfully')
    page_title = _('Mosaic item create')
    page_name = 'mosaic_sitem_create'

    def get_success_url(self):
        return reverse_lazy('main:item_create')

    def get_context_data(self, **kwargs):
        d = super(MosaicItemCreateView, self).get_context_data(**kwargs)
        d['items'] = MosaicItem.objects.all()
        return d


class MosaicItemUpdateView(SuccessMessageMixin, IAAUIMixin, UpdateView):
    template_name = 'main/mosaic_item_form.html'
    model = MosaicItem
    form_class = MosaicItemUpdateForm
    success_message = _('Mosaic item updated successfully')
    page_title = _('Mosaic item update')
    page_name = 'mosaic_item_update'

    def get_initial(self):
        return {
            'materials': tuple(self.object.materials)
        }

    def get_success_url(self):
        return reverse_lazy('main:item_create')


class MosaicItemDeleteView(SuccessMessageMixin, IAAUIMixin, DeleteView):
    model = MosaicItem
    success_message = _('Mosaic item deleted successfully')

    def get_success_url(self):
        return reverse_lazy('main:item_create')


def tags(request):
    print("in")
    tags_list = Tag.objects.all()
    for tag in tags_list:
        print(tag.tag)
    tags = [tag.tag for tag in tags_list]
    d = {
        'tags': tags_list
    }
    return render(request, "tags.html", d)


def tag_page(request, tagid):
    try:
        tag = Tag.objects.get(id=tagid)
    except ObjectDoesNotExist:
        return HttpResponseNotFound('<h1>Page not found</h1>')

    mosaics = set(MosaicItem.objects.filter(tags=tag))
    # mosaic_pics = MosaicPicture.objects.filter(mosaic__tags = tag)
    mosaic_pics = []
    if len(mosaics) == 0:
        return HttpResponseNotFound('<h1>No Mosaics with this tag</h1>')

    for mosaic in mosaics:
        pictures = MosaicPicture.objects.filter(mosaic=mosaic).order_by('order_priority')
        mosaic_pics.append(pictures[0])

    d = {
        'mosaics': mosaics,
        'mosaic_pics': mosaic_pics
    }

    return render(request, "tag_page.html", d)


def mosaic_map(request):
    mosaics = MosaicItem.objects.all()
    m = folium.Map(
        location=[31.781959, 35.2137],
        tiles='Stamen Toner',
        zoom_start=12
    )
    marker_cluster = MarkerCluster().add_to(m)
    for point in mosaics:
        folium.Marker(
            location=[point.dimen_width, point.dimen_length],
            popup=point.title
        ).add_to(marker_cluster)
    m.save("main/templates/map.html")

    return render(request, "map_page.html")
