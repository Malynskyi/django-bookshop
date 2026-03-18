from django import forms
from books.forms import FilterBookForm, AuthorFilterForm, QueryFilterForm
from django.contrib.auth.mixins import UserPassesTestMixin


class UserFilteringMixin:
    user_field = ...

    def filter_by_user(self, queryset):
        return queryset.filter(**{self.user_field: self.request.user}) if self.request.user.is_authenticated else queryset
    

class AuthorFilteringMixin(UserFilteringMixin):
    user_field = 'author'

    def get_queryset(self):
        queryset = super().get_queryset()
        return self.filter_by_user(queryset)
    

class AuthorFilteredTemplateResponseMixin(UserFilteringMixin):
    context_param_name = ...
    user_field = 'author'
    model = ...

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_filtered = self.filter_by_user(self.model.objects.all())

        context[self.context_param_name] = user_filtered.filter(is_available=True).order_by('id')[:5]
        return context
    

class TextAuthorFilteringMixin(UserFilteringMixin):
    user_field = 'name'

    def get_gueryset(self):
        queryset = super().get_queryset()
        return self.filter_by_user(queryset)
    

class QueryFilterMixin:
    filter_field_name = ...
    query_param_name = ...
    filter_form = None
    form_context_name = 'search_form'

    def search_in_queryset(self, qs, filter_condition):
        return qs.filter(**filter_condition)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.filter_form:
            context[self.form_context_name] = self.filter_form(self.request.GET or None)
        return context
    
class BookNameFilterMixin(QueryFilterMixin):
    name_query_param = 'query'
    name_filter_field = 'name_icontains'
    filter_form = QueryFilterForm

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get(self.name_query_param)
        if query:
            queryset = self.search_in_queryset(queryset, {self.name_filter_field: query})
        return queryset


class AuthorNameFilterMixin(QueryFilterMixin):
    author_query_param = 'author'
    author_filter_field = 'author'
    filter_form = AuthorFilterForm


    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get(self.author_query_param)
        if query:
            queryset = self.search_in_queryset(queryset, {self.author_filter_field: query})
        return queryset


class AuthorBookNameMixin(AuthorNameFilterMixin, BookNameFilterMixin):
    filter_form = FilterBookForm


class GodModRequiredMixin(UserPassesTestMixin):
    def test_func(self) -> bool | None:
        return self.request.user.is_authenticated and self.request.user.username.startswith('godmode_')