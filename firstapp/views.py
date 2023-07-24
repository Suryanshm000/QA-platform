from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Question, Comment
from .forms import QuestionForm, CommentForm
from django.views.generic import (TemplateView,ListView,
                                  DetailView,CreateView,
                                  UpdateView,DeleteView)

from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class QuestionListView(ListView):
    model = Question

    # def get_queryset(self):
    #     return Question.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')


class QuestionDetailView(DetailView):
    model = Question


class CreateQuestionView(LoginRequiredMixin,CreateView):
    # redirect_field_name = 'firstapp/question_detail.html'

    form_class = QuestionForm

    model = Question

    def post(self, request):
        title = request.POST.get('title')
        text = request.POST.get('text')
        author = request.user
        question = Question.objects.create(title=title, text=text, author=author)
        return redirect('question_detail', pk=question.id)


@login_required
def add_comment(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.question = question
            comment.save()
            return redirect('question_detail', pk=question.pk)
    else:
        form = CommentForm()
    return render(request, 'firstapp/comment_form.html', {'form': form})


@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, id=pk)
    if request.user in comment.likes.all():
        # User already liked the answer, remove the like
        comment.likes.remove(request.user)
    else:
        # User hasn't liked the answer, add the like
        comment.likes.add(request.user)
    return redirect('question_detail', pk=comment.question.id)