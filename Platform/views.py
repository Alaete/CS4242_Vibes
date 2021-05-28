from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from .forms import NewVibeForm, NewRevibeForm
from .models import Vibe, Revibe
from .sentiment_analysis import analyse_sentiment


def home(request):
    vibes = Vibe.objects.all()
    return render(request, 'home.html', {'vibes': vibes})


def vibe(request, pk):
    vibe = get_object_or_404(Vibe, pk=pk)
    return render(request, 'vibe.html', {'vibe': vibe})


def revibe(request, pk, revibe_pk):
    vibe = get_object_or_404(Vibe, pk=pk)
    revibe = get_object_or_404(Revibe, pk=revibe_pk)
    return render(request, 'revibe.html', {'vibe': vibe, 'revibe': revibe})


def vibe_revibes(request, pk):
    vibe = get_object_or_404(Vibe, pk=pk)
    return render(request, 'vibe_revibes.html', {'vibe': vibe})


@login_required
def new_vibe(request):
    if request.method == 'POST':
        form = NewVibeForm(request.POST)
        if form.is_valid():
            vibe = form.save(commit=False)
            vibe.body = form.cleaned_data.get('title')
            vibe.body = form.cleaned_data.get('body')
            vibe.sentiment = analyse_sentiment(vibe.body)
            vibe.created_by = request.user
            vibe.created_at = timezone.now()
            vibe.save()
            return redirect('home')
    else:
        form = NewVibeForm()
    return render(request, 'new_vibe.html', {'form': form})


@login_required
def new_revibe(request, pk):
    vibe = get_object_or_404(Vibe, pk=pk)
    if request.method == 'POST':
        form = NewRevibeForm(request.POST)
        if form.is_valid():
            revibe = form.save(commit=False)
            revibe.title = form.cleaned_data.get('title')
            revibe.body = form.cleaned_data.get('body')
            revibe.sentiment = analyse_sentiment(vibe.body)
            revibe.original = vibe
            revibe.created_by = request.user
            revibe.created_at = timezone.now()
            revibe.save()
            return redirect('vibe_revibes', pk=pk)
    else:
        form = NewRevibeForm()
    return render(request, 'new_revibe.html', {'vibe': vibe, 'form': form})


@method_decorator(login_required, name='dispatch')
class VibeUpdateView(UpdateView):
    model = Vibe
    fields = ('body', )
    template_name = 'edit_vibe.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'vibe'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        vibe = form.save(commit=False)
        vibe.sentiment = analyse_sentiment(vibe.body)
        vibe.edited_at = timezone.now()
        vibe.save()
        return redirect('vibe', pk=vibe.pk)


@method_decorator(login_required, name='dispatch')
class RevibeUpdateView(UpdateView):
    model = Revibe
    fields = ('body',)
    template_name = 'edit_revibe.html'
    pk_url_kwarg = 'revibe_pk'
    context_object_name = 'revibe'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(created_by=self.request.user)

    def form_valid(self, form):
        revibe = form.save(commit=False)
        revibe.sentiment = analyse_sentiment(revibe.body)
        revibe.edited_at = timezone.now()
        revibe.save()
        return redirect('revibe', pk=revibe.original.pk, revibe_pk=revibe.pk)
